# 引入下方程式所需的函式庫
import sys
import pygame
import numpy
import os
from pygame.locals import QUIT, KEYUP

# 設定初始化及基礎設定(標題、背景顏色、線條顏色)
# 初始化
pygame.init()
# 音效初始化
pygame.mixer.init()
# 建立遊戲視窗畫布,大小為 670*710
game_screen = pygame.display.set_mode((670, 710))
# 設置視窗標題為 五子棋
pygame.display.set_caption("五子棋")

# 設定常用顏色
WHITE = [255, 255, 255]
GREY = [220, 220, 220]
BLACK = [0, 0, 0]
# 設定背景顏色(棕黃色)
game_screen_color = [238, 154, 73]

# 引入初始畫面的圖片
background_image = pygame.image.load(os.path.join("background_image1-1.jpg")).convert()
# 調整圖片大小
background_image = pygame.transform.scale(background_image, (900, 1181.25))
# 載入棋子
chess1 = 'blackChess.png'
chess2 = 'whiteChess.png'
# 引入音效、音樂
# 下棋音效X
play_sound = pygame.mixer.Sound(os.path.join("play_chess.mp3"))
# 黑棋玩家獲勝音效
winner_sound2 = pygame.mixer.Sound(os.path.join("white.mp3"))
# 白旗玩家獲勝音效
winner_sound1 = pygame.mixer.Sound(os.path.join("black.mp3"))
# 背景音樂
pygame.mixer.music.load("background_music.mp3")
# 設置背景音樂音量
pygame.mixer.music.set_volume(0.7)
# 重複撥放背景音樂
pygame.mixer.music.play(-1)

# 宣告一個可將字顯示在畫面上的函式
def draw_text(surf, text, color, size, x, y):
    # 建一個font物件
    game_font = pygame.font.Font("font.ttf", size)
    # 將font要寫的文字渲染出來
    text_surface = game_font.render(text, True, color)
    # 將文字定位
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    # 將文字畫在指定位置
    surf.blit(text_surface, text_rect)

# 宣告可顯示初始畫面、下棋教學的函式
def draw_init():
    # 畫出背景圖片
    game_screen.blit(background_image, (-140, -260))
    # 顯示標題、遊戲教學
    draw_text(game_screen, "五子棋", WHITE, 120, 670 / 2, 700 / 4 + 20)
    draw_text(game_screen, "使用滑鼠選擇下棋位置", WHITE, 30, 670 / 2, 700 / 2 + 50)
    draw_text(game_screen, "點擊滑鼠左鍵下棋~", WHITE, 30, 670 / 2, 700 / 2 + 40 + 50)
    draw_text(game_screen, "按任意鍵可重新遊戲!", WHITE, 20, 670 / 2, 580)
    # 更新畫面
    pygame.display.update()
    # 持續待在等待遊戲開始的畫面
    waiting_start = True
    while waiting_start:
        for event in pygame.event.get():
            # 當使用者結束視窗，程式結束
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # 若按任意鍵，則停止等待遊戲開始
            elif event.type == KEYUP:
                waiting_start = False

# 宣告一個能回傳可落子位置的函式
def A(x, y):
    for i in range(27, 670, 44):
        for j in range(27, 670, 44):
            X1 = i - 22
            X2 = i + 22
            Y1 = j - 22
            Y2 = j + 22
            # 若鼠標附近有棋盤交點
            if x >= X1 and x <= X2 and y >= Y1 and y <= Y2:
                # 則回傳鼠標附近的棋盤交點
                return i, j
    # 若不在棋盤範圍內，則回傳鼠標目前位置
    return x, y

# 宣告一個檢查是否已有落子的函式
def Check(x, y, played):
    # 限制在棋盤內線上交點處
    if x >= 27 and x <= 643 and y >= 27 and y<= 643:
        for chess in played:
            # 如果鼠標的座標已有落子，則回傳False(無法落子)
            if chess[0][0] == x and chess[0][1] == y:
                return False
        # 目前沒落子(可以落子)
        return True

# 下棋標籤
flag = False
# 延遲變數
time = 0

# 已落子的位置集合
played = []

