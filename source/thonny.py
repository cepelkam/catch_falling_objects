import pygame
import random
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch Falling Objects")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont(None, 36)

# Načtení obrázků
basket_image = pygame.image.load("basket.png")
apple_image = pygame.image.load("apple.png")
pineapple_image = pygame.image.load("pineapple.png")
rotten_pineapple_image = pygame.image.load("rotten_pineapple.png")
green_apple_image = pygame.image.load("green_apple.png")

# Úprava velikosti obrázků
object_size = (30, 30)
apple_image = pygame.transform.scale(apple_image, object_size)
pineapple_image = pygame.transform.scale(pineapple_image, object_size)
rotten_pineapple_image = pygame.transform.scale(rotten_pineapple_image, object_size)
green_apple_image = pygame.transform.scale(green_apple_image, object_size)

basket_width = basket_image.get_width()
basket_height = basket_image.get_height()

# Highscore soubor
highscore_file = "highscores.txt"
if not os.path.exists(highscore_file):
    with open(highscore_file, "w") as f:
        f.write("Name: Score\n")

def load_highscores():
    with open(highscore_file, "r") as f:
        return [line.strip() for line in f.readlines()[1:]]  # Přeskakuju první řádek s nadpisem

def save_highscores(name, score):
    highscores = load_highscores()
    highscores.append(f"{name}: {score}")
    highscores = sorted(highscores, key=lambda x: int(x.split(": ")[1]), reverse=True)[:5]  # Uchováme pouze top 5
    with open(highscore_file, "w") as f:
        f.write("Name: Score\n")
        for entry in highscores:
            f.write(f"{entry}\n")

def show_menu():
    screen.fill(BLACK)
    title = font.render("Catch Falling Objects", True, WHITE)
    start_text = font.render("Press SPACE to Start", True, WHITE)
    quit_text = font.render("Press ESC to Quit", True, WHITE)
    control_text = font.render("Move with ARROWS", True, WHITE)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 40))
    screen.blit(control_text, (WIDTH // 2 - control_text.get_width() // 2, HEIGHT // 2 + 80))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def show_highscores():
    screen.fill(BLACK)
    title = font.render("Highscores", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))

    highscores = load_highscores()
    for i, score in enumerate(highscores):
        score_text = font.render(f"{i + 1}. {score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3 + (i + 1) * 40))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

def get_player_name():
    name = ""
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = font.render(name, True, WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        screen.fill(BLACK)
        title = font.render("Enter Your Name", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        
        pygame.draw.rect(screen, color, input_box, 2)
        text = font.render(name, True, WHITE)
        screen.blit(text, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()

def game_over_screen(score, player_name):
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    player_name_text = font.render(f"Player: {player_name}", True, WHITE)
    restart_text = font.render("Press SPACE to Play Again", True, WHITE)
    quit_text = font.render("Press ESC to Quit", True, WHITE)
    
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(player_name_text, (WIDTH // 2 - player_name_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 80))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    save_highscores(player_name, score)
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def game_loop(player_name):
    basket_x = (WIDTH - basket_width) // 2
    basket_y = HEIGHT - basket_height - 10
    basket_speed = 8

    falling_objects = []

    object_weights = {
        "apple": 50,
        "rotten_pineapple": 20,
        "pineapple": 15,
        "green_apple": 10
    }

    object_types = [
        {"image": apple_image, "effect": "normal", "points": 1},
        {"image": rotten_pineapple_image, "effect": "bomb", "points": 0},
        {"image": pineapple_image, "effect": "bonus", "points": 2},
        {"image": green_apple_image, "effect": "double", "points": 0}
    ]

    weights = list(object_weights.values())

    score = 0
    lives = 3
    current_speed = 2.0

    running = True
    clock = pygame.time.Clock()
    spawn_rate = 50
    frame_count = 0
    max_objects = 6

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
            obj_type = random.choices(object_types, weights=weights)[0]
            falling_objects.append({
                "x": random.randint(0, WIDTH - object_size[0]),
                "y": random.randint(-100, -50),
                "speed": current_speed,
                "image": obj_type["image"],
                "effect": obj_type["effect"],
                "points": obj_type["points"]
            })

        for obj in falling_objects[:]:
            obj["y"] += obj["speed"]

            screen.blit(obj["image"], (obj["x"], obj["y"]))

            if (obj["y"] + object_size[1] >= basket_y) and (obj["x"] >= basket_x and obj["x"] + object_size[0] <= basket_x + basket_width):
                if obj["effect"] == "normal" or obj["effect"] == "bonus":
                    score += obj["points"]
                elif obj["effect"] == "double":
                    score *= 2
                elif obj["effect"] == "bomb":
                    lives -= 1
                    if lives == 0:
                        game_over_screen(score, player_name)
                        return
                falling_objects.remove(obj)

            if obj["y"] > HEIGHT:
                if obj["effect"] in ["normal", "bonus"]:
                    lives -= 1
                    if lives == 0:
                        game_over_screen(score, player_name)
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

        current_speed += 0.0005

def main():
    while True:
        show_menu()
        player_name = get_player_name()
        game_loop(player_name)

main()
