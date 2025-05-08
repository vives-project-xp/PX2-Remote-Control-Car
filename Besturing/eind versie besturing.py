import pygame
import time 
import lgpio
import math

# Define GPIO pins for steering and throttle/brake control
STEERING_PIN = 18  # PWM pin for steering control
THROTTLE_PIN = 19  # PWM pin for throttle/brake control

# Open the GPIO chip (hardware interface)
chip = lgpio.gpiochip_open(0)

# Set the GPIO pins for steering and throttle/brake as PWM outputs
lgpio.gpio_claim_output(chip, STEERING_PIN)
lgpio.gpio_claim_output(chip, THROTTLE_PIN)

# Initialize pygame for joystick handling
pygame.init()
pygame.joystick.init()

# Initialize and find the first joystick (assuming the first joystick is used)
joystick = pygame.joystick.Joystick(0)
joystick.init()


def set_pedals(brake, throttle, deadzone=0.05):
    # set pedals function to calculate voltage
    
    if brake < 0 or throttle < 0:
        raise ValueError("Brake and throttle values cannot be negative")
    
    # Apply a deadzone to avoid joystick noise near the neutral position
    if abs(brake) < deadzone:
        brake = 0
    if abs(throttle) < deadzone:
        throttle = 0

    # If the throttle is 0 and the brake is active (greater than 0)
    if throttle == 0 and brake > 0:
        voltage = 1.65 - brake
        print("Brake works")
        if voltage < 1.10:  # limit the speed
            voltage = 1.10
        return voltage
        
    # If the brake is 0 and the throttle is active (greater than 0)
    elif brake == 0 and throttle > 0:
        voltage = 1.65 + throttle
        print("Throttle works")
        if voltage > 1.95:  # limit the speed
            voltage = 1.95
        return voltage
        
    else:
        print("Both pedals are active")
        return 1.65  # Return a neutral voltage value if both pedals are active


def set_voltage(pin, voltage):
    # voltage to PWM
    duty_cycle = (voltage / 3.3) * 100  # Convert voltage to a duty cycle (0-100%)
    lgpio.tx_pwm(chip, pin, 1500, duty_cycle)  # Set PWM signal on the pin with the duty cycle

STEERING_SENSITIVITY = 2.5

try:
    print("G923 Steering Active")
    while True:
        pygame.event.pump()

        # Get the steering input from the joystick (axis 0)
        steering = joystick.get_axis(0)
        steering = steering * STEERING_SENSITIVITY
        steering = max(min(steering, 1), -1)
        steering_voltage = (steering + 1) / 2 * 3.3
        set_voltage(STEERING_PIN, steering_voltage)
        print(f"Steering: {steering:.2f}, Voltage: {steering_voltage:.2f}V")
        
        # Get the brake and throttle input from the joystick (axes 1 and 2)
        brake = 1 - joystick.get_axis(2)  # Invert the brake axis
        throttle = 1 - joystick.get_axis(1)
        
        print(f"Raw Brake: {brake:.2f}, Raw Throttle: {throttle:.2f}")

        throttle_voltage = set_pedals(brake, throttle)
        
        set_voltage(THROTTLE_PIN, throttle_voltage)
        print(f"Throttle: {throttle:.2f}, Brake: {brake:.2f}, Voltage: {throttle_voltage:.2f}V")

        time.sleep(0.05)

except KeyboardInterrupt:  # Handle when the program is interrupted (e.g., pressing Ctrl+C)
    print("\nShutting down...")

    set_voltage(THROTTLE_PIN, 1.65)  # Set throttle voltage to neutral (1.65V)
    time.sleep(0.5)

    # Stop the PWM signals for both steering and throttle
    lgpio.tx_pwm(chip, STEERING_PIN, 1500, 50)
    lgpio.tx_pwm(chip, THROTTLE_PIN, 1500, 50)

    lgpio.gpiochip_close(chip)
