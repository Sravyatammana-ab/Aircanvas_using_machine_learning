import cv2 as cv
import numpy as np
import mediapipe as mp
import os

def is_inside(point, rect_pt1, rect_pt2):
# this func Checks if point is inside the rectangle defined by two points.
    x, y = point
    x1, y1 = rect_pt1
    x2, y2 = rect_pt2
    return x1 <= x <= x2 and y1 <= y <= y2

def clear_all():
    canvas1[:]=(0,0,0)

cv.namedWindow = lambda x: None
prev_x,prev_y=-1,-1
fps = 0
prev_time = cv.getTickCount()

script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the full path to the image
image_path = os.path.join(script_dir, 'CLEAR ALL.png')

# Load the image from file
header = cv.imread(image_path)
#initializing color index to switch to multipe colors and colors in the list
color_index=0
colors = [(255,0,0),(0,0,255),(0,255,0),(255,255,0),(0,0,0)]
#Initializing the model
mp_hands = mp.solutions.hands.Hands(static_image_mode=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=1,
    model_complexity=1)
mp_drawing = mp.solutions.drawing_utils

#Tells which device to use as input  for camera (webcam or video file)
cap = cv.VideoCapture(0)

#naming and resizing the window
cv.namedWindow("Paint_window")
cap.set(3,1280)
cap.set(4,720)

_, frame = cap.read()

canvas1 = np.zeros(frame.shape, dtype=np.uint8)
penSelected=False;Eraser=False
while cap.isOpened():
    success,frame = cap.read()
    if not success :
        print("Ignoring empty frame.")
        continue
    #flipping the frame 
    frame = cv.flip(frame,1)
    #color converting the frame
    frame = cv.cvtColor(frame,cv.COLOR_BGR2RGB)

    #fps function
    current_time = cv.getTickCount()
    elapsed_time = (current_time - prev_time) / cv.getTickFrequency()
    fps = 1 / elapsed_time
    prev_time = current_time
    # Display the FPS in output window
    cv.putText(frame, "FPS: {:.1f}".format(fps), (15, 150), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    result = mp_hands.process(frame)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmark_list = []
            for landmark in hand_landmarks.landmark:
                x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                # inorder to get landmarks in coordinates we need to multipy the points with frame shape
                landmark_list.append((x, y))
        index_tip = landmark_list[8]
        middle_tip = landmark_list[12]

        #selection mode
        if index_tip[1]>middle_tip[1]:
            # print("Selection Mode",landmark_list[8],landmark_list[12])
            Penselected = False ;Eraser=False
            prev_x,prev_y=(-1,-1)
        else:
                if is_inside(index_tip,(0,0), (260,120)):
                    clear_all()
                elif is_inside(index_tip,(350,0), (470,120)):
                    color_index = 0
                    penSelected=True;Eraser=False
                elif is_inside(index_tip,(520,0), (640,120)):
                    color_index = 1
                    penSelected=True;Eraser=False
                elif is_inside(index_tip,(700,0), (820,120)):
                    color_index = 2
                    penSelected=True;Eraser=False
                elif is_inside(index_tip,(880,0), (1000,120)):
                    color_index = 3
                    penSelected=True;Eraser=False
                elif is_inside(index_tip, (1050,0), (1280,120)):
                    color_index = -1
                    Penselected=False;Eraser=True
                else:
                    if penSelected:
                        if (prev_x,prev_y)==(-1,-1):
                            prev_x,prev_y=index_tip
                            continue
                        if prev_x!=-1 and prev_y!=-1:
                            cv.line(canvas1,(prev_x,prev_y),index_tip,colors[color_index],5)
                            cv.line(frame,(prev_x,prev_y),index_tip,colors[color_index],5)
                        prev_x,prev_y=index_tip
                    if Eraser:
                        cv.line(canvas1,(prev_x,prev_y),index_tip,colors[color_index],50)
                        cv.line(frame,(prev_x,prev_y),index_tip,colors[color_index],50)
    canvasGray = cv.cvtColor(canvas1, cv.COLOR_BGR2GRAY)
    _, imgInv = cv.threshold(canvasGray, 20, 255, cv.THRESH_BINARY_INV)
    imgInv = cv.cvtColor(imgInv, cv.COLOR_GRAY2BGR)
    frame = cv.bitwise_and(frame, imgInv)
    frame = cv.bitwise_or(frame, canvas1)
    frame = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    # frame = cv.flip(frame,1)
    frame[0:120,0:1280]=header
    cv.imshow("Paint_window",frame)
    # cv.imshow("Canvas",canvas1)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()

