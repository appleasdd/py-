import pygame
import sys

# 初始化 Pygame
pygame.init()

# 設定遊戲視窗大小
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# 設定顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#載入背景畫面:
background = pygame.image.load("background.jpg")  # 替換成你的背景圖片路徑

# 設定球和板的初始位置和速度
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
ball_speed = [5, 5]

paddle1 = pygame.Rect(10, HEIGHT // 2 - 60, 10, 120)
paddle2 = pygame.Rect(WIDTH - 20, HEIGHT // 2 - 60, 10, 120)
paddle_speed = 10

#設定分數
score1 = 0
score2 = 0

#字型設計
font = pygame.font.SysFont('arial', 36)

#設定一條線
middle_line = pygame.Rect(WIDTH // 2 - 2, 0, 4, HEIGHT)

# 遊戲迴圈
clock = pygame.time.Clock()

# 設定倒計時
countdown = 3  # 設定倒計時秒數
countdown_font = pygame.font.SysFont('arial', 100)

#設定倒計時:
countdown = 6000

while countdown > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # 控制玩家1的板
    if keys[pygame.K_w] and paddle1.top > 0:
        paddle1.y -= paddle_speed
    if keys[pygame.K_s] and paddle1.bottom < HEIGHT:
        paddle1.y += paddle_speed
    '''if keys[pygame.K_a] and paddle1.left > 10:
        paddle1.x -= paddle_speed
    if keys[pygame.K_d] and paddle1.right < 400:
        paddle1.x += paddle_speed'''
    # 控制玩家2的板
    if keys[pygame.K_UP] and paddle2.top > 0:
        paddle2.y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle2.bottom < HEIGHT:
        paddle2.y += paddle_speed
    '''if keys[pygame.K_LEFT] and paddle2.left > 400:
        paddle2.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle2.right < WIDTH - 10:
        paddle2.x += paddle_speed'''

    # 移動球
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # 碰撞檢測
    if ball.top < 0 or ball.bottom > HEIGHT:
        ball_speed[1] = -ball_speed[1]

    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball_speed[0] = -ball_speed[0]

    # 球越過左邊界
    if ball.left <= 0:
        score2 += 1
        ball.x = WIDTH // 2 - 15
        ball_speed[0] = -ball_speed[0]

    # 球越過右邊界
    if ball.right >= WIDTH:
        score1 += 1
        ball.x = WIDTH // 2 - 15
        ball_speed[0] = -ball_speed[0]

    # 判斷勝負
    if score1 > score2:
        winner_text = font.render("Player 1 Wins!", True, WHITE)
    elif score2 > score1:
        winner_text = font.render("Player 2 Wins!", True, WHITE)
    else:
        winner_text = font.render("It's a Tie!", True, WHITE)

    # 畫面更新
    WIN.fill(BLACK)
    WIN.blit(background, (0, 0))  # 繪製背景
    pygame.draw.rect(WIN, WHITE, paddle1)
    pygame.draw.rect(WIN, WHITE, paddle2)
    pygame.draw.ellipse(WIN, WHITE, ball)
    pygame.draw.ellipse(WIN, WHITE, middle_line)

    #分數
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    #倒計時
    countdown_text = font.render(str(countdown // 100), True, WHITE)
    WIN.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))

    pygame.display.flip()

    countdown -= 1
    # 控制遊戲迴圈的速度
    clock.tick(60)

if score1 > score2:
    winner_text = font.render("Player 1 Wins!", True, WHITE)
elif score2 > score1:
    winner_text = font.render("Player 2 Wins!", True, WHITE)
else:
    winner_text = font.render("It's a Tie!", True, WHITE)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    WIN.blit(background, (0, 0))  # 繪製背景
    WIN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
    
    pygame.display.flip()
    clock.tick(60)