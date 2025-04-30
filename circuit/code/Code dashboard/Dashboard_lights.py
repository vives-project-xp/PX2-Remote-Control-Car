import pygame
import time
import RPi.GPIO as GPIO
from light_control import LightControl
import serial
import time

# Initialiseer het LightControl-object
lc = LightControl()

COM_PORT = '/dev/ttyS0'    # Gebruikte seriële poort
BAUD_RATE = 115200         # Baudrate van de seriële console
TARGET_TAG    = "3000E280699500004014CC14" # Doel tag ID 1 (oranje auto)
TARGET_TAG_2 = "3000E200420072C06017068E" # Doel tag ID 2 (rode auto, nog niet finale ID)

# Definieer het commando dat naar de lezer wordt gestuurd
INVENTORY_CMD = bytes.fromhex("BB 00 22 00 00 22 7E")

# Initialiseer GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Instellen van knop 1
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Instellen van knop 2

# Initialiseer Pygame
pygame.init()

# Stel het scherm in
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Time View")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Stel lettertypen in
font_large = pygame.font.Font(None, HEIGHT // 5)
font_small = pygame.font.Font(None, HEIGHT // 10)
font_medium = pygame.font.Font(None, HEIGHT // 8)

# Initialiseer variabelen
start_ticks = 0  # Houdt de starttijd bij (in milliseconden) wanneer de timer begint
time_str = "00:00.000"  # Stringrepresentatie van de verstreken tijd in minuten, seconden en milliseconden
auto1_name = "Oranje auto"  # Naam van de eerste auto (Oranje auto)
auto2_name = "Rode auto"  # Naam van de tweede auto (Rode auto)
auto1_time = "00:00.000"  # Verstreken tijd voor de eerste auto (wordt bijgewerkt tijdens de timer of wanneer gestopt)
auto2_time = "00:00.000"  # Verstreken tijd voor de tweede auto (wordt bijgewerkt tijdens de timer of wanneer gestopt)
auto1_stopped = False  # Boolean die aangeeft of de eerste auto is gestopt
auto2_stopped = False  # Boolean die aangeeft of de tweede auto is gestopt
auto1_stop_ticks = 0  # Houdt de tijd bij (in milliseconden) waarop de eerste auto is gestopt
auto2_stop_ticks = 0  # Houdt de tijd bij (in milliseconden) waarop de tweede auto is gestopt
timer_stopped = 0  # Boolean die aangeeft of de timer is gestopt
timer_running = False  # Boolean die aangeeft of de timer momenteel loopt

def parse_tag_id(data):
    # Controleer of de data lang genoeg is en de juiste header heeft
    if len(data) < 6 or data[0] != 0xBB or data[2] != 0x22:
        return None
    
    # De lengte van de data is twee bytes (little-endian)
    data_length = data[3]
    
    # Controleer of het pakket compleet is
    if len(data) < 5 + data_length + 2:  # Header (5 bytes) + data + checksum (2)
        return None
    
    # Tag ID is meestal 12 bytes vanaf index 10
    tag_start = 6
    tag_end = tag_start + 12
    if tag_end > len(data) - 2:  # Zorg ervoor dat we niet buiten de data en checksum gaan
        return None
    
    tag_bytes = data[tag_start:tag_end]
    
    return tag_bytes.hex().upper()

# Initialiseer de seriële verbinding
ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
print(f"Verbonden met {COM_PORT}")

running = True
while running:
    screen.fill(WHITE)
    
    ser.write(INVENTORY_CMD)
        
    # Lees de respons
    buffer = ser.read(ser.in_waiting or 1)
    
    # Controleer of de buffer niet leeg is en parse de tag ID
    if buffer:
        tag = parse_tag_id(buffer)
        if tag:
            if tag == TARGET_TAG and timer_running and not auto1_stopped:
                auto1_stopped    = True
                auto1_stop_ticks = pygame.time.get_ticks() - start_ticks
                auto1_time       = time_str
            elif tag == TARGET_TAG_2 and timer_running and not auto2_stopped:
                auto2_stopped = True
                auto2_stop_ticks = pygame.time.get_ticks() - start_ticks
                auto2_time = time_str

    elapsed_ticks = pygame.time.get_ticks() - start_ticks if timer_running else 0
    
    # Bereken verstreken tijd
    if timer_running and not timer_stopped:
        elapsed_seconds = elapsed_ticks // 1000
        elapsed_minutes = elapsed_seconds // 60
        elapsed_seconds = elapsed_seconds % 60
        elapsed_milliseconds = elapsed_ticks % 1000
        time_str = f"{elapsed_minutes:02}:{elapsed_seconds:02}.{elapsed_milliseconds:03d}"
    
    # Update de tijd voor elke auto als ze niet gestopt zijn
    if not auto1_stopped and timer_running:
        auto1_time = time_str
    if not auto2_stopped and timer_running:
        auto2_time = time_str
    
    # Bereken de huidige tijd voor elke auto
    # Als de auto is gestopt, gebruik de stoptijd; anders de verstreken tijd
    auto1_current = auto1_stop_ticks if auto1_stopped else (elapsed_ticks if timer_running else 0)
    auto2_current = auto2_stop_ticks if auto2_stopped else (elapsed_ticks if timer_running else 0)
    
    # Bepaal de volgorde van de auto's op basis van hun huidige tijd
    if auto1_current <= auto2_current:
        first_name, first_time = auto1_name, auto1_time
        second_name, second_time = auto2_name, auto2_time
    else:
        first_name, first_time = auto2_name, auto2_time
        second_name, second_time = auto1_name, auto1_time
    
    # Controleer de status van de startknop
    if GPIO.input(23) == GPIO.LOW:
        lc.start_sequence()
        timer_running = True
        timer_stopped = False
        auto1_stopped = False
        auto2_stopped = False
        auto1_time = "00:00.000"
        auto2_time = "00:00.000"
        start_ticks = pygame.time.get_ticks()
        print("start")
        pygame.time.delay(200)
    
    # Controleer de status van de resetknop
    if GPIO.input(25) == GPIO.LOW:
        lc.reset_lights()
        timer_running = False
        timer_stopped = False
        auto1_stopped = False
        auto2_stopped = False
        auto1_time = "00:00.000"
        auto2_time = "00:00.000"
        time_str = "00:00.000"
        print("reset")
        pygame.time.delay(200)
        
    if auto1_stopped and auto2_stopped and not timer_stopped:
        timer_stopped = True
        pygame.time.delay(1000)
        # Bepaal de winnaar
        if auto1_stop_ticks <= auto2_stop_ticks:
            winner_name = auto1_name
            winner_time = auto1_time
        else:
            winner_name = auto2_name
            winner_time = auto2_time
            
        # Bepaal de winnaarstijd
        if auto1_stop_ticks == auto2_stop_ticks:
            winner_text = font_medium.render(f"Gelijkspel", True, BLACK)
        else:
            winner_text = font_medium.render(f"Winnaar: {winner_name}", True, BLACK)
        
        # Toon de winnaar en tijd
        winner_time_text = font_small.render(f"Tijd: {winner_time}", True, BLACK)
        screen.fill(WHITE)
        screen.blit(winner_text, (WIDTH * 0.2, HEIGHT * 0.4))
        screen.blit(winner_time_text, (WIDTH * 0.2, HEIGHT * 0.6))
        pygame.display.flip()
        
        pygame.time.delay(3000)
    
    # Teken de tekst op het scherm
    title_text = font_large.render(f"Tijd: {time_str}", True, BLACK)
    first_text = font_small.render(f"1e  —  {first_name}  —  {first_time}", True, BLACK)
    second_text = font_small.render(f"2e  —  {second_name}  —  {second_time}", True, BLACK)
    
    # Teken de tekst op het scherm
    screen.blit(title_text, (WIDTH * 0.05, HEIGHT * 0.05))
    screen.blit(first_text, (WIDTH * 0.05, HEIGHT * 0.35))
    screen.blit(second_text, (WIDTH * 0.05, HEIGHT * 0.65))
    
    # Controleer op gebeurtenissen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            lc.cleanup()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_1 and timer_running and not auto1_stopped:
                auto1_stopped = True
                auto1_stop_ticks = pygame.time.get_ticks() - start_ticks
                auto1_time = time_str
            elif event.key == pygame.K_2 and timer_running and not auto2_stopped:
                auto2_stopped = True
                auto2_stop_ticks = pygame.time.get_ticks() - start_ticks
                auto2_time = time_str
    # Update het scherm
    pygame.display.flip()

GPIO.cleanup()
pygame.quit()
lc.cleanup()
ser.close()
