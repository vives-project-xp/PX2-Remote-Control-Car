import pygame  # Import pygame library to handle joystick input
import time  # Import time library for controlling the loop timing
import lgpio  # Import lgpio library to control GPIO pins (PWM for motor control)
import math  # Import math library, though it's not being used in the current code

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
    """Set pedal values, accounting for deadzone to avoid noise near the neutral position."""
    
    # Raise an error if brake or throttle values are negative (they should be positive)
    if brake < 0 or throttle < 0:
        raise ValueError("Brake and throttle values cannot be negative")
    
    # Apply a deadzone to avoid joystick noise near the neutral position
    if abs(brake) < deadzone:
        brake = 0  # If brake value is within the deadzone, treat it as 0
    if abs(throttle) < deadzone:
        throttle = 0  # If throttle value is within the deadzone, treat it as 0

    # If the throttle is 0 and the brake is active (greater than 0)
    if throttle == 0 and brake > 0:
        voltage = 1.65 - brake  # Reduce voltage based on the brake value
        print("Brake works")  # Print that brake is active
        if voltage < 1.10:  # Ensure voltage doesn't go below 0.60V
            voltage = 1.10
        return voltage  # Return the calculated brake voltage
        
    # If the brake is 0 and the throttle is active (greater than 0)
    elif brake == 0 and throttle > 0:
        voltage = 1.65 + throttle  # Increase voltage based on the throttle value
        print("Throttle works")  # Print that throttle is active
        if voltage > 1.95:  # Ensure voltage doesn't go above 2.1V
            voltage = 1.95
        return voltage  # Return the calculated throttle voltage
        
    else:
        # If both brake and throttle are active (non-zero), print a message
        print("Both pedals are active")
        return 1.65  # Return a neutral voltage value if both pedals are active


def set_voltage(pin, voltage):
    """Set the voltage on the specified pin via PWM"""
    duty_cycle = (voltage / 3.3) * 100  # Convert voltage to a duty cycle (0-100%)
    lgpio.tx_pwm(chip, pin, 1500, duty_cycle)  # Set PWM signal on the pin with the duty cycle

# Define steering sensitivity factor
STEERING_SENSITIVITY = 2.5

try:
    print("G923 Steering Active")  # Print a message indicating that the steering control is active

    while True:  # Loop to continuously check for joystick input
        pygame.event.pump()  # Pump the pygame events (this is necessary to process joystick input)

        # Get the steering input from the joystick (axis 0)
        steering = joystick.get_axis(0)  # Get the steering axis (left-right)
        steering = steering * STEERING_SENSITIVITY  # Scale the steering input by sensitivity factor
        steering = max(min(steering, 1), -1)  # Ensure the steering value stays within [-1, 1]
        steering_voltage = (steering + 1) / 2 * 3.3  # Map the steering value to voltage range (0V to 3.3V)
        set_voltage(STEERING_PIN, steering_voltage)  # Set the PWM signal for steering control
        print(f"Steering: {steering:.2f}, Voltage: {steering_voltage:.2f}V")  # Print the steering value and voltage

        # Get the brake and throttle input from the joystick (axes 1 and 2)
        brake = 1 - joystick.get_axis(2)  # Invert the brake axis (since joystick axis values are typically [-1, 1])
        throttle = 1 - joystick.get_axis(1)  # Invert the throttle axis (same reason as brake)
        
        # Print the raw values of brake and throttle (debugging purposes)
        print(f"Raw Brake: {brake:.2f}, Raw Throttle: {throttle:.2f}")

        # Calculate the throttle/brake voltage based on the pedal inputs with the deadzone applied
        throttle_voltage = set_pedals(brake, throttle)
        
        set_voltage(THROTTLE_PIN, throttle_voltage)  # Set the PWM signal for throttle/brake control
        print(f"Throttle: {throttle:.2f}, Brake: {brake:.2f}, Voltage: {throttle_voltage:.2f}V")  # Print pedal values and voltage

        time.sleep(0.05)  # Add a small delay to prevent high CPU usage

except KeyboardInterrupt:  # Handle when the program is interrupted (e.g., pressing Ctrl+C)
    print("\nShutting down...")  # Print a message indicating shutdown

    set_voltage(THROTTLE_PIN, 1.65)  # Set throttle voltage to neutral (1.65V)
    time.sleep(0.5)  # Wait for a brief moment

    # Stop the PWM signals for both steering and throttle
    lgpio.tx_pwm(chip, STEERING_PIN, 1500, 50)  # Stop PWM signal on the steering pin
    lgpio.tx_pwm(chip, THROTTLE_PIN, 1500, 50)  # Stop PWM signal on the throttle pin

    # Close the GPIO chip to release the resources
    lgpio.gpiochip_close(chip)
