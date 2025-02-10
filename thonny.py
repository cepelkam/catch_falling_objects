import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch Falling Objects")

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)

basket_width = 100
basket_height = 20
basket_x = (WIDTH - basket_width) // 2
basket_y = HEIGHT - basket_height - 10
basket_speed = 8  

object_width = 20
object_height = 20
falling_objects = []

object_colors = [RED, GREEN, YELLOW, PURPLE, ORANGE]

score = 0
lives = 3
font = pygame.font.SysFont(None, 36)

high_score = 0
try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    pass

print(f"Loaded high score: {high_score}")  

running = True
clock = pygame.time.Clock()  
spawn_rate = 60  
frame_count = 0  
max_objects = 10  
min_speed = 2.0  
max_speed = 2.5  

while running:
    screen.fill(BLACK)  
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
        basket_x += basket_speed

    if frame_count % spawn_rate == 0 and len(falling_objects) < max_objects:
        if score > 10:
            min_speed = 2.2
            max_speed = 2.7
        if score > 20:
            min_speed = 2.5
            max_speed = 3.0

        falling_objects.append({
            "x": random.randint(0, WIDTH - object_width),
            "y": random.randint(-100, -50),  
            "speed": random.uniform(min_speed, max_speed),  
            "color": random.choice(object_colors)  
        })

    if frame_count > 1000:
        spawn_rate = 70  
    if frame_count > 2000:
        spawn_rate = 80  

    for obj in falling_objects[:]:
        obj["y"] += obj["speed"]
        pygame.draw.rect(screen, obj["color"], (obj["x"], obj["y"], object_width, object_height))

        if (obj["y"] + object_height >= basket_y) and (obj["x"] >= basket_x and obj["x"] + object_width <= basket_x + basket_width):
            score += 1  
            falling_objects.remove(obj)

        if obj["y"] > HEIGHT:
            falling_objects.remove(obj)
            lives -= 1
            if lives == 0:
                running = False

    pygame.draw.rect(screen, BLUE, (basket_x, basket_y, basket_width, basket_height))

    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (10, 10))  
    screen.blit(lives_text, (10, 40))
    screen.blit(high_score_text, (10, 100))

    pygame.display.flip()  

    frame_count += 1
    clock.tick(60)  

if score > high_score:
    print(f"New high score saved: {score}")  
    with open("highscore.txt", "w") as file:
        file.write(str(score))

pygame.quit()