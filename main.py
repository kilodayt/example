import pygame
import random

# Настройки окна
WIDTH = 500
HEIGHT = 500
FPS = 60

# Цвета
YELLOW = (255, 255, 0)
SKY = (133, 193, 233)
GREEN = (46, 204, 113)
WHITE = (255, 255, 255)

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Настройки персонажа
bird = pygame.Rect(40, 250, 30, 23)
birdImg = pygame.image.load('fpbs1.png')
points = 0

# Шрифты
font = pygame.font.SysFont('comic sans ms', 30)
game_over_font = pygame.font.SysFont('comic sans ms', 50)
game_over_text = game_over_font.render('GAME OVER', 1, WHITE)

# Падение
GRAVITY = 0.3
y_change = 0

# Прыжок
isJump = False
jumpCount = 10

# Трубы
pipes = []
pipecd = 1500

# Очки
check = []

# Время
currentTime = 0
lastPipeTime = 0

game_over = False
running = True
while running:
    screen.fill(SKY)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE:
                isJump = True
                hopCount = 0
    # Прыжок
    if isJump:
        hopCount += 1
        bird.top -= 6
        if hopCount == 5:
            y_change = 0
            isJump = False
    # Падение
    else:
        y_change += GRAVITY
        bird.top += y_change

    # Текущее время
    currentTime = pygame.time.get_ticks()
    # Генерация труб
    if currentTime - lastPipeTime > pipecd:
        widthPipe = 40

        # Верхняя труба
        heightUpPipe = random.randint(50, 400)
        upPipe = pygame.Rect(WIDTH, 0, widthPipe, heightUpPipe)

        # Нижняя труба
        yDownPipe = heightUpPipe + 100
        heightDownPipe = HEIGHT - yDownPipe
        downPipe = pygame.Rect(WIDTH, yDownPipe, widthPipe, heightDownPipe)

        # Промежуток между трубами
        yMiddle = heightUpPipe
        heightMiddle = HEIGHT - heightUpPipe - heightDownPipe
        middle = pygame.Rect(WIDTH, yMiddle, widthPipe, heightMiddle)
        check.append(middle)

        pipes.append((upPipe, downPipe))

        lastPipeTime = currentTime
        pipecd = random.randint(1500, 2000)

    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe[0])
        pygame.draw.rect(screen, GREEN, pipe[1])

        pipe[0].left -= 2
        pipe[1].left -= 2

    for pipe in pipes:
        up_pipe = pipe[0]
        down_pipe = pipe[1]

        if bird.colliderect(up_pipe):
            game_over = True
        elif bird.colliderect(down_pipe):
            game_over = True

    for flag in check:
        flag.left -= 2
        if bird.colliderect(flag):
            points += 1
            check.remove(flag)

    # Столкновение
    # Столкновение птички с краями окна игры
    if bird.top < 0 or bird.bottom > HEIGHT:
        game_over = True

    screen.blit(birdImg, (bird.left, bird.top))
    pointsText = font.render(str(points), True, WHITE)
    screen.blit(pointsText, (245, 245))

    if game_over:
        screen.fill(SKY)
        screen.blit(game_over_text, (80, 120))

    clock.tick(FPS)
    pygame.display.update()
pygame.quit()
