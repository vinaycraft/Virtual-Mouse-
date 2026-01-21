import cv2 
import mediapipe as mp 
import pyautogui
import sys

# Initialize MediaPipe hands - try different approaches
try:
    # Try the older solutions API
    hand_detector = mp.solutions.hands.Hands()
    drawing_utils = mp.solutions.drawing_utils
except AttributeError:
    try:
        # Try direct hands access
        hand_detector = mp.hands.Hands()
        drawing_utils = mp.drawing_utils
    except AttributeError:
        print("Error: MediaPipe version not compatible. Please install: pip install mediapipe==0.9.0.1")
        sys.exit(1)

# Initialize camera with error handling
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera")
    sys.exit(1)

screen_width, screen_height = pyautogui.size()

# Initialize variables outside the loop
index_x = index_y = 0
thumb_x = thumb_y = 0
middle_x = middle_y = 0
index2_x = index2_y = 0
ring_x = ring_y = 0
pinky_x = pinky_y = 0

# Gesture thresholds (adjustable)
CLICK_THRESHOLD = 20
DOUBLE_CLICK_THRESHOLD = 10
RIGHT_CLICK_THRESHOLD = 20
SCROLL_THRESHOLD = 20
MOVE_THRESHOLD = 100
ACTION_DELAY = 0.2  # Reduced delay for better responsiveness 

while True: 
    ret, frame = cap.read() 
    if not ret:
        print("Error: Could not read frame")
        break
        
    frame = cv2.flip(frame, 1) 
    frame_height, frame_width, _ = frame.shape 
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands: 
        for hand in hands: 
            drawing_utils.draw_landmarks(frame, hand) 
            landmarks = hand.landmark 
            for id, landmark in enumerate(landmarks): 
                x = int(landmark.x*frame_width) 
                y = int(landmark.y*frame_height) 
                if id == 8: 
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255)) 
                    index_x = screen_width/frame_width*x 
                    index_y = screen_height/frame_height*y
                if id == 4: 
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255)) 
                    thumb_x = screen_width/frame_width*x 
                    thumb_y = screen_height/frame_height*y 
                    
                    # Click gesture: thumb and index finger close
                    if abs(index_y - thumb_y) < CLICK_THRESHOLD: 
                        pyautogui.click()   
                        pyautogui.sleep(ACTION_DELAY) 
                    # Move gesture: thumb and index finger moderately close
                    elif abs(index_y - thumb_y) < MOVE_THRESHOLD: 
                        pyautogui.moveTo(index_x, index_y)
                if id == 12:
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255)) 
                    middle_x = screen_width/frame_width*x 
                    middle_y = screen_height/frame_height*y  
                    
                    # Double click gesture: index and middle fingers close
                    if abs(index_y - middle_y) < DOUBLE_CLICK_THRESHOLD: 
                        pyautogui.doubleClick() 
                        pyautogui.sleep(ACTION_DELAY)
                if id == 5: 
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                    index2_x = screen_width/frame_width*x 
                    index2_y = screen_height/frame_height*y
                    
                    # Right click gesture: thumb and index finger base close
                    if abs(index2_y - thumb_y) < RIGHT_CLICK_THRESHOLD:
                        pyautogui.rightClick()
                        pyautogui.sleep(ACTION_DELAY)
                    # elif abs(index2_y - thumb_y) < 10:
                    #     pyautogui.dragTo(index2_y, thumb_y, button="")

                if id == 16: 
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                    ring_x = screen_width/frame_width*x 
                    ring_y = screen_height/frame_height*y
                if id == 20: 
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                    pinky_x = screen_width/frame_width*x 
                    pinky_y = screen_height/frame_height*y
                    if abs(ring_y - thumb_y) < SCROLL_THRESHOLD:
                        pyautogui.scroll(70)
                        pyautogui.sleep(ACTION_DELAY)
                    elif abs(thumb_y - pinky_y) < SCROLL_THRESHOLD:
                        pyautogui.scroll(-70)
                        pyautogui.sleep(ACTION_DELAY)
                    
                # if id == 20: 
                #     cv2.circle(img=frame, center=(x,y), radius=10, color=(255, 0, 255))
                #     pinky_x = screen_width/frame_width*x 
                #     pinky_y = screen_height/frame_height*y
                # if id == 17: 
                #     cv2.circle(img=frame, center=(x,y), radius=10, color=(255, 0, 255))
                #     pinky2_x = screen_width/frame_width*x 
                #     pinky2_y = screen_height/frame_height*y
                #     if abs(pinky2_y - pinky_y) < 20:
                #         pyautogui.hscroll(-70)
                #         pyautogui.sleep(0.5)
                # if id == 2: 
                #     cv2.circle(img=frame, center=(x,y), radius=10, color=(255, 0, 255))
                #     thumb2_x = screen_width/frame_width*x
                #     thumb2_y = screen_height/frame_height*y
                #     if abs(thumb2_y - thumb_y) < 20:
                #         pyautogui.hscroll(70)
                #         pyautogui.sleep(0.5)

                
    cv2.imshow('Virtual Mouse', frame) 
    
    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()