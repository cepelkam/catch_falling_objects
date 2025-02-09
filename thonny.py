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
font = pygame.font.SysFont(None, 36)

running = True
clock = pygame.time.Clock()  
spawn_rate = 60  
frame_count = 0  
max_objects = 5  

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
        falling_objects.append({
            "x": random.randint(0, WIDTH - object_width),
            "y": random.randint(-100, -50),  
            "speed": random.uniform(1.0, 2.5),  
            "color": random.choice(object_colors)  
        })

    if frame_count > 1000:
        spawn_rate = 90 
    if frame_count > 2000:
        spawn_rate = 120  

    for obj in falling_objects:
        obj["y"] += obj["speed"]
        pygame.draw.rect(screen, obj["color"], (obj["x"], obj["y"], object_width, object_height))

        if (obj["y"] + object_height >= basket_y) and (obj["x"] >= basket_x and obj["x"] + object_width <= basket_x + basket_width):
            score += 1  
            obj["x"] = random.randint(0, WIDTH - object_width) 
            obj["y"] = random.randint(-100, -50)  

        if obj["y"] > HEIGHT:
            obj["x"] = random.randint(0, WIDTH - object_width)
            obj["y"] = random.randint(-100, -50)  

    pygame.draw.rect(screen, BLUE, (basket_x, basket_y, basket_width, basket_height))

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))  

    pygame.display.flip()  

    frame_count += 1
    clock.tick(60)  

pygame.quit()
