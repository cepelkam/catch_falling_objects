import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch Falling Objects")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

font = pygame.font.SysFont(None, 36)

# Načtení obrázků
basket_image = pygame.image.load("basket.png")
apple_image = pygame.image.load("apple.png")  # Jablko pro červený objekt

# Úprava velikosti obrázků podle potřeby
object_size = (30, 30)  # Nastav velikost objektů
apple_image = pygame.transform.scale(apple_image, object_size)

basket_width = basket_image.get_width()
basket_height = basket_image.get_height()

def game_loop():
    basket_x = (WIDTH - basket_width) // 2
    basket_y = HEIGHT - basket_height - 10
    basket_speed = 8

    falling_objects = []

    object_types = [
        {"image": apple_image, "effect": "normal", "points": 1, "chance": 1.0},  # Jablko místo červeného objektu
        {"color": DARK_GRAY, "effect": "bomb", "points": 0, "chance": 0.3},
        {"color": YELLOW, "effect": "bonus", "points": 2, "chance": 0.1},
        {"color": GREEN, "effect": "double", "points": 0, "chance": 0.01},
        {"color": WHITE, "effect": "speed_boost", "points": 0, "chance": 0.05}
    ]

    score = 0
    lives = 3
    normal_speed_range = (2.0, 2.5)
    boosted_speed_range = (4.0, 5.0)
    speed_boost_active = False
    speed_boost_timer = 0

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
                "x": random.randint(0, WIDTH - object_size[0]),
                "y": random.randint(-100, -50),
                "speed": random.uniform(*normal_speed_range) if not speed_boost_active else random.uniform(*boosted_speed_range),
                "image": obj_type.get("image"),  # Pokud existuje obrázek, použij ho
                "color": obj_type.get("color", WHITE),  # Jinak použij barvu
                "effect": obj_type["effect"],
                "points": obj_type["points"]
            })

        if speed_boost_active:
            speed_boost_timer -= 1
            if speed_boost_timer <= 0:
                speed_boost_active = False
                for obj in falling_objects:
                    obj["speed"] = random.uniform(*normal_speed_range)

        for obj in falling_objects[:]:
            obj["y"] += obj["speed"]
            
            # Pokud má objekt obrázek, vykresli ho, jinak nakresli obdélník
            if obj["image"]:
                screen.blit(obj["image"], (obj["x"], obj["y"]))
            else:
                pygame.draw.rect(screen, obj["color"], (obj["x"], obj["y"], *object_size))

            if (obj["y"] + object_size[1] >= basket_y) and (obj["x"] >= basket_x and obj["x"] + object_size[0] <= basket_x + basket_width):
                if obj["effect"] == "normal" or obj["effect"] == "bonus":
                    score += obj["points"]
                elif obj["effect"] == "double":
                    score *= 2
                elif obj["effect"] == "bomb":
                    lives -= 1
                    if lives == 0:
                        return
                elif obj["effect"] == "speed_boost":
                    speed_boost_active = True
                    speed_boost_timer = 600  # 10 sekund (60 FPS * 10)
                    for existing_obj in falling_objects:
                        existing_obj["speed"] = random.uniform(*boosted_speed_range)
                falling_objects.remove(obj)

            if obj["y"] > HEIGHT:
                if obj["effect"] == "normal" or obj["effect"] == "bonus":
                    lives -= 1
                    if lives == 0:
                        return
                falling_objects.remove(obj)

        screen.blit(basket_image, (basket_x, basket_y))

        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))

        pygame.display.flip()
        frame_count += 1
        clock.tick(60)

game_loop()
