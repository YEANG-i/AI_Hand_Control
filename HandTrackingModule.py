"""
Hand Tracking Module

"""

import math
import sys
import time
import cv2
import mediapipe as mp


class handDetector:
    def __init__(self, mode=False, maxHands=1, detectionCon=0.8, trackCon=0.8):
        self.lmList = None  # 后加的
        self.results = None  # 后加的
        self.mode = mode  # 静态图像模式，默认false，用于处理视频
        self.maxHands = maxHands  # 支持检测最多手的数量
        self.detectionCon = detectionCon  # 后面两个应该是检测和追踪的置信度阈值
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def find_hands(self, frame_input, draw=True):
        frame_RGB = cv2.cvtColor(frame_input, cv2.COLOR_BGR2RGB)  # 转换为 RGB 格式
        self.results = self.hands.process(frame_RGB)  # 完成对图像的处理，输入必须为 RGB 格式
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:  # 如果有检测到手
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame_input, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return frame_input

    def find_position(self, img, hand_no=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        if self.results.multi_hand_landmarks:  # 如果检测到手
            myHand = self.results.multi_hand_landmarks[hand_no]  # 0坐标，手腕位置
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])  # 指头序号，位置？？？？
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                x_min, x_max = min(xList), max(xList)
                y_min, y_max = min(yList), max(yList)
                bbox = x_min, y_min, x_max, y_max

                # if draw:  # 指头的轮廓画方框？？
                #     cv2.rectangle(img, (x_min - 20, y_min - 20), (x_max + 20, y_max + 20),
                #                   (0, 255, 0), 2)
        else:
            print("No Hands!!!!!!!!No Hands!!!!!!!!No Hands!!!!!!!!")
            print("Give me your Hands!!!!!Give me your Hands!!!!!Give me your Hands!!!!!")
            # sys.exit(1)
        return self.lmList, bbox

    def fingers_up(self):
        fingers = []
        # Thumb
        if self.results.multi_hand_landmarks:
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)  # self.land_mark_list[4][1] > self.land_mark_list[3][1]
            else:
                fingers.append(0)

            # Fingers
            for i in range(1, 5):
                if self.lmList[self.tipIds[i]][2] < self.lmList[self.tipIds[i] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                # totalFingers = fingers.count(1)
        else:
            print("函数内部No fingers_up!!!!Give me your fingers_up!!!!!")
            # sys.exit(1)
        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]


def main():
    pTime = 0
    Camera = cv2.VideoCapture(0)  # open Camera
    detector = handDetector()

    while True:
        success, frame = Camera.read()
        frame_deal = detector.find_hands(frame)  # 把原始图像传进去，识别出，然后绘出线
        lmList, bbox = detector.find_position(frame_deal)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(frame_deal, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.namedWindow("frame_deal", cv2.WINDOW_NORMAL)
        cv2.imshow('frame_deal', frame_deal)
        if cv2.waitKey(1) in [ord('q'), 27]:  # 按键盘上的 q 或 esc 退出（在英文输入法下）
            break
    # 所有操作结束后不要忘记释放
    Camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
