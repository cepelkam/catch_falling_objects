import pygame
import random
import os

pygame.init()

WIDTH, HEIGHT = 1100, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chytání padajících objektů")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
ORANGE = (255, 165, 0)
GREEN = (50, 205, 50)

font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 60)

basket_image = pygame.image.load("basket.png")
apple_image = pygame.image.load("apple.png")
pineapple_image = pygame.image.load("pineapple.png")
rotten_pineapple_image = pygame.image.load("rotten_pineapple.png")
green_apple_image = pygame.image.load("green_apple.png")

object_size = (30, 30)
apple_image = pygame.transform.scale(apple_image, object_size)
pineapple_image = pygame.transform.scale(pineapple_image, object_size)
rotten_pineapple_image = pygame.transform.scale(rotten_pineapple_image, object_size)
green_apple_image = pygame.transform.scale(green_apple_image, object_size)

basket_width = basket_image.get_width()
basket_height = basket_image.get_height()

highscore_file = "highscores.txt"
if not os.path.exists(highscore_file):
    with open(highscore_file, "w") as f:
        f.write("Jméno: Skóre\n")

def load_highscores():
    try:
        if not os.path.exists(highscore_file):
            with open(highscore_file, "w") as f:
                f.write("Jméno: Skóre\n")
            return []
            
        with open(highscore_file, "r") as f:
            lines = [line.strip() for line in f.readlines()[1:]]  
            valid_lines = []
            for line in lines:
                parts = line.split(": ")
                if len(parts) == 2 and parts[1].isdigit():
                    valid_lines.append(line)
            return valid_lines
    except Exception as e:
        print(f"Chyba při načítání skóre: {e}")
        return []

def save_highscores(name, score):
    try:
        highscores = load_highscores()
        highscores.append(f"{name}: {score}")
        highscores = sorted(highscores, key=lambda x: int(x.split(": ")[1]) if len(x.split(": ")) > 1 else 0, reverse=True)[:5]  # Uchováme pouze top 5
        with open(highscore_file, "w") as f:
            f.write("Jméno: Skóre\n")
            for entry in highscores:
                f.write(f"{entry}\n")
    except Exception as e:
        print(f"Chyba při ukládání skóre: {e}")

def draw_button(text, x, y, width, height, inactive_color, active_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1:
            pygame.time.delay(200)
            return True
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
    
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=((x + width/2), (y + height/2)))
    screen.blit(text_surf, text_rect)
    return False

def show_menu():
    menu_running = True
    
    while menu_running:
        screen.fill(BLACK)
        
        title = title_font.render("Chytání padajících objektů", True, ORANGE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        
        info_text = font.render("Chytej ovoce a vyhýbej se shnilým ananasům!", True, WHITE)
        screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, HEIGHT // 4 + 60))
        
        button_width, button_height = 200, 50
        button_x = WIDTH // 2 - button_width // 2
        
        controls_text = font.render("Ovládání: Šipky vlevo/vpravo", True, WHITE)
        screen.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT // 4 + 100))
        
        legend_y = HEIGHT // 4 + 140
        legend_items = [
            (apple_image, "Jablko: +1 bod"),
            (pineapple_image, "Ananas: +2 body"),
            (green_apple_image, "Zelené jablko: zdvojnásobí skóre"),
            (rotten_pineapple_image, "Shnilý ananas: -1 život")
        ]
        
        for i, (img, text) in enumerate(legend_items):
            screen.blit(img, (WIDTH // 2 - 150, legend_y + i * 30))
            item_text = font.render(text, True, WHITE)
            screen.blit(item_text, (WIDTH // 2 - 100, legend_y + i * 30))
        
        if draw_button("HRÁT", button_x, HEIGHT * 0.65, button_width, button_height, GREEN, (100, 255, 100)):
            return "play"
        
        if draw_button("ŽEBŘÍČEK", button_x, HEIGHT * 0.65 + 70, button_width, button_height, BLUE, (100, 100, 255)):
            show_highscores()
        
        if draw_button("KONEC", button_x, HEIGHT * 0.65 + 140, button_width, button_height, (200, 50, 50), (255, 100, 100)):
            pygame.quit()
            exit()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "play"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                    
        pygame.display.flip()

def show_highscores():
    back_to_menu = False
    
    while not back_to_menu:
        screen.fill(BLACK)
        title = title_font.render("Žebříček nejlepších", True, ORANGE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

        highscores = load_highscores()
        
        table_width, table_height = 400, 300
        table_x, table_y = WIDTH // 2 - table_width // 2, HEIGHT // 3 + 50
        
        pygame.draw.rect(screen, (50, 50, 50), (table_x, table_y, table_width, table_height))
        pygame.draw.rect(screen, WHITE, (table_x, table_y, table_width, table_height), 2)
        
        header = font.render("Pořadí     Jméno     Skóre", True, WHITE)
        screen.blit(header, (table_x + table_width // 2 - header.get_width() // 2, table_y + 10))
        
        pygame.draw.line(screen, WHITE, (table_x, table_y + 50), (table_x + table_width, table_y + 50), 2)
        
        if len(highscores) == 0:
            no_scores = font.render("Zatím žádné skóre!", True, WHITE)
            screen.blit(no_scores, (table_x + table_width // 2 - no_scores.get_width() // 2, table_y + 100))
        else:
            for i, score in enumerate(highscores):
                try:
                    parts = score.split(": ")
                    if len(parts) != 2:
                        continue
                    name, points = parts
                    score_text = font.render(f"{i + 1}.         {name}         {points}", True, WHITE)
                    screen.blit(score_text, (table_x + table_width // 2 - score_text.get_width() // 2, table_y + 70 + i * 40))
                except Exception as e:
                    print(f"Chyba při zobrazení řádku žebříčku: {e}")
                    continue

        button_width, button_height = 200, 50
        button_x = WIDTH // 2 - button_width // 2
        
        if draw_button("ZPĚT DO MENU", button_x, table_y + table_height + 30, button_width, button_height, BLUE, (100, 100, 255)):
            back_to_menu = True
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    back_to_menu = True
                    
        pygame.display.flip()

def get_player_name():
    name = ""
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 40)
    color_inactive = BLUE
    color_active = (100, 100, 255)
    color = color_inactive
    active = False
    text = font.render(name, True, WHITE)

    screen.fill(BLACK)
    title = title_font.render("Zadej své jméno", True, ORANGE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if name.strip() == "":
                            name = "Hráč"
                        return name
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 10:
                            name += event.unicode

        screen.fill(BLACK)
        title = title_font.render("Zadej své jméno", True, ORANGE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        
        instruction = font.render("Zadej své jméno a stiskni Enter", True, WHITE)
        screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT // 3 + 70))
        
        pygame.draw.rect(screen, color, input_box, 2)
        
        pygame.draw.rect(screen, (50, 50, 50), (input_box.x, input_box.y, input_box.width, input_box.height))
        
        text = font.render(name, True, WHITE)
        screen.blit(text, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()

def game_over_screen(score, player_name):
    try:
        save_highscores(player_name, score)
        
        while True:
            try:
                screen.fill(BLACK)
                game_over_text = title_font.render("KONEC HRY", True, (255, 50, 50))
                score_text = font.render(f"Skóre: {score}", True, WHITE)
                player_name_text = font.render(f"Hráč: {player_name}", True, WHITE)
                
                screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
                screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 20))
                screen.blit(player_name_text, (WIDTH // 2 - player_name_text.get_width() // 2, HEIGHT // 2))
                
                highscores = load_highscores()
                
                table_title = font.render("Nejlepší výsledky", True, ORANGE)
                screen.blit(table_title, (WIDTH // 2 - table_title.get_width() // 2, HEIGHT // 2 + 40))
                
                table_width, table_height = 300, 200
                table_x, table_y = WIDTH // 2 - table_width // 2, HEIGHT // 2 + 80
                
                pygame.draw.rect(screen, (50, 50, 50), (table_x, table_y, table_width, table_height))
                pygame.draw.rect(screen, WHITE, (table_x, table_y, table_width, table_height), 2)
                
                if len(highscores) == 0:
                    no_scores = font.render("Zatím žádné skóre!", True, WHITE)
                    screen.blit(no_scores, (table_x + table_width // 2 - no_scores.get_width() // 2, table_y + 80))
                else:
                    for i, score_entry in enumerate(highscores[:5]):  
                        try:
                            parts = score_entry.split(": ")
                            if len(parts) != 2:
                                continue
                                
                            name, points = parts
                            if name == player_name and int(points) == score:
                                score_entry_text = font.render(f"{i + 1}. {name}: {points}", True, (255, 255, 0))
                            else:
                                score_entry_text = font.render(f"{i + 1}. {name}: {points}", True, WHITE)
                            screen.blit(score_entry_text, (table_x + 20, table_y + 20 + i * 30))
                        except Exception as e:
                            print(f"Chyba při vykreslování položky skóre: {e}")
                            continue
                
                button_width, button_height = 200, 50
                button_x = WIDTH // 2 - button_width // 2
                
                play_again = draw_button("HRÁT ZNOVU", button_x, table_y + table_height + 20, button_width, button_height, GREEN, (100, 255, 100))
                back_to_menu = draw_button("ZPĚT DO MENU", button_x, table_y + table_height + 80, button_width, button_height, BLUE, (100, 100, 255))
                
                if play_again:
                    return "play_again"
                    
                if back_to_menu:
                    return "menu"

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            return "play_again"
                        if event.key == pygame.K_ESCAPE:
                            return "menu"
                            
                pygame.display.flip()
                pygame.time.delay(30) 
                
            except Exception as e:
                print(f"Chyba na obrazovce 'game over': {e}")
                return "menu"  
    except Exception as e:
        print(f"Kritická chyba v game_over_screen: {e}")
        return "menu"

def game_loop(player_name):
    basket_x = (WIDTH - basket_width) // 2
    basket_y = HEIGHT - basket_height - 10
    basket_speed = 8

    falling_objects = []

    object_weights = {
        "apple": 30,
        "rotten_pineapple": 10,
        "pineapple": 6,
        "green_apple": 1
    }

    object_types = [
        {"image": apple_image, "effect": "normal", "points": 1, "name": "Jablko"},
        {"image": rotten_pineapple_image, "effect": "bomb", "points": 0, "name": "Shnilý ananas"},
        {"image": pineapple_image, "effect": "bonus", "points": 2, "name": "Ananas"},
        {"image": green_apple_image, "effect": "double", "points": 0, "name": "Zelené jablko"}
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
    
    last_caught = None
    caught_timer = 0

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
                "points": obj_type["points"],
                "name": obj_type["name"]
            })

        for obj in falling_objects[:]:
            obj["y"] += obj["speed"]

            screen.blit(obj["image"], (obj["x"], obj["y"]))

            basket_collision = (obj["y"] + object_size[1] >= basket_y and 
                             obj["y"] <= basket_y + basket_height and
                             obj["x"] + object_size[0] >= basket_x and 
                             obj["x"] <= basket_x + basket_width)
                             
            if basket_collision:
                if obj["effect"] == "normal" or obj["effect"] == "bonus":
                    score += obj["points"]
                    last_caught = f"+{obj['points']} ({obj['name']})"
                    caught_timer = 60  
                elif obj["effect"] == "double":
                    old_score = score
                    score *= 2
                    last_caught = f"x2! ({obj['name']}) {old_score} → {score}"
                    caught_timer = 60
                elif obj["effect"] == "bomb":
                    lives -= 1
                    last_caught = f"-1 život ({obj['name']})"
                    caught_timer = 60
                    if lives == 0:
                        result = game_over_screen(score, player_name)
                        return result
                falling_objects.remove(obj)
                continue

            if obj["y"] > HEIGHT:
                if obj["effect"] in ["normal", "bonus"]:
                    lives -= 1
                    if lives == 0:
                        result = game_over_screen(score, player_name)
                        return result
                falling_objects.remove(obj)

        screen.blit(basket_image, (basket_x, basket_y))

        score_text = font.render(f"Skóre: {score}", True, WHITE)
        lives_text = font.render(f"Životy: {lives}", True, WHITE)
        player_text = font.render(f"Hráč: {player_name}", True, WHITE)

        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(player_text, (10, 90))
        
        if caught_timer > 0:
            info_text = font.render(last_caught, True, ORANGE)
            screen.blit(info_text, (WIDTH - info_text.get_width() - 10, 10))
            caught_timer -= 1

        pygame.display.flip()
        frame_count += 1
        clock.tick(60)

        if frame_count % 300 == 0:  
            current_speed += 0.2
            if spawn_rate > 30:
                spawn_rate -= 1
            if max_objects < 10:
                max_objects += 0.5

def main():
    player_name = None
    
    while True:
        action = show_menu()
        
        if action == "play":
            if not player_name:
                player_name = get_player_name()
            
            result = game_loop(player_name)
            
            if result == "play_again":
                continue
            
main()