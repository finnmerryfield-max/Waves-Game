import pygame, math, random

pygame.init()
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Waves")
clock = pygame.time.Clock()


A = 77
K = 0.008
speed = 5
offset = 0

x_player = 100
ball_radius = 25
angle = 0

y_vel = 0
jumping = False
gravity = 0.5
jump_strength = -12

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    offset += speed
    screen.fill((18, 52, 86))

    points = []
    for x in range(W + 1):
        y = H // 1.4 + A * math.sin(K * (x + offset))
        points.append((x, y))

    points.append((W, H,))
    points.append((0, H))
    pygame.draw.polygon(screen, (60, 120, 200), points)
    pygame.draw.lines(screen, (150, 220, 255), False, points[:-2], 4)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not jumping:
        y_vel = jump_strength
        jumping = True

    wave_y = H // 1.4 + A * math.sin(K * (x_player + offset))
    if jumping:
        y_player += y_vel
        y_vel += gravity

        if y_player >= wave_y - ball_radius:
            y_player = wave_y - ball_radius
            jumping = False
            y_vel = 0

    else:
        y_player = wave_y - ball_radius
    
    slope = A * K * math.cos(K * (x_player + offset))
    angle = -math.degrees(math.atan(slope))

    center = (x_player, y_player)
    ball_surface = pygame.Surface((ball_radius*2, ball_radius*2), pygame.SRCALPHA)

    pygame.draw.circle(ball_surface, (80, 200, 255), (ball_radius, ball_radius), ball_radius)
    
    for i in range(6):
        radius = 10 - i
        highlight_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(highlight_surface, (200, 255, 255), (radius, radius), radius)
        highlight_surface.set_alpha(120 - i*20)
        ball_surface.blit(highlight_surface, (ball_radius-6-radius, ball_radius-8-radius))

    rotated_ball = pygame.transform.rotate(ball_surface, angle)
    rect = rotated_ball.get_rect(center=center)
    screen.blit(rotated_ball, rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()