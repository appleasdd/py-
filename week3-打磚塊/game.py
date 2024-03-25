import pygame
import sys
import random

# 初始化pygame
pygame.init()

# 設定遊戲視窗大小
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("打磚塊遊戲")

# 定義顏色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# 定義球的屬性
ball_radius = 10
ball_color = red
ball_pos = [window_size[0] // 2, window_size[1] // 2]
ball_speed = [random.choice([-5, 5]), 5]

# 定義擊打板的屬性
paddle_width = 100
paddle_height = 10
paddle_color = blue
paddle_pos = [(window_size[0] - paddle_width) // 2, window_size[1] - paddle_height]

# 定義磚塊的屬性
brick_width = 80
brick_height = 20
brick_color = white
brick_rows = 5
brick_cols = 10
brick_padding = 5
bricks = []

for row in range(brick_rows):
    for col in range(brick_cols):
        brick_x = col * (brick_width + brick_padding)
        brick_y = row * (brick_height + brick_padding)
        bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

# 遊戲主迴圈
game_over = False
game_won = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # 如果遊戲結束且按下 B 鍵，重新啟動遊戲
    if game_over and keys[pygame.K_b]:
        game_over = False
        game_won = False
        ball_pos = [window_size[0] // 2, window_size[1] // 2]
        ball_speed = [random.choice([-5, 5]), 5]
        paddle_pos = [(window_size[0] - paddle_width) // 2, window_size[1] - paddle_height]
        bricks = [
            pygame.Rect(col * (brick_width + brick_padding), row * (brick_height + brick_padding), brick_width, brick_height)
            for row in range(brick_rows) for col in range(brick_cols)
        ]

    # 移動擊打板
    if keys[pygame.K_LEFT] and paddle_pos[0] > 0:
        paddle_pos[0] -= 10
    if keys[pygame.K_RIGHT] and paddle_pos[0] < window_size[0] - paddle_width:
        paddle_pos[0] += 10

    # 移動球
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # 球碰到牆壁時反彈
    if ball_pos[0] <= 0 or ball_pos[0] >= window_size[0] - ball_radius:
        ball_speed[0] = -ball_speed[0]
    if ball_pos[1] <= 0:
        ball_speed[1] = -ball_speed[1]

    # 如果球超出底部，遊戲結束
    if ball_pos[1] >= window_size[1]:
        game_over = True

    # 球碰到擊打板時反彈
    if (
        paddle_pos[0] <= ball_pos[0] <= paddle_pos[0] + paddle_width
        and paddle_pos[1] <= ball_pos[1] <= paddle_pos[1] + paddle_height
    ):
        ball_speed[1] = -ball_speed[1]

    # 檢查球是否碰到磚塊
    for brick in bricks:
        if brick.colliderect(pygame.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, ball_radius * 2, ball_radius * 2)):
            bricks.remove(brick)
            ball_speed[1] = -ball_speed[1]

    # 清除畫面
    screen.fill(black)

    # 畫出擊打板
    pygame.draw.rect(screen, paddle_color, (paddle_pos[0], paddle_pos[1], paddle_width, paddle_height))

    # 畫出球
    pygame.draw.circle(screen, ball_color, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # 畫出磚塊
    for brick in bricks:
        pygame.draw.rect(screen, brick_color, brick)

    # 如果遊戲結束，顯示文字
    if game_over:
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over. Press B to restart.", True, white)
        text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
        screen.blit(text, text_rect)

    if game_won:
        font = pygame.font.Font(None, 36)
        text = font.render("Congratulations! You Won. B can restart", True, white)
        text_rect = text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
        screen.blit(text, text_rect)

    # 更新畫面
    pygame.display.flip()

    # 控制遊戲速度
    pygame.time.Clock().tick(60)