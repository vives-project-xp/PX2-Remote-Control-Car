import pygame
import time

# Initialize pygame
pygame.init()

# Full-screen settings
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Time View")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font_large = pygame.font.Font(None, HEIGHT // 5)
font_small = pygame.font.Font(None, HEIGHT // 6)

# Initial text
start_ticks = pygame.time.get_ticks()
auto1_name = "Auto 1"
auto2_name = "Auto 2"
auto1_time = "00:00.000"
auto2_time = "00:00.000"
auto1_stopped = False
auto2_stopped = False
auto1_stop_ticks = 0
auto2_stop_ticks = 0

# Main loop
running = True
while running:
    screen.fill(WHITE)
    
    # Calculate elapsed time
    elapsed_ticks = pygame.time.get_ticks() - start_ticks
    elapsed_seconds = elapsed_ticks // 1000
    elapsed_minutes = elapsed_seconds // 60
    elapsed_seconds = elapsed_seconds % 60
    elapsed_milliseconds = elapsed_ticks % 1000
    time_str = f"{elapsed_minutes:02}:{elapsed_seconds:02}.{elapsed_milliseconds:03d}"
    
    # Update auto times if not stopped
    if not auto1_stopped:
        auto1_time = time_str
    if not auto2_stopped:
        auto2_time = time_str
    
    # Render text
    title_text = font_large.render(f"Tijd: {time_str}", True, BLACK)
    first_text = font_small.render(f"1st  —  {auto1_name}  —  {auto1_time}", True, BLACK)
    second_text = font_small.render(f"2nd  —  {auto2_name}  —  {auto2_time}", True, BLACK)
    
    # Draw text centered
    screen.blit(title_text, (WIDTH * 0.05, HEIGHT * 0.05))
    screen.blit(first_text, (WIDTH * 0.05, HEIGHT * 0.35))
    screen.blit(second_text, (WIDTH * 0.05, HEIGHT * 0.65))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False  # Exit full screen when ESC is pressed
            elif event.key == pygame.K_SPACE:
                if not auto1_stopped:
                    auto1_stopped = True
                    auto1_stop_ticks = elapsed_ticks
                elif not auto2_stopped:
                    auto2_stopped = True
                    auto2_stop_ticks = elapsed_ticks
    
    pygame.display.flip()

pygame.quit()
