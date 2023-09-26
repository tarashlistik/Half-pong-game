import pygame
from random import randint

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

WIDTH, HEIGHT = 860, 540
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("half pong")
clock = pygame.time.Clock()

pygame.mixer.music.load("Sounds/Epic_music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
catch = pygame.mixer.Sound("Sounds/catch.ogg")
music_game_over = pygame.mixer.Sound("Sounds/Game Over (online-audio-converter.com).ogg")

PLATFORM_WIDTH = 120
PLATFORM_HEIGHT = 15
SPEED_PLATFORM = 10
platform_rect = pygame.rect.Rect(WIDTH // 2 - PLATFORM_WIDTH / 2,
                                 HEIGHT - PLATFORM_HEIGHT * 2,
                                 PLATFORM_WIDTH,
                                 PLATFORM_HEIGHT)

BOTTOM_TOP_LINE = HEIGHT-5
bottom_line_rect = pygame.rect.Rect(0, BOTTOM_TOP_LINE, WIDTH, HEIGHT)
first_collide_line = False

circle_first_collide = False
CIRCLE_RADIUS = 15
CIRCLE_SPEED = 10
circle_speed_x = 0
circle_speed_y = CIRCLE_SPEED
circle_rect = pygame.rect.Rect(WIDTH // 2 - CIRCLE_RADIUS,
                               HEIGHT // 2 - CIRCLE_RADIUS,
                               CIRCLE_RADIUS * 2,
                               CIRCLE_RADIUS * 2)

score = 0

ARIAL_FOND_PATH = pygame.font.match_font("alial")
ARIAL_FOND_60 = pygame.font.Font(ARIAL_FOND_PATH, 60)
ARIAL_FOND_54 = pygame.font.Font(ARIAL_FOND_PATH, 54)

game_over = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_over = False
                score = 0
                circle_first_collide = False
                platform_rect.centerx = WIDTH // 2
                circle_rect.center = [WIDTH // 2, HEIGHT // 2]
                circle_speed_x = 0
                circle_speed_y = CIRCLE_SPEED
                CIRCLE_SPEED = 10
                pygame.mixer.music.play(-1)
                first_collide_line = False

    screen.fill(BLACK)

    if not game_over:

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            platform_rect.x -= SPEED_PLATFORM
            if platform_rect.x < 0:
                platform_rect.x = 0
        if keys[pygame.K_RIGHT]:
            platform_rect.x += SPEED_PLATFORM
            if platform_rect.x > WIDTH-platform_rect.width:
                platform_rect.x = WIDTH-platform_rect.width

        if platform_rect.colliderect(circle_rect):
            if not circle_first_collide:
                if randint(0, 1) == 0:
                    circle_speed_x = CIRCLE_SPEED
                else:
                    circle_speed_x = -CIRCLE_SPEED
                circle_first_collide = True
            score += 1
            if score > 10:
                CIRCLE_SPEED += 0.1
            circle_speed_y = -CIRCLE_SPEED
            catch.play()

        pygame.draw.rect(screen, WHITE, platform_rect)
        pygame.draw.rect(screen, WHITE, bottom_line_rect)

    circle_rect.x += circle_speed_x
    circle_rect.y += circle_speed_y

    if circle_rect.bottom >= HEIGHT:
        pygame.mixer.music.stop()
        game_over = True
        circle_speed_y = -CIRCLE_SPEED
    if circle_rect.top <= 0:
        circle_speed_y = CIRCLE_SPEED
    if circle_rect.left <= 0:
        circle_speed_x = CIRCLE_SPEED
    if circle_rect.right >= WIDTH:
        circle_speed_x = -CIRCLE_SPEED

    pygame.draw.circle(screen, WHITE, circle_rect.center, CIRCLE_RADIUS)
    score_surface = ARIAL_FOND_54.render(str(score), True, WHITE)
    if not game_over:
        screen.blit(score_surface, [0, 15])
    else:
        retry_surface = ARIAL_FOND_60.render("press R to restart", True, WHITE)
        screen.blit(score_surface, [WIDTH // 2, HEIGHT // 3])
        screen.blit(retry_surface, [WIDTH // 2 - retry_surface.get_width() // 2, HEIGHT // 2])
        if not first_collide_line:
            music_game_over.play()
        first_collide_line = True
    pygame.display.update()

    clock.tick(FPS)