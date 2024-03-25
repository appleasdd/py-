import pygame
import random

# 初始化 Pygame
pygame.init()

# 設定遊戲視窗
width, height = 600, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("2048 Game")

# 定義顏色
white = (255, 255, 255)
black = (0, 0, 0)
tile_colors = {
    0: (205, 192, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# 初始化遊戲狀態
grid_size = 6
grid = [[0] * grid_size for _ in range(grid_size)]
score = 0

def move(direction):
    global score

    if direction == 'left':
        for y in range(grid_size):
            for x in range(grid_size):
                if grid[x][y] != 0:
                    for i in range(x - 1, -1, -1):
                        if grid[i][y] == 0:
                            grid[i][y] = grid[i + 1][y]
                            grid[i + 1][y] = 0
                        elif grid[i][y] == grid[i + 1][y]:
                            grid[i][y] *= 2
                            score += grid[i][y]
                            grid[i + 1][y] = 0
                            break
                        else:
                            break
    elif direction == 'right':
        for y in range(grid_size):
            for x in range(grid_size - 1, -1, -1):
                if grid[x][y] != 0:
                    for i in range(x + 1, grid_size):
                        if grid[i][y] == 0:
                            grid[i][y] = grid[i - 1][y]
                            grid[i - 1][y] = 0
                        elif grid[i][y] == grid[i - 1][y]:
                            grid[i][y] *= 2
                            score += grid[i][y]
                            grid[i - 1][y] = 0
                            break
                        else:
                            break

    elif direction == 'up':
        for x in range(grid_size):
            for y in range(grid_size):
                if grid[x][y] != 0:
                    for i in range(y - 1, -1, -1):
                        if grid[x][i] == 0:
                            grid[x][i] = grid[x][i + 1]
                            grid[x][i + 1] = 0
                        elif grid[x][i] == grid[x][i + 1]:
                            grid[x][i] *= 2
                            score += grid[x][i]
                            grid[x][i + 1] = 0
                            break
                        else:
                            break

    elif direction == 'down':
        for x in range(grid_size):
            for y in range(grid_size - 1, -1, -1):
                if grid[x][y] != 0:
                    for i in range(y + 1, grid_size):
                        if grid[x][i] == 0:
                            grid[x][i] = grid[x][i - 1]
                            grid[x][i - 1] = 0
                        elif grid[x][i] == grid[x][i - 1]:
                            grid[x][i] *= 2
                            score += grid[x][i]
                            grid[x][i - 1] = 0
                            break
                        else:
                            break
# 新增一個隨機數字(2或4)到空的格子
def add_random_tile():
    empty_tiles = [(x, y) for x in range(grid_size) for y in range(grid_size) if grid[x][y] == 0]
    if empty_tiles:
        x, y = random.choice(empty_tiles)
        grid[x][y] = random.choice([2, 4])

# 畫出方塊
def draw_tiles():
    for x in range(grid_size):
        for y in range(grid_size):
            value = grid[x][y]
            color = tile_colors.get(value, (255, 255, 255))
            pygame.draw.rect(window, color, (x * 100, y * 100, 100, 100))
            if value != 0:
                font = pygame.font.Font(None, 36)
                text = font.render(str(value), True, black)
                text_rect = text.get_rect(center=(x * 100 + 50, y * 100 + 50))
                window.blit(text, text_rect)

# 畫出分數
def draw_score():
    score = sum(row for row in map(sum, grid))
    font = pygame.font.Font(None, 48)
    text = font.render("Score: " + str(score), True, black)
    window.blit(text, (10, height - 50))

# 更新遊戲畫面
def update_screen():
    window.fill(white)
    draw_tiles()
    draw_score()
    pygame.display.flip()

# 遊戲主迴圈
running = True
add_random_tile()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move('left')
                add_random_tile()
            elif event.key == pygame.K_RIGHT:
                move('right')
                add_random_tile()
            elif event.key == pygame.K_UP:
                move('up')
                add_random_tile()
            elif event.key == pygame.K_DOWN:
                move('down')
                add_random_tile()
        

    # 在這裡更新遊戲邏輯，例如處理移動、合併方塊等

    update_screen()

# 關閉 Pygame
pygame.quit()