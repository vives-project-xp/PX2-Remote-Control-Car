import pygame
import time
import RPi.GPIO as GPIO
from light_control import LightControl
import serial
import time

lc = LightControl()

COM_PORT = '/dev/ttyS0'    # Gebruikte poort
BAUD_RATE = 115200         # Baudrate van de seriële console
TARGET_TAG    = "3000E280699500004014CC14" # Doel tag ID 1 (oranje auto)
TARGET_TAG_2 = "3000E200420072C06017068E" # Doel tag ID 2 nog niet finale ID (rode auto)


INVENTORY_CMD = bytes.fromhex("BB 00 22 00 00 22 7E")

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Time View")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font_large = pygame.font.Font(None, HEIGHT // 5)
font_small = pygame.font.Font(None, HEIGHT // 10)
font_medium = pygame.font.Font(None, HEIGHT // 8)

# Initialize variables
start_ticks = 0
time_str = "00:00.000"
auto1_name = "Oranje auto"
auto2_name = "Rode auto"
auto1_time = "00:00.000"
auto2_time = "00:00.000"
auto1_stopped = False
auto2_stopped = False
auto1_stop_ticks = 0
auto2_stop_ticks = 0
timer_stopped = 0
timer_running = False

def parse_tag_id(data):
    # Check if the data is long enough and has the correct header
    if len(data) < 6 or data[0] != 0xBB or data[2] != 0x22:
        return None
    
    # Data length is two bytes (little-endian)
    data_length = data[3]
    
    # Check if the packet is complete
    if len(data) < 5 + data_length + 2:  # Header (5 bytes) + data + checksum (2)
        return None
    
    # Tag ID is typically 12 bytes starting at index 10
    tag_start = 6
    tag_end = tag_start + 12
    if tag_end > len(data) - 2:  # Ensure we don't exceed data and checksum
        return None
    
    tag_bytes = data[tag_start:tag_end]
    
    return tag_bytes.hex().upper()


ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
print(f"Verbonden met {COM_PORT}")

running = True
while running:
    screen.fill(WHITE)
    
    ser.write(INVENTORY_CMD)
        
    # Read response
    buffer = ser.read(ser.in_waiting or 1)
        
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
    
    # Calculate elapsed time
    if timer_running and not timer_stopped:
        elapsed_seconds = elapsed_ticks // 1000
        elapsed_minutes = elapsed_seconds // 60
        elapsed_seconds = elapsed_seconds % 60
        elapsed_milliseconds = elapsed_ticks % 1000
        time_str = f"{elapsed_minutes:02}:{elapsed_seconds:02}.{elapsed_milliseconds:03d}"
    
    if not auto1_stopped and timer_running:
        auto1_time = time_str
    if not auto2_stopped and timer_running:
        auto2_time = time_str
    
    # Calculate current time for each car
    # If the car is stopped, use the stop time; otherwise, use the elapsed time
    auto1_current = auto1_stop_ticks if auto1_stopped else (elapsed_ticks if timer_running else 0)
    auto2_current = auto2_stop_ticks if auto2_stopped else (elapsed_ticks if timer_running else 0)
    
    if auto1_current <= auto2_current:
        first_name, first_time = auto1_name, auto1_time
        second_name, second_time = auto2_name, auto2_time
    else:
        first_name, first_time = auto2_name, auto2_time
        second_name, second_time = auto1_name, auto1_time
    
    # Check start button state
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
    
    # Check reset button state
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

        if auto1_stop_ticks <= auto2_stop_ticks:
            winner_name = auto1_name
            winner_time = auto1_time
        else:
            winner_name = auto2_name
            winner_time = auto2_time

        if auto1_stop_ticks == auto2_stop_ticks:
            winner_text = font_medium.render(f"Gelijkspel", True, BLACK)
        else:
            winner_text = font_medium.render(f"Winner: {winner_name}", True, BLACK)
        
        winner_time_text = font_small.render(f"Time: {winner_time}", True, BLACK)
        screen.fill(WHITE)
        screen.blit(winner_text, (WIDTH * 0.2, HEIGHT * 0.4))
        screen.blit(winner_time_text, (WIDTH * 0.2, HEIGHT * 0.6))
        pygame.display.flip()
        
        pygame.time.delay(3000)
    
    # Draw the text on the screen
    title_text = font_large.render(f"Tijd: {time_str}", True, BLACK)
    first_text = font_small.render(f"1st  —  {first_name}  —  {first_time}", True, BLACK)
    second_text = font_small.render(f"2nd  —  {second_name}  —  {second_time}", True, BLACK)
    
    screen.blit(title_text, (WIDTH * 0.05, HEIGHT * 0.05))
    screen.blit(first_text, (WIDTH * 0.05, HEIGHT * 0.35))
    screen.blit(second_text, (WIDTH * 0.05, HEIGHT * 0.65))
    
    # Check for events
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
    
    pygame.display.flip()

GPIO.cleanup()
pygame.quit()
lc.cleanup()
ser.close()