# 宣告一個判斷是否有人五子連線的函示
def check_win(played):
    # 設一個全為0的 15*15陣列，代表所有棋格
    id = numpy.zeros([15, 15], dtype=int)
    for chess in played:
        # 將位置作編號
        x = int((chess[0][0] - 27) / 44)
        y = int((chess[0][1] - 27) / 44)
        # 在所有下過的棋格，若此格為黑子，則將這格設為1
        if chess[1] == BLACK:
            id[x][y] = 1
        # 否則設為2
        else:
            id[x][y] = 2
    
    # 判斷是否有連續 直向 五子
    for i in range(15):
        player1 = []
        player2 = []
        for j in range(15):
            # 若有連續直向黑棋，則將棋子id持續加入黑棋玩家的陣列
            if id[i][j] == 1:
                player1.append([i, j])
            # 否則清空黑棋玩家的陣列
            else:
                player1 = []
            
            # 白棋同黑棋處理
            if id[i][j] == 2:
                player2.append([i, j])
            else:
                player2 = []
            
            # 若有同色棋子連續超過五子連線
            # 則回傳勝利玩家和五子連線的位置
            if len(player1) >= 5:
                return [1, player1]
            if len(player2) >= 5:
                return [2, player2]
    
    # 判斷是否有連續 橫向 五子
    for j in range(15):
        player1 = []
        player2 = []
        for i in range(15):
            # 若有連續橫向黑棋，則將棋子id持續加入黑棋玩家的陣列
            if id[i][j] == 1:
                player1.append([i, j])
            # 否則清空黑棋玩家的陣列
            else:
                player1 = []
            
            # 白棋同黑棋處理
            if id[i][j] == 2:
                player2.append([i, j])
            else:
                player2 = []
            
            # 若有同色棋子連續超過五子連線
            # 則回傳勝利玩家和五子連線的位置
            if len(player1) >= 5:
                return [1, player1]
            if len(player2) >= 5:
                return [2, player2]
    
    # 判斷是否有連續 左上-右下 五子
    for i in range(15):
        for j in range(15):
            player1 = []
            player2 = []
            for k in range(15):
                # 若超過棋盤範圍，則跳出迴圈
                if i + k >= 15 or j + k >= 15:
                    break
                
                # 若有連續斜向(左上-右下)黑棋，則將棋子id持續加入黑棋玩家的陣列
                if id[i + k][j + k] == 1:
                    player1.append([i + k, j + k])
                # 否則清空黑棋玩家的陣列
                else:
                    player1 = []
                
                # 白棋同黑棋處理
                if id[i + k][j + k] == 2:
                    player2.append([i + k, j + k])
                else:
                    player2 = []
                
                # 若有同色棋子連續超過五子連線
                # 則回傳勝利玩家和五子連線的位置
                if len(player1) >= 5:
                    return [1, player1]
                if len(player2) >= 5:
                    return [2, player2]
    
    # 判斷是否有連續 右上-左下 五子
    for i in range(15):
        for j in range(15):
            player1 = []
            player2 = []
            for k in range(15):
                # 若超過棋盤範圍，則跳出迴圈
                if i + k >= 15 or j - k < 0:
                    break
                
                # 若有連續斜向(右上-左下)黑棋，則將棋子id持續加入黑棋玩家的陣列
                if id[i + k][j - k] == 1:
                    player1.append([i + k, j - k])
                # 否則清空黑棋玩家的陣列
                else:
                    player1 = []
                
                # 白棋同黑棋處理
                if id[i + k][j - k] == 2:
                    player2.append([i + k, j - k])
                else:
                    player2 = []
                
                # 若有同色棋子連續超過五子連線
                # 則回傳勝利玩家和五子連線的位置
                if len(player1) >= 5:
                    return [1, player1]
                if len(player2) >= 5:
                    return [2, player2]
    return [0, []]


# 宣告一個顯示遊戲結束、按下任意鍵可重新遊戲的函式
def restart():
    # 若為黑棋玩家獲勝
    if res[0] == 1:
        # 顯示 黑棋玩家獲勝
        draw_text(game_screen, "黑棋玩家獲勝!", BLACK, 28, 670 / 2, 650)
        # 撥放 黑棋玩家獲勝 的音效
        winner_sound1.play()
    # 反之亦然
    else:
        # 顯示 白棋玩家獲勝
        draw_text(game_screen, "白棋玩家獲勝!", WHITE, 28, 670 / 2, 650)
        # 撥放 白棋玩家獲勝 的音效
        winner_sound2.play()
    # 在畫面最下方顯示 遊戲已結束,按任意鍵可重新遊戲!
    draw_text(game_screen, "遊戲已結束,按任意鍵可重新遊戲!", GREY, 18, 670 / 2, 685)
    # 更新畫面
    pygame.display.update()
    # 持續待在等待遊戲重新開始的畫面
    waiting_restart = True
    while waiting_restart:
        for event in pygame.event.get():
            # 當使用者結束視窗，程式結束
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # 若按任意鍵，則重新開始遊戲
            elif event.type == KEYUP:
                # 將 已下過的位置 的集合清空
                played.clear()
                waiting_restart = False

# 遊戲迴圈
show_init = True
game_over = False
while 1:
    #遊戲一開始，會進入等待開始遊戲的畫面
    if show_init:
        draw_init()
        show_init = False
    
    # 迭帶整個事件迴圈，若有符合事件則對應處理
    for event in pygame.event.get():
        # 當使用者結束視窗，程式結束
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # 清屏
    game_screen.fill(game_screen_color)
    
    # 開始製作棋盤
    # 畫線
    for i in range(27, 670, 44):
        # 畫豎線
        # 若為邊線，則線加寬
        if i == 27 or i == 643:
            pygame.draw.line(game_screen, BLACK, [i, 27], [i, 643], 4)
        # 否則正常寬即可
        else:
            pygame.draw.line(game_screen, BLACK, [i, 27], [i, 643], 2)
        
        # 畫橫線
        # 同上所述，加寬
        if i == 27 or i == 643:
            pygame.draw.line(game_screen, BLACK, [27, i], [643, i], 4)
        # 否則，正常寬
        else:
            pygame.draw.line(game_screen, BLACK, [27, i], [643, i], 2)
    
    # 在棋盤中央畫一個黑點表示正中心的位置
    # (讓畫面更像棋盤、輔助玩家找到中心點)
    # (不必要但是沒有黑點看起來怪怪的)
    pygame.draw.circle(game_screen, BLACK, [27 + 44 * 7, 27 + 44 * 7], 8, 0)
    # 棋盤繪製完成
    
    # 將所有棋子畫出來
    for chess in played:
        if chess[1] == BLACK:
            chess3= pygame.image.load(chess1)
        else:
            chess3= pygame.image.load(chess2)
        chess3 = pygame.transform.scale(chess3,(50, 50))
        game_screen.blit(chess3,chess[0])
    
    # 呼叫能檢查是否有五顆同色棋子連線的函式
    res = check_win(played)
    # 若有，則將這五顆棋子以洋紅色方框顯示
    if res[0] != 0:
        for chess in res[1]:
            pygame.draw.rect(game_screen, [238, 48, 167], [chess[0] * 44 + 27 - 22 + 44, chess[1] * 44 + 27 - 22 + 44, 44, 44], 2, 1)
        # 遊戲結束時，將準備進入遊戲結束畫面
        game_over = True
        # 畫面更新
        pygame.display.update()
    
    # 當遊戲結束時，呼叫可顯示遊戲結束、按下任意鍵可重新遊戲的函式
    if game_over:
        restart()
        game_over = False
    
    # 找到鼠標位置
    x, y = pygame.mouse.get_pos()
    
    # 呼叫找可落子位置的函式
    x, y = A(x, y)
    # 判斷鼠標位置是否有落子，若無則用空心方框顯示可落子位置
    if Check(x, y, played):
        pygame.draw.rect(game_screen, [0 , 229 , 238 ], [x - 22, y - 22, 44, 44], 2, 1)
    
    # 滑鼠左鍵以落子
    press = pygame.mouse.get_pressed()
    
    # time用來做延遲，以免按一下卻感應到很多次
    if press[0] and time == 0:
        flag = True
        # 判斷是否可落子，再落子
        if Check(x, y, played):
            # 落子時加入下棋音效
            play_sound.play()
            # 奇數回合(已下偶數個棋)為黑子回合
            if len(played) % 2 == 0:
                played.append([[x-25, y-25], BLACK])
            # 否則為白子回合
            else:
                played.append([[x-25, y-25], WHITE])
    
    # 做延遲處理
    if flag:
        time += 1
    
    # 延遲20ms
    if time % 20 == 0:
        flag = False
        time = 0
    
    # 更新畫面，等所有操作完成後一次更新(若沒更新，元素不會出現)
    pygame.display.update()