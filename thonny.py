import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch Falling Objects")

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

font = pygame.font.SysFont(None, 36)
menu_font = pygame.font.SysFont(None, 48)

# Načteme obrázek košíku
basket_image = pygame.image.load("basket.png")  # Nahraďte "basket.png" cestou k vašemu obrázku
basket_width = basket_image.get_width()  # Získáme šířku obrázku
basket_height = basket_image.get_height()  # Získáme výšku obrázku

def draw_menu():
    screen.fill(BLACK)
    title_text = menu_font.render("Catch Falling Objects", True, WHITE)
    start_text = font.render("Press ENTER to Start", True, WHITE)
    screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, HEIGHT // 3))
    screen.blit(start_text, ((WIDTH - start_text.get_width()) // 2, HEIGHT // 2))
    pygame.display.flip()

def game_loop():
    basket_x = (WIDTH - basket_width) // 2
    basket_y = HEIGHT - basket_height - 10
    basket_speed = 8  

    object_width = 20
    object_height = 20
    falling_objects = []

    object_types = [
        {"color": RED, "effect": "normal", "points": 1, "chance": 1.0},
        {"color": DARK_GRAY, "effect": "bomb", "points": 0, "chance": 0.3},
        {"color": YELLOW, "effect": "bonus", "points": 2, "chance": 0.1},
        {"color": GREEN, "effect": "double", "points": 0, "chance": 0.01}
    ]

    score = 0
    lives = 3
    high_score = 0
    try:
        with open("highscore.txt", "r") as file:
            high_score = int(file.read())
    except FileNotFoundError:
        pass

    running = True
    clock = pygame.time.Clock()  
    spawn_rate = 80  
    frame_count = 0  
    max_objects = 5  

    while running:
        screen.fill(BLACK)  
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
            basket_x += basket_speed

        if frame_count % spawn_rate == 0 and len(falling_objects) < max_objects:
            obj_type = random.choices(object_types, weights=[t["chance"] for t in object_types])[0]
            falling_objects.append({
                "x": random.randint(0, WIDTH - object_width),
                "y": random.randint(-100, -50),  
                "speed": random.uniform(2.0, 2.5),  
                "color": obj_type["color"],
                "effect": obj_type["effect"],
                "points": obj_type["points"]
            })

        for obj in falling_objects[:]:
            obj["y"] += obj["speed"]
            pygame.draw.rect(screen, obj["color"], (obj["x"], obj["y"], object_width, object_height))

            if (obj["y"] + object_height >= basket_y) and (obj["x"] >= basket_x and obj["x"] + object_width <= basket_x + basket_width):
                if obj["effect"] == "normal" or obj["effect"] == "bonus":
                    score += obj["points"]
                elif obj["effect"] == "double":
                    score *= 2
                elif obj["effect"] == "bomb":
                    lives -= 1
                    if lives == 0:
                        return
                falling_objects.remove(obj)

            if obj["y"] > HEIGHT:
                if obj["effect"] == "normal" or obj["effect"] == "bonus":
                    lives -= 1
                    if lives == 0:
                        return
                falling_objects.remove(obj)

        # Aktualizace high score během hry
        if score > high_score:
            high_score = score
            with open("highscore.txt", "w") as file:
                file.write(str(high_score))

        # Zobrazení košíku jako obrázku
        screen.blit(basket_image, (basket_x, basket_y))  # Nakreslí obrázek na pozici košíku

        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(score_text, (10, 10))  
        screen.blit(lives_text, (10, 40))
        screen.blit(high_score_text, (10, 100))

        pygame.display.flip()  

        frame_count += 1
        clock.tick(60)  

while True:
    draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            game_loop()
