import pygame
pygame.init()

# Initialize a display window (necessary for some systems)
pygame.display.set_mode((1, 1))  # Tiny invisible window

crash_sound = pygame.mixer.Sound("smal_Beep.wav")
print("this works")

pygame.mixer.Sound.play(crash_sound)
pygame.time.wait(int(crash_sound.get_length() * 1000))  # Wait for sound duration
print("this works")
