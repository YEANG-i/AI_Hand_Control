# version 1.0.0
# 只有鼠标控制飞机，空格键开火


# import autopy
# import cv2
# import HandTrackingModule as Htm
import math  # 引入数学模块\
import random
import pygame
from pygame import MOUSEMOTION, QUIT


def show_score():
    text = ("Score: %s" % score)
    score_render = font.render(text, True, (0, 255, 0))
    screen.blit(score_render, (10, 10))


def check_is_over():
    if is_over:
        text = "Game Over"
        render = over_font.render(text, True, (255, 0, 0))
        screen.blit(render, (200, 250))


# 9. 添加敌人 敌人类
class Enemy:
    def __init__(self):
        self.img = pygame.image.load('img/enemy.png')
        self.x = random.randint(200, 600)
        self.y = random.randint(50, 250)
        self.step = random.randint(2, 3)  # 敌人移动的速度

    def reset(self):  # 当被射中时，恢复位置
        self.x = random.randint(200, 600)
        self.y = random.randint(50, 200)


# 两个点之间的距离
def distance(bx, by, ex, ey):
    a = bx - ex
    b = by - ey
    return math.sqrt(a * a + b * b)  # 开根号


# 子弹类
class Bullet:
    def __init__(self):
        self.img = pygame.image.load('img/bullet.png')
        self.x = playerX + 16  # (64-32)/2
        self.y = playerY + 10
        self.step = 10  # 子弹移动的速度

    # 击中
    def hit(self):
        global score
        for e in enemies:
            if distance(self.x, self.y, e.x, e.y) < 30:
                # 射中啦
                bao_sound.play()
                e.reset()  # 射中小兵，小兵重置
                # 射中就重置子弹
                self.plus()
                score += 1
                print(score)

    def plus(self):
        self.img = pygame.image.load('img/bullet.png')
        self.x = playerX + 16  # (64-32)/2
        self.y = playerY + 10
        self.step = 10  # 子弹移动的速度


# 显示并移动子弹
def show_bullets():
    for b in bullets:
        screen.blit(b.img, (b.x, b.y))
        b.hit()  # 看看是否击中了敌人
        # b.x -= b.step/3
        b.y -= b.step  # 移动子弹
        # 判断子弹是否出了界面，如果出了就移除掉
        if b.y < 0:
            bullets.remove(b)


def enemy_out(number):
    for s in range(number):
        yys = Enemy()
        enemies.append(yys)


# 显示敌人，并且实现敌人的移动和下沉
def show_enemy():
    global is_over
    for e in enemies:
        screen.blit(e.img, (e.x, e.y))
        e.x += e.step
        if e.x > 736 or e.x < 0:
            e.step *= -1
            e.y += 50
            if e.y > 450:
                is_over = True
                print("游戏结束啦")
                enemies.clear()


def move_player():
    global playerX
    playerX += playerStep
    # 防止飞机出界
    if playerX > 736:
        playerX = 736
    if playerX < 0:
        playerX = 0


# 主程序
# # AI Camera初始化
# wCam, hCam = 640, 480
# frameR = 100  # Frame Reduction帧缩减
# Camera = cv2.VideoCapture(0)  # open Camera
# Camera.set(3, wCam)
# Camera.set(4, hCam)
# detector = Htm.handDetector(maxHands=1)  # 调用那个类，最大识别手的数量为 1 个
# wScr, hScr = autopy.screen.size()
# print(wScr, hScr)
# pygame初始化
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('飞机大战')  # 设置标题
icon = pygame.image.load('img/ufo.png')  # 设置图标
pygame.display.set_icon(icon)
bgImg = pygame.image.load('img/bg.png')
pygame.mixer.music.load('sound/bg.wav')  # 添加背景音效
pygame.mixer.music.play(-1)  # 单曲循环
bao_sound = pygame.mixer.Sound('sound/exp.wav')  # 创建射中音效
playerImg = pygame.image.load('img/player.png')  # 5.飞机
playerX = 400  # 玩家的X坐标
playerY = 500  # 玩家的Y坐标
playerStep = 0  # 玩家移动的速度
score = 0  # 分数
font = pygame.font.Font('freesansbold.ttf', 32)
is_over = False  # 游戏结束
over_font = pygame.font.Font('freesansbold.ttf', 64)
bullets = []  # 保存现有的子弹
enemies = []  # 保存所有的敌人
number_of_enemies = 12  # 敌人的数量
enemy_out(number_of_enemies)  # 产生敌人
i = 0

while True:
    screen.blit(bgImg, (0, 0))
    show_score()  # 显示分数
    # # AI Camera调用部分
    # success, frame = Camera.read()
    # frame_deal = detector.find_hands(frame)
    # land_mark_list, bbox = detector.find_position(frame_deal, draw=True)  # 识别手指头并划线
    # cv2.rectangle(frame_deal, (frameR, frameR), (wCam - frameR, hCam - frameR),
    #               (255, 0, 255), 2)  # print(fingers) 画方框？？# 画方框？？# 画方框？？
    # # # AI Camera手指调用部分
    # fingers = detector.fingers_up()  # 3. Check which fingers are up
    # if fingers:  # 大拇指开火，食指左移，中指右移
    #     if fingers[0] == 1:  # 抬起来就不动
    #         bullets.append(Bullet())
    #         print('发射子弹....，已发射{0}发'.format(i))
    #         i += 1
    #     if fingers[1] == 1 and fingers[2] == 0:  # 4. Only Index Finger : Moving Mode
    #         playerStep = -5
    #     if fingers[1] == 0 and fingers[2] == 1:
    #         playerStep = 5
    #     if fingers[1] == 1 and fingers[2] == 1:  # 抬起来就不动
    #         playerStep = 0
    # else:
    #     print("No fingers_up!!!!Give me your fingers_up!!!!!")
    # cv2.namedWindow("frame_deal", cv2.WINDOW_NORMAL)
    # cv2.imshow('frame_deal', frame_deal)

    # pygame调用部分
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            playerX = pos[0]
            playerY = pos[1]
        if event.type == pygame.KEYDOWN:  # 按下就移动
            if event.key == pygame.K_SPACE:
                print('发射子弹....')
                # 创建一颗子弹
                bullets.append(Bullet())

    screen.blit(playerImg, (playerX, playerY))
    move_player()  # 移动玩家
    show_enemy()  # 显示敌人
    show_bullets()  # 显示子弹
    check_is_over()  # 显示游戏结束字段
    pygame.display.update()  # 界面显示循环
    # AI Camera调用部分，触发结束程序
    # if cv2.waitKey(1) in [ord('q'), 27]:  # 按键盘上的 q 或 esc 退出（在英文输入法下）
    #     break
# # AI Camera调用部分，操作结束后释放屏幕
# Camera.release()
# cv2.destroyAllWindows()
