import cv2
import numpy as np

click = False     # Mouse 클릭된 상태 (false = 클릭 x / true = 클릭 o) : 마우스 눌렀을때 true로, 뗏을때 false로
x1,y1 = -1,-1
mode = "black"

# Mouse Callback함수 : 파라미터는 고정됨.
def draw_rectangle(event, x, y, flags, param):
    global x1,y1, click, mode                                     # 전역변수 사용

    if event == cv2.EVENT_LBUTTONDOWN:                      # 마우스를 누른 상태
        click = True 
        x1, y1 = x,y
        print("사각형의 왼쪽위 설정 : (" + str(x1) + ", " + str(y1) + ")")
		
    elif event == cv2.EVENT_MOUSEMOVE:                      # 마우스 이동
        if click == True:         
            if mode == "black":
                cv2.rectangle(dst2,(x1,y1),(x,y),(0,0,0),-1)
            elif mode == "white":
                cv2.rectangle(dst2,(x1,y1),(x,y),(255,0,0),-1)

    elif event == cv2.EVENT_LBUTTONUP:
        click = False;                                      # 마우스를 때면 상태 변경
        if mode == "black":
            cv2.rectangle(dst2,(x1,y1),(x,y),(0,0,0),-1)
        elif mode == "white":
            cv2.rectangle(dst2,(x1,y1),(x,y),(255,0,0),-1)

if __name__ == "__main__":
    
    img_size_ratio = 0.5
    dliate_iteration = 5
    
    img = cv2.imread("make_mask/driver_06.jpg")
    img = cv2.resize(img, (0,0), fx=img_size_ratio, fy=img_size_ratio)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, dst = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    dst1 = cv2.morphologyEx(dst, cv2.MORPH_OPEN, None)
    dst2 = cv2.dilate(dst1, None, iterations=dliate_iteration)
    
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_rectangle, dst2)
    
    while True:
        cv2.imshow('image', dst2)    # 화면을 보여준다.

        k = cv2.waitKey(1) & 0xFF   # 키보드 입력값을 받고
        
        if k == 27:
            break
    
    cv2.destroyAllWindows()
    
    mode = "white"
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_rectangle, dst2)
    
    while True:
        cv2.imshow('image', dst2)    # 화면을 보여준다.

        k = cv2.waitKey(1) & 0xFF   # 키보드 입력값을 받고
        
        if k == 27:               # esc를 누르면 종료
            dst2 = cv2.resize(dst2, (0,0), fx=1/img_size_ratio, fy=1/img_size_ratio)
            cv2.imwrite("mask_result.png", dst2)
            break

    cv2.destroyAllWindows()