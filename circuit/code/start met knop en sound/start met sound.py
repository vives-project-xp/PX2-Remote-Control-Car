import time  # Import the time module for delays
import board  # Import the board module for hardware pin definitions
import neopixel  # Import the neopixel module to control NeoPixel LEDs
import random  # Import the random module for generating random numbers
import RPi.GPIO as GPIO  # Import the GPIO module for Raspberry Pi GPIO control
import pygame  # Import the pygame module for audio playback

# GPIO initialization
GPIO.setwarnings(False)  # Disable GPIO warnings
if GPIO.getmode() is not None:  # Check if GPIO mode is already set
    GPIO.cleanup()  # Clean up GPIO settings if already configured
BUTTON_PIN = 7  # Define the GPIO pin number for the button
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up the button pin as input with a pull-up resistor

# NeoPixel configuration
pixels = neopixel.NeoPixel(
    board.D18,  # Define the GPIO pin connected to the NeoPixel data line
    89,  # Number of NeoPixel LEDs in the strip
    brightness=0.5,  # Set the brightness level of the LEDs
    pixel_order=neopixel.GRBW,  # Define the color order (Green, Red, Blue, White) (note that for some reason green and red are switched)
    auto_write=False  # Disable automatic updates to the LEDs
)

# Audio initialization
pygame.mixer.init()  # Initialize the pygame mixer for audio playback

def f1_5_lights(small_beep, long_beep):
    # Define segments of LEDs to light up
    segments = [(5, 10), (22, 28), (42, 48), (62, 68), (80, 85)]
    
    # Reset all LEDs to off
    pixels.fill((0, 0, 0, 0))  # Set all LEDs to black (off)
    pixels.show()  # Update the LEDs to reflect the changes
    time.sleep(1)  # Wait for 1 second

    # Light up each segment with a beep
    for start, end in segments:  # Iterate through each segment
        pixels[start:end] = [(255, 0, 0, 0)] * (end - start)  # Set the segment to red
        pixels.show()  # Update the LEDs
        small_beep.play()  # Play the small beep sound
        time.sleep(1)  # Wait for 1 second
    
    # Wait for a random amount of time
    time.sleep(1)  # Wait for 1 second
    time.sleep(random.uniform(0.2, 0.8))  # Wait for an additional random time between 0.2 and 0.8 seconds
    
    # Turn off the LEDs and play the long beep
    pixels.fill((0, 0, 0, 0))  # Set all LEDs to black (off)
    pixels.show()  # Update the LEDs
    long_beep.play()  # Play the long beep sound
    time.sleep(long_beep.get_length())  # Wait until the long beep finishes playing

def main():
    try:
        # Load sound effects
        small_beep = pygame.mixer.Sound('smal_Beep.wav')  # Load the small beep sound file
        long_beep = pygame.mixer.Sound('long_beep.wav')  # Load the long beep sound file
        
        print("Ready - Druk op de knop (PIN7) om te starten...")  # Print a message indicating readiness
        while True:  # Infinite loop to wait for button press
            if not GPIO.input(BUTTON_PIN):  # Check if the button is pressed
                print("Start sequence!")  # Print a message indicating the sequence has started
                f1_5_lights(small_beep, long_beep)  # Call the function to execute the light and sound sequence
                
                # Wait until the button is released
                time.sleep(0.5)  # Debounce delay
                while not GPIO.input(BUTTON_PIN):  # Wait while the button is still pressed
                    time.sleep(0.1)  # Small delay to avoid busy-waiting
                
    except KeyboardInterrupt:  # Handle Ctrl+C interrupt
        print("\nAfsluiten...")  # Print a message indicating shutdown
        pixels.fill((0, 0, 0, 0))  # Turn off all LEDs
        pixels.show()  # Update the LEDs
        pygame.mixer.quit()  # Quit the pygame mixer
        GPIO.cleanup()  # Clean up GPIO settings

if __name__ == "__main__":
    main()  # Run the main function if the script is executed directly
