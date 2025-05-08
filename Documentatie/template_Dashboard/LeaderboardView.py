import pygame
import random

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Leaderboard")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font_large = pygame.font.Font(None, HEIGHT // 10)
font_small = pygame.font.Font(None, HEIGHT // 15)

title_text = font_large.render("Leaderboard", True, BLACK)
positions = [
    "1st", "2nd", "3rd", "4th", "5th",
    "6th", "7th", "8th", "9th", "10th"
]

times = sorted([random.randint(0, 999999) for _ in range(10)])

formatted_times = [f"{t // 60000:02}:{(t // 1000) % 60:02}.{t % 1000:03d}" for t in times]

logo = pygame.image.load("Documentatie/template_Dashboard/img/logo_Vives.png")
logo = pygame.transform.scale(logo, (WIDTH // 2.5, HEIGHT // 2.5))
logo_rect = logo.get_rect()
logo_rect.topright = (WIDTH - 75, 250)

running = True
while running:
    screen.fill(WHITE)
    
    screen.blit(title_text, (WIDTH * 0.05, HEIGHT * 0.05))
    
    for i, (pos, time_str) in enumerate(zip(positions, formatted_times)):
        text = font_small.render(f"{pos}  —  naam  —  {time_str}", True, BLACK)
        screen.blit(text, (WIDTH * 0.10, HEIGHT * (0.15 + i * 0.08)))
    
    screen.blit(logo, logo_rect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    
    pygame.display.flip()

pygame.quit()
