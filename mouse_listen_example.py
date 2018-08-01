import cv2
import numpy as np

# 当鼠标按下时变为True
drawing = False
# 如果mode为true绘制矩形。按下'm' 变成绘制曲线。
ix, iy = -1, -1


def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy=x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),-1)



img = np.ones([500, 500, 3], np.uint8) * 255
img_copy = img.copy()
print(np.sum(img[:]))
keyvalue = {
    'a': 97,
    'd': 100,
    'q': 113,
    'e': 101,
    'y': 121,
    '[': 91,
    ']': 93,
    'l': 108,
    'esc': 27
}
cv2.namedWindow('label image software')
cv2.setMouseCallback('label image software', draw_circle)
while True:
    cv2.imshow('label image software', img)
    c = cv2.waitKey(10)

    if c == keyvalue['esc']:
        break
    elif c == keyvalue['a']:
        img = img_copy.copy()
        print(np.sum(img_copy[:]))
cv2.destroyAllWindows()