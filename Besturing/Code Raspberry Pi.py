
import pygame
import time
import lgpio
import math

# Define GPIO pins
STEERING_PIN = 18  # PWM pin voor sturen
THROTTLE_PIN = 19  # PWM pin voor gas/rem

# Open GPIO chip
chip = lgpio.gpiochip_open(0)

# Zet de GPIO-pinnen als PWM-uitgangen
lgpio.gpio_claim_output(chip, STEERING_PIN)
lgpio.gpio_claim_output(chip, THROTTLE_PIN)

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

def scale_exponential(value, min_input, max_input, min_output, max_output, k=2):
    
    # Normaliseer de waarde tussen 0 en 1
    normalized = (value - min_input) / (max_input - min_input)
    # Pas exponentiële curve toe
    exp_value = math.exp(k * normalized) / math.exp(k)
    # Schaal terug naar uitvoerbereik
    return min_output + (max_output - min_output) * exp_value

def set_voltage(pin, voltage):
    """Zet een spanning via PWM"""
    duty_cycle = (voltage / 3.3) * 100  # Converteer spanning naar duty cycle (0-100%)
    lgpio.tx_pwm(chip, pin, 800, duty_cycle)  # 1000Hz PWM

STEERING_SENSITIVITY = 2

try:
    print("G923-besturing actief")

    while True:
        pygame.event.pump()

        # Stuur (-1 = links, 1 = rechts)
        steering = joystick.get_axis(0)
        steering = steering * STEERING_SENSITIVITY  
        steering = max(min(steering, 1), -1)  
        steering_voltage = (steering + 1) / 2 * 3.3
        set_voltage(STEERING_PIN, steering_voltage)
        print(f"Stuur: {steering:.2f}, Voltage: {steering_voltage:.2f}V")

        # Gas (1 = geen gas, -1 = vol gas)
        throttle = joystick.get_axis(2)
        throttle_voltage = 1.65  # Neutraal

        # Rem (1 = geen rem, -1 = vol rem)
        brake = joystick.get_axis(1)
        
        # Prioriteit geven aan remmen als beide pedalen worden ingedrukt
        if brake < 0.9:
            brake_normalized = (brake - 1) / (-1 - 1)
            throttle_voltage = scale_exponential(brake_normalized, 0, 1, 1.65, 2, k=2)
        elif throttle < 0.9:
            throttle_normalized = (throttle - 1) / (-1 - 1)
            throttle_voltage = scale_exponential(throttle_normalized, 0, 1, 1.65, 0.85, k=2)

        set_voltage(THROTTLE_PIN, throttle_voltage)

        print(f"Throttle: {throttle:.2f}, Brake: {brake:.2f}, Voltage: {throttle_voltage:.2f}V")

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nAfsluiten...")

    set_voltage(THROTTLE_PIN, 1.65)
    time.sleep(0.5)

    # Stop PWM-signalen
    lgpio.tx_pwm(chip, STEERING_PIN, 1500, 50)
    lgpio.tx_pwm(chip, THROTTLE_PIN, 1500, 50)

    # GPIO chip sluiten
    lgpio.gpiochip_close(chip)
