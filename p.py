import pygame
import random

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DND Battle Prototype")

title_font = pygame.font.SysFont("segoeuiemoji", 72)
button_font = pygame.font.SysFont("segoeuiemoji", 40)

game_state = "title"
selected_class = None

enemy_waiting = False
player_has_acted = False

start_button = pygame.Rect(350, 300, 200, 60)

classes = [
    {"name": "Barbarian", "emoji": "[B]", "hp": 140, "rect": pygame.Rect(170, 160, 220, 70)},
    {"name": "Wizard", "emoji": "[W]", "hp": 80, "rect": pygame.Rect(510, 160, 220, 70)},
    {"name": "Druid", "emoji": "[D]", "hp": 100, "rect": pygame.Rect(170, 340, 220, 70)},
    {"name": "Ranger", "emoji": "[R]", "hp": 90, "rect": pygame.Rect(510, 340, 220, 70)}
]

class_attacks = {
    "Barbarian": [
        {"name": "Slash", "damage": 10, "accuracy": 90, "crit_chance": 10},
        {"name": "Slam", "damage": 18, "accuracy": 65, "crit_chance": 20},
        {"name": "Pierce", "damage": 14, "accuracy": 80, "crit_chance": 15}
    ],
    "Wizard": [
        {"name": "Fireball", "damage": 12, "accuracy": 85, "crit_chance": 15},
        {"name": "Shock", "damage": 9, "accuracy": 95, "crit_chance": 5},
        {"name": "Ice Knife", "damage": 15, "accuracy": 75, "crit_chance": 20}
    ],
    "Druid": [
        {"name": "Vine Whip", "damage": 11, "accuracy": 90, "crit_chance": 10},
        {"name": "Nature Blast", "damage": 17, "accuracy": 70, "crit_chance": 20},
        {"name": "Root Strike", "damage": 12, "accuracy": 85, "crit_chance": 10}
    ],
    "Ranger": [
        {"name": "Arrow", "damage": 10, "accuracy": 95, "crit_chance": 10},
        {"name": "Ice Arrow", "damage": 13, "accuracy": 85, "crit_chance": 15},
        {"name": "Power Shot", "damage": 17, "accuracy": 65, "crit_chance": 25}
    ]
}

enemy_attacks = [
    {"name": "Claw", "damage": 8, "accuracy": 90, "crit_chance": 5},
    {"name": "Bite", "damage": 12, "accuracy": 70, "crit_chance": 10},
    {"name": "Stab", "damage": 22, "accuracy": 80, "crit_chance": 20}
]

player_max_hp = 100
enemy_max_hp = 100

enemy_name = "Goblin"
enemy_hp = 100

winner_text = ""

current_turn = "player"

player_log = ""
enemy_log = ""

running = True
while running:
    screen.fill((40, 40, 40))
    mouse_pos = pygame.mouse.get_pos()

    # ---------------- TITLE ----------------
    if game_state == "title":
        title_text = title_font.render("DnD RPG", True, (255, 255, 255))
        screen.blit(title_text, title_text.get_rect(center=(WIDTH // 2, 180)))

        button_colour = (100, 100, 100) if start_button.collidepoint(mouse_pos) else (70, 70, 70)

        pygame.draw.rect(screen, button_colour, start_button, border_radius=20)

        btn_text = button_font.render("Start", True, (255, 255, 255))
        screen.blit(btn_text, btn_text.get_rect(center=start_button.center))

    # ---------------- CLASS SELECT ----------------
    elif game_state == "class_select":

        title_text = title_font.render("Choose Your Class", True, (255, 255, 255))
        screen.blit(title_text, title_text.get_rect(center=(WIDTH // 2, 100)))

        for c in classes:
            rect = c["rect"]
            is_hovered = rect.collidepoint(mouse_pos)

            if is_hovered:
                draw_rect = pygame.Rect(rect.x - 15, rect.y - 10, rect.width + 30, rect.height + 20)
                colour = (110, 110, 110)
            else:
                draw_rect = rect
                colour = (80, 80, 80)

            pygame.draw.rect(screen, colour, draw_rect, border_radius=20)

            text = button_font.render(c["emoji"] + c["name"], True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=draw_rect.center))

    # ---------------- BATTLE ----------------
    elif game_state == "battle":

        # PLAYER
        player_text = title_font.render(selected_class, True, (255, 255, 255))
        screen.blit(player_text, (80, 80))

        pygame.draw.rect(screen, (80, 80, 80), (80, 170, 250, 30), border_radius=10)
        player_bar_width = (player_hp / player_max_hp) * 250
        pygame.draw.rect(screen, (50, 200, 50), (80, 170, player_bar_width, 30), border_radius=10)

        hp_text = button_font.render(str(player_hp) + " HP", True, (255, 255, 255))
        screen.blit(hp_text, hp_text.get_rect(center=(205, 185)))

        # ENEMY
        enemy_text = title_font.render(enemy_name, True, (255, 255, 255))
        screen.blit(enemy_text, enemy_text.get_rect(topright=(820, 80)))

        pygame.draw.rect(screen, (80, 80, 80), (570, 170, 250, 30), border_radius=10)
        enemy_bar_width = (enemy_hp / enemy_max_hp) * 250
        pygame.draw.rect(screen, (200, 50, 50), (570, 170, enemy_bar_width, 30), border_radius=10)

        enemy_hp_text = button_font.render(str(enemy_hp) + " HP", True, (255, 255, 255))
        screen.blit(enemy_hp_text, enemy_hp_text.get_rect(center=(695, 185)))

        # ---------------- ATTACK BUTTONS ----------------
        current_attacks = class_attacks[selected_class]

        for i, attack in enumerate(current_attacks):
            attack_rect = pygame.Rect(90 + i * 260, 500, 220, 60)

            color = (110, 110, 110) if attack_rect.collidepoint(mouse_pos) else (80, 80, 80)

            pygame.draw.rect(screen, color, attack_rect, border_radius=20)

            attack_text = button_font.render(attack["name"], True, (255, 255, 255))
            screen.blit(attack_text, attack_text.get_rect(center=attack_rect.center))

        # ---------------- LOGS (FIXED: ONLY ONCE) ----------------
        player_log_text = button_font.render(player_log, True, (255, 255, 255))
        enemy_log_text = button_font.render(enemy_log, True, (255, 255, 255))

        screen.blit(player_log_text, (WIDTH // 2 - player_log_text.get_width() // 2, 410))
        screen.blit(enemy_log_text, (WIDTH // 2 - enemy_log_text.get_width() // 2, 460))

        # ---------------- ENEMY TURN ----------------
        if enemy_waiting and current_turn == "enemy":
            if pygame.time.get_ticks() - enemy_start_time > 600:

                attack = random.choice(enemy_attacks)
                hit_roll = random.randint(1, 100)

                if hit_roll <= attack["accuracy"]:
                    damage = attack["damage"]
                    if random.randint(1, 100) <= attack["crit_chance"]:
                        damage *= 2
                        enemy_log = "Enemy CRIT with " + attack["name"]
                    else:
                        enemy_log = "Enemy used " + attack["name"]

                    player_hp = max(0, player_hp - damage)
                else:
                    enemy_log = "Enemy missed!"

                enemy_waiting = False
                current_turn = "player"
                player_has_acted = False

    # ---------------- EVENTS ----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_state == "title" and start_button.collidepoint(event.pos):
                game_state = "class_select"

            elif game_state == "class_select":
                for c in classes:
                    if c["rect"].collidepoint(event.pos):
                        selected_class = c["name"]
                        player_max_hp = c["hp"]
                        player_hp = player_max_hp
                        game_state = "battle"

            elif game_state == "battle":

                if current_turn == "player" and not player_has_acted:

                    for i, attack in enumerate(class_attacks[selected_class]):
                        attack_rect = pygame.Rect(90 + i * 260, 500, 220, 60)

                        if attack_rect.collidepoint(event.pos):

                            hit_roll = random.randint(1, 100)

                            if hit_roll <= attack["accuracy"]:
                                damage = attack["damage"]

                                if random.randint(1, 100) <= attack["crit_chance"]:
                                    damage *= 2
                                    player_log = attack["name"] + " CRIT for " + str(damage)
                                else:
                                    player_log = attack["name"] + " hit for " + str(damage)

                                enemy_hp = max(0, enemy_hp - damage)
                            else:
                                player_log = attack["name"] + " MISSED!"

                            player_has_acted = True
                            current_turn = "enemy"
                            enemy_waiting = True
                            enemy_start_time = pygame.time.get_ticks()

    pygame.display.flip()

pygame.quit()