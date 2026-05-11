import pygame

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DND Battle Prototype")
title_font = pygame.font.SysFont("segoeuiemoji", 72)
button_font = pygame.font.SysFont("segoeuiemoji", 40)

game_state =  "title"
selected_class = None

start_button = pygame.Rect(350, 300, 200, 60)

classes = [
    {
        "name": "Barbarian",
        "emoji": "[B]",
        "hp": 140,
        "rect": pygame.Rect(170, 160, 220, 70)
    },
    {
        "name": "Wizard",
        "emoji": "[W]",
        "hp": 80,
        "rect": pygame.Rect(510, 160, 220, 70)
    },
    {
        "name": "Druid",
        "emoji": "[D]",
        "hp": 100,
        "rect": pygame.Rect(170, 340, 220, 70)
    },
    {
        "name": "Ranger",
        "emoji": "[R]",
        "hp": 90,
        "rect": pygame.Rect(510, 340, 220, 70)
    }
]

player_max_hp = 100
enemy_max_hp = 100

enemy_name = "Goblin"
enemy_hp = 100

attack_button = pygame.Rect(320, 500, 260, 60)

winner_text = ""

current_turn = "player"

battle_message = ""

running = True
while running:
    screen.fill((40, 40, 40))
    mouse_pos = pygame.mouse.get_pos()

    if game_state == "title":

        title_text = title_font.render("DnD RPG", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, 180))
        screen.blit(title_text, title_rect)

        button_colour = (70, 70, 70)
        button_rect = start_button

        if start_button.collidepoint(mouse_pos):
            button_colour = (100, 100, 100)

            button_rect = pygame.Rect(
                start_button.x - 10,
                start_button.y - 5,
                start_button.width + 20,
                start_button.height + 10
            )

        pygame.draw.rect(screen, button_colour, button_rect, border_radius=20)

        button_text = button_font.render("Start", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, button_text_rect)

    elif game_state == "class_select":

        title_text = title_font.render("Choose Your Class", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        for c in classes:

            rect = c["rect"]

            is_hovered = rect.collidepoint(mouse_pos)

            if is_hovered:
                draw_rect = pygame.Rect(
                    rect.x - 15,
                    rect.y - 10,
                    rect.width + 30,
                    rect.height + 20
                )
                colour = (110, 110, 110)

            else:
                draw_rect = rect
                colour = (80, 80, 80)

            pygame.draw.rect(screen, colour, draw_rect, border_radius=20)

            text = button_font.render(
                c["emoji"] + "" + c["name"],
                True,
                (255, 255, 255)
            )

            text_rect = text.get_rect(center=draw_rect.center)

            screen.blit(text, text_rect)

    elif game_state == "battle":

        # PLAYER SECTION
    
        player_text = title_font.render(
            selected_class,
            True,
            (255,255,255)
        )
    
        screen.blit(player_text, (80, 80))
    
        # PLAYER HP BAR
    
        pygame.draw.rect(screen, (80,80,80), (80, 170, 250, 30), border_radius=10)
    
        player_bar_width = (player_hp / player_max_hp) * 250

        pygame.draw.rect(
            screen,
            (50, 200, 50),
            (80, 170, player_bar_width, 30),
            border_radius = 10
        )
    
        hp_text = button_font.render(
            str(player_hp) + " HP",
            True,
            (255,255,255)
        )

        hp_rect = hp_text.get_rect(center=(205, 185))
    
        screen.blit(hp_text, hp_rect)
    
        # ENEMY SECTION
    
        enemy_text = title_font.render(
            enemy_name,
            True,
            (255,255,255)
        )
    
        enemy_rect = enemy_text.get_rect(topright=(820, 80))
    
        screen.blit(enemy_text, enemy_rect)
    
        # ENEMY HP BAR
    
        pygame.draw.rect(screen, (80,80,80), (570, 170, 250, 30), border_radius=10)
    
        enemy_bar_width = (enemy_hp / enemy_max_hp) * 250
        
        pygame.draw.rect(
            screen,
            (200,50,50),
            (570, 170, enemy_bar_width, 30),
            border_radius=10
        )
    
        enemy_hp_text = button_font.render(
            str(enemy_hp) + " HP",
            True,
            (255,255,255)
        )

        enemy_hp_rect = enemy_hp_text.get_rect(center=(695, 185))
        
        screen.blit(enemy_hp_text, enemy_hp_rect)

        # ATTACK BUTTON

        attack_color = (80,80,80)
        
        if attack_button.collidepoint(mouse_pos):
            attack_color = (110,110,110)
        
        pygame.draw.rect(
            screen,
            attack_color,
            attack_button,
            border_radius=20
        )
        
        attack_text = button_font.render(
            "Attack",
            True,
            (255,255,255)
        )
        
        attack_text_rect = attack_text.get_rect(
            center=attack_button.center
        )
        
        screen.blit(attack_text, attack_text_rect)

        if winner_text != "":

            win_text = title_font.render(
                winner_text,
                True,
                (255, 255, 0)
            )

            win_rect = win_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2)
            )

            screen.blit(win_text, win_rect)

        message_text = button_font.render(
            battle_message,
            True,
            (255, 255, 255)
        )

        message_rect = message_text.get_rect(
            center=(WIDTH // 2, 440)
        )

        screen.blit(message_text, message_rect)

        if current_turn == "enemy" and enemy_hp > 0:
            pygame.display.flip()
            pygame.time.delay(600)
            player_hp -= 8
            player_hp = max(0, player_hp)
            battle_message = "Goblin Hits You"
            current_turn = "player"

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_state == "title":

                if start_button.collidepoint(event.pos):
                    game_state = "class_select"
                    pygame.time.delay(150)

            if game_state == "class_select":

                for c in classes:

                    if c["rect"].collidepoint(event.pos):

                        selected_class = c["name"]

                        player_max_hp = c["hp"]
                        player_hp = player_max_hp

                        game_state = "battle"

            if game_state == "battle":

                if attack_button.collidepoint(event.pos):

                    if current_turn == "player":
                        enemy_hp -= 13
                        enemy_hp = max(0, enemy_hp)
                        battle_message = "You Hit Goblin"
                        if enemy_hp == 0:
                            winner_text = "You Win"
                        else:
                            current_turn = "enemy"
    
    pygame.display.flip()

pygame.quit()