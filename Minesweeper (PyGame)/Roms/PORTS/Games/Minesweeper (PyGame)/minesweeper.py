# coding:utf-8
# This is a minesweeper game
import pygame, sys, random, time

# 主畫面大小參數
width = 640
height = 480
w = 40                           # 格子寬度
cols = int(width / w)            # 欄位數
rows = int(height / w)           # 列位數

click_show = 1
kxpos = 0
kypos = 0
kxspace = width / cols
kyspace = height / rows

class Cell:
    def __init__(self, i, j, w):
        self.i = i          # 欄
        self.j = j          # 列
        self.x = i * w      # x座標
        self.y = j * w      # y座標
        self.w = w          # 方格寬
        self.bombCount = 0  # 周圍炸彈數
        self.bomb = False   # 方格內有無炸彈
        self.revealed = False  # 方格是否顯示
    def show(self):
        if click_show > 0:
            playSurface.blit(img_click, pygame.Rect(kxpos * kxspace - 32, kypos * kyspace - 3, 0, 0))
        cell = pygame.Rect(self.x, self.y, self.w, self.w)  # 得到方格的方形區域
        # 如果此方格為顯示狀態
        if (self.revealed):
            # 方格內有炸彈
            if (self.bomb):
                # 炸彈圖檔對齊方格中心後貼到畫面上
                rect = img_bomb.get_rect()
                rect.center = (int(self.x+self.w/2), int(self.y+self.w/2))
                playSurface.blit(img_bomb, rect)
            # 方格內不是炸彈
            else:
                playSurface.fill(gray, cell)   # 該方格填上底色
                # 如果周圍炸彈數非0
                if (self.bombCount > 0):
                    # 設定字體款式->建立字體表面->得到字體矩形區域->對齊方格中心->貼上
                    sFont = pygame.font.SysFont('monaco', 30)
                    Ssurf = sFont.render('{0}'.format(self.bombCount), True, black)
                    Srect = Ssurf.get_rect()
                    Srect.center = (self.x + self.w/2, self.y + self.w/2)
                    playSurface.blit(Ssurf, Srect)
        pygame.draw.rect(playSurface, black, cell, 1)  # 畫上正方形於方格內
    def contains(self, x, y):
    	# 回傳(x,y)是否在本方格之區域內
        return (x > self.x and x < self.x + self.w and y > self.y and y < self.y + self.w)
    def reveal(self):
        self.revealed = True   # 設定炸彈為 存在
        self.show()            # 這一格重畫
        pygame.display.flip()  # 更新畫面
        if (self.bombCount == 0):
            self.floodFill()   # 如果周圍沒有炸彈就擴散
    def countBombs(self):
        # 如果本身是炸彈，設定炸彈數-1
        if (self.bomb):
            self.bombCount = -1
            return
        total = 0  # 初始計量
        # 計算周遭鄰居的炸彈個數
        for xoff in range(-1, 2):
            for yoff in range(-1, 2):
                # 計算鄰居方格的表格座標
                i = self.i + xoff
                j = self.j + yoff
                # 邊界方格條件 (預防超出範圍)
                if (i > -1 and i < cols and j > -1 and j < rows):
                    neighbor = grid[i][j] # 邊鄰方格
                    if (neighbor.bomb):
                        total += 1        # 如果有炸彈就加1
        self.bombCount = total            # 回傳記數值
    def floodFill(self):
    	# 左:-1 中:0 右:1
        for xoff in range(-1, 2):
            # 上:-1 中:0 下:1
            for yoff in range(-1, 2):
                i = self.i + xoff
                j = self.j + yoff
                # 邊
                if (i > -1 and i < cols and j > -1 and j < rows):
                    neighbor = grid[i][j] # 邊鄰方格
                    # 邊鄰方格沒有炸彈且未顯示，就顯示
                    if (not neighbor.bomb and not neighbor.revealed):
                        time.sleep(0.05)  # 控制漸進擴散的速度
                        neighbor.reveal() # 間隔一段時間後開啟邊鄰方格  

class Explode:
    def __init__(self):
        # 讀取一系列爆炸圖像
        self.image = [pygame.image.load("explosion" + str(v) + ".png") for v in range(1, 9)]
        self.interval = 0.2   # 每張間隔
    def show(self, index, x, y, w):
    	# 要先訂好大小再取長方形，不然位子會跑掉
        img = pygame.transform.scale(self.image[index], (w-2, w-2)) # 壓縮至固定大小
        rect = img.get_rect()
        rect.center = (int(x+w/2), int(y+w/2))                      # 對齊方格中心
        playSurface.blit(img, rect)                                 # 貼到畫面上
        pygame.display.flip()                                       # 更新畫面
        

def make2DArray(cols, rows):
    # 建立空白2D array
    Array = [[0 for y in range(rows)] for x in range(cols)]
    return Array

def MousePressed():
	# 取得滑鼠位置
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for i in range(cols):
        for j in range(rows):
            # 當滑鼠位於該區域內
            if (grid[i][j].contains(mouse_x, mouse_y)):
                sound_click.play()    # 播放 點擊 音效
                grid[i][j].reveal()   # 顯示該方格
                # 如果點到有炸彈的方格就gameover
                if (grid[i][j].bomb):
                    gameOver()

def gameOver():
    # 設定所有格子為 顯示
    for i in range(cols):
        for j in range(rows):
            grid[i][j].revealed = True
    # 撥放 爆炸 & 結束 音效
    sound_bomb.play()
    sound_end.play()
    # 顯示所有格子
    for i in range(cols):
        for j in range(rows):
            grid[i][j].show()
    # 延遲0.1秒後進入爆炸階段
    time.sleep(0.1)
    explosion = Explode()
    # 爆炸特效顯示 (目的是讓所有炸彈同時爆炸)
    for k in range(len(explosion.image)):  # 圖像列表長度
        for location in bombList:          # 含有炸彈的座標列表
            i = location[0]
            j = location[1]
            bomb = grid[i][j]              # 取得方格資訊
            explosion.show(k, bomb.x, bomb.y, bomb.w) # 顯示該片段畫面於該方格
        time.sleep(explosion.interval)     # 間隔以做出連續畫面的效果
    # 等待2秒關閉視窗且退出
    time.sleep(2)
    pygame.quit()
    sys.exit()

def WinningDetect():
    # 檢查是否勝利
    for i in range(cols):
        for j in range(rows):
            # 檢查每一個格子
            cell = grid[i][j]
            if (cell.bomb and cell.revealed):
                return False   # 有炸彈 且 已顯示
            elif (not cell.bomb and not cell.revealed):
                return False   # 無炸彈 且 未顯示
    return True   # 一切無誤即勝利

def gameWinning():
    sound1.play()  # 播放音效
    sound2.play()
    time.sleep(3)  # 停留3秒
    pygame.quit()  # pygame中止
    sys.exit()     # 系統退出

grid = make2DArray(cols, rows)   # 產生空白二維陣列

# 初始化隨機種子
random.seed()

# 確認pygame初始化有無錯誤
check_errors = pygame.init()
if (check_errors[1] > 0):
    print("(!) Had {0} initializing errors,exiting... ".format(check_errors[1]))
    sys.exit(-1)
else:
    print("(+) Pygame successfully initialized!")

# 音樂功能初始化
pygame.mixer.init()

# 點擊 音效
sound_click = pygame.mixer.Sound('Mouse.wav')
sound_click.set_volume(0.5)
# 炸彈 音效
sound_bomb = pygame.mixer.Sound('Bomb.wav')
sound_bomb.set_volume(0.3)
# 失敗 音效
sound_end = pygame.mixer.Sound('fail.wav')
sound_end.set_volume(0.3)
# 勝利 音效
sound1 = pygame.mixer.Sound('DongDong.wav')
sound1.set_volume(0.7)
sound2 = pygame.mixer.Sound('YouWin.wav')
sound2.set_volume(0.7)

# 主畫面
playSurface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Minesweeper')

# 設定顏色
white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)
gray = pygame.Color(200, 200, 200)     

# 幀數控制器
fpsController = pygame.time.Clock()
# 幀率
frame_rate = 50

# 輸入炸彈圖片檔，將其轉為固定大小
img_bomb = pygame.image.load('bomb.png')
img_bomb = pygame.transform.scale(img_bomb, (int(w/2)+20, int(w/2)+20))

img_click = pygame.image.load('click.png')
img_click = pygame.transform.scale(img_click, (int(80), int(80)))

# 炸彈總個數
totalBombs = 30

# 給每一個方格一個類別
for i in range(cols):
    for j in range(rows):
        grid[i][j] = Cell(i, j, w)

optionList = []  # 可選擇的位置
bombList = []    # 炸彈位置

# 將所有座標輸入到 optionList 裡面
for i in range(cols):
    for j in range(rows):
        optionList.append([i, j])

# 設定炸彈位置
for num in range(totalBombs):
    index = int(random.randrange(len(optionList))) # 隨機選擇數字(介於 0 ~ List長度之間)
    choice = optionList[index]          # 該數字對應到列表->座標
    i = choice[0]                       # 方格 x 位置
    j = choice[1]                       # 方格 y 位置
    bombList.append(choice)             # 將座標存入bombList中
    optionList.pop(index)               # 將座標從選擇表中移除
    grid[i][j].bomb = True              # 將該位置標記為有炸彈

# 數周圍炸彈的個數
for i in range(cols):
    for j in range(rows):
        grid[i][j].countBombs()

while True:
    # 背景顏色
    playSurface.fill(white)

    # 先把底畫好，後面才能做出擴散的效果
    for i in range(cols):
        for j in range(rows):
            grid[i][j].show()

    # 偵測滑鼠是否按下
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            click = 0
            if event.key == pygame.K_UP:
                if kypos > 0:
                    kypos = kypos - 1
            if event.key == pygame.K_DOWN:
                if kypos < (rows - 1):
                    kypos = kypos + 1
            if event.key == pygame.K_LEFT:
                if kxpos > 0:
                    kxpos = kxpos - 1
            if event.key == pygame.K_RIGHT:
                if kxpos < (cols - 1):
                    kxpos = kxpos + 1
            if event.key == pygame.K_SPACE:
                click = 1
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            if click == 1:
                sound_click.play()    # 播放 點擊 音效
                grid[kxpos][kypos].reveal()   # 顯示該方格
                # 如果點到有炸彈的方格就gameover
                if (grid[kxpos][kypos].bomb):
                    click_show = 0
                    gameOver()
            
        elif event.type == pygame.MOUSEBUTTONUP:
            MousePressed()
    
    # 確認是否獲勝
    if (WinningDetect()):
        gameWinning()

    pygame.display.flip()            # 更新視窗畫面
    fpsController.tick(frame_rate)   # 幀數
