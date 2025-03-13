import pygame  # Voor de input van stuur en pedalen in te lezen
import time
import lgpio  # Voor de GPIO-besturing van de motoren
import math  # Voor exponentiële berekeningen

# Define GPIO pins
STEERING_PIN = 18  # PWM pin voor sturen
THROTTLE_PIN = 19  # PWM pin voor gas/rem

# Open GPIO chip
chip = lgpio.gpiochip_open(0)

# Zet de GPIO-pinnen als PWM-uitgangen
lgpio.gpio_claim_output(chip, STEERING_PIN)
lgpio.gpio_claim_output(chip, THROTTLE_PIN)

# pygame init
pygame.init()
pygame.joystick.init()

# Zoek en initialiseer het stuur
joystick = pygame.joystick.Joystick(0)
joystick.init()

def scale_exponential_mirrored(value, min_input, max_input, min_output, max_output, k=3):
    """Schaal een waarde met een omgekeerde exponentiële curve (snelle respons in het begin, trager aan het einde)."""
    normalized_value = (value - min_input) / (max_input - min_input)  # Schalen naar 0-1
    mirrored_value = math.exp(-k * (1 - normalized_value))  # Omgekeerde exponentiële curve
    return min_output + (max_output - min_output) * mirrored_value  # Terugschalen naar uitvoerbereik

def set_voltage(pin, voltage):
    """Zet een spanning via PWM"""
    duty_cycle = (voltage / 3.3) * 100  # Converteer spanning naar duty cycle (0-100%)
    lgpio.tx_pwm(chip, pin, 1500, duty_cycle)  # 1000Hz PWM

# Gevoeligheid van de besturing
STEERING_SENSITIVITY = 2.5  

try:
    print("G923-besturing actief")

    while True:
        pygame.event.pump()

        # Stuur (-1 = links, 1 = rechts)
        steering = joystick.get_axis(0)
        steering = steering * STEERING_SENSITIVITY  
        steering = max(min(steering, 1), -1)  
        steering_voltage = (steering + 1) / 2 * 3.3  # Normale lineaire schaling
        set_voltage(STEERING_PIN, steering_voltage)
        print(f"Stuur: {steering:.2f}, Voltage: {steering_voltage:.2f}V")

        # Gas (1 = geen gas, -1 = vol gas)
        throttle = joystick.get_axis(2)
        throttle_voltage = 1.65  # Neutraal

        if throttle < 0.9:  # Gas wordt ingedrukt
            throttle_voltage = scale_exponential_mirrored(throttle, 1, -1, 1.65, 0.9, k=3)  

        # Rem (1 = geen rem, -1 = vol rem)
        brake = joystick.get_axis(1)

        if brake < 0.9:  # Rem wordt ingedrukt
            throttle_voltage = scale_exponential_mirrored(brake, 1, -1, 1.65, 2.4, k=3)  

        set_voltage(THROTTLE_PIN, throttle_voltage)

        print(f"Throttle: {throttle:.2f}, Brake: {brake:.2f}, Voltage: {throttle_voltage:.2f}V")

        time.sleep(0.05)  # Voorkom CPU-overbelasting

except KeyboardInterrupt:
    print("\nAfsluiten...")

    # Stop PWM-signalen
    lgpio.tx_pwm(chip, STEERING_PIN, 0, 0)
    lgpio.tx_pwm(chip, THROTTLE_PIN, 0, 0)

    # GPIO chip sluiten
    lgpio.gpiochip_close(chip)
