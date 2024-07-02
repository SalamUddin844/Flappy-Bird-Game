import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)

# Game settings
bird_width = 50
bird_height = 50
bird_x = screen_width // 4
bird_y = screen_height // 2
bird_velocity = 0
gravity = 1
flap_strength = -10

pipe_width = 100
pipe_gap = 200
pipe_velocity = 5
pipe_frequency = 1500  # milliseconds

# Font settings
font = pygame.font.SysFont("comicsansms", 35)

# Game variables
pipes = []
score = 0
running = True
clock = pygame.time.Clock()

# Pipe generation event
pygame.time.set_timer(pygame.USEREVENT, pipe_frequency)

# Function to draw the bird
def draw_bird(x, y):
    pygame.draw.rect(screen, red, (x, y, bird_width, bird_height))

# Function to draw pipes
def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, green, pipe['top_rect'])
        pygame.draw.rect(screen, green, pipe['bottom_rect'])

# Function to generate new pipes
def generate_pipe():
    pipe_height = random.randint(100, screen_height - pipe_gap - 100)
    top_rect = pygame.Rect(screen_width, 0, pipe_width, pipe_height)
    bottom_rect = pygame.Rect(screen_width, pipe_height + pipe_gap, pipe_width, screen_height - pipe_height - pipe_gap)
    return {'top_rect': top_rect, 'bottom_rect': bottom_rect}

# Function to check for collisions
def check_collision(bird_rect, pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe['top_rect']) or bird_rect.colliderect(pipe['bottom_rect']):
            return True
    if bird_rect.top <= 0 or bird_rect.bottom >= screen_height:
        return True
    return False

# Function to display score
def display_score(score):
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (10, 10))

# Main game loop
while running:
    screen.fill(blue)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = flap_strength
        if event.type == pygame.USEREVENT:
            pipes.append(generate_pipe())
    
    # Bird movement
    bird_velocity += gravity
    bird_y += bird_velocity
    bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
    
    # Pipe movement
    for pipe in pipes:
        pipe['top_rect'].x -= pipe_velocity
        pipe['bottom_rect'].x -= pipe_velocity
    
    # Remove pipes that have gone off screen
    pipes = [pipe for pipe in pipes if pipe['top_rect'].right > 0]
    
    # Check for collisions
    if check_collision(bird_rect, pipes):
        running = False
    
    # Draw bird and pipes
    draw_bird(bird_x, bird_y)
    draw_pipes(pipes)
    
    # Display score
    score += 1
    display_score(score // 100)
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()
