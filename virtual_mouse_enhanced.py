import cv2
import mediapipe as mp
import pyautogui
import sys
import time
import math
import numpy as np
from collections import deque
from dataclasses import dataclass
from typing import Tuple, Optional
from config import GestureConfig

@dataclass
class HandState:
    """Track hand state for smooth interactions"""
    last_click_time: float = 0
    last_position: Tuple[float, float] = (0, 0)
    position_history: deque = None
    is_dragging: bool = False
    gesture_active: Optional[str] = None
    
    def __post_init__(self):
        if self.position_history is None:
            self.position_history = deque(maxlen=5)

class VirtualMouse:
    """Enhanced Virtual Mouse with advanced gesture recognition and smooth tracking"""
    
    def __init__(self, config: GestureConfig = None):
        self.config = config or GestureConfig()
        self.screen_width, self.screen_height = pyautogui.size()
        self.hand_state = HandState()
        
        # Initialize MediaPipe with optimized settings
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Initialize camera with optimized settings
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open camera")
            sys.exit(1)
            
        # Optimize camera settings
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.camera_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.camera_height)
        self.cap.set(cv2.CAP_PROP_FPS, self.config.camera_fps)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        # Performance tracking
        self.frame_count = 0
        self.start_time = time.time()
        self.fps = 0
        
        # Gesture state tracking
        self.last_gesture_time = 0
        self.gesture_cooldown = self.config.gesture_cooldown
        
    def calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """Calculate Euclidean distance between two points"""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def smooth_position(self, new_pos: Tuple[float, float]) -> Tuple[float, float]:
        """Apply smoothing filter to reduce jitter"""
        if self.hand_state.last_position == (0, 0):
            self.hand_state.last_position = new_pos
            return new_pos
            
        smoothed_x = (self.config.smoothing_factor * new_pos[0] + 
                     (1 - self.config.smoothing_factor) * self.hand_state.last_position[0])
        smoothed_y = (self.config.smoothing_factor * new_pos[1] + 
                     (1 - self.config.smoothing_factor) * self.hand_state.last_position[1])
        
        self.hand_state.last_position = (smoothed_x, smoothed_y)
        return (smoothed_x, smoothed_y)
    
    def detect_gesture(self, landmarks) -> Optional[str]:
        """Advanced gesture detection with confidence scoring"""
        try:
            # Get key landmark positions
            index_tip = landmarks[8]
            thumb_tip = landmarks[4]
            middle_tip = landmarks[12]
            index_mcp = landmarks[5]
            ring_tip = landmarks[16]
            pinky_tip = landmarks[20]
            
            # Calculate distances in normalized coordinates
            thumb_index_dist = self.calculate_distance(
                (thumb_tip.x, thumb_tip.y), 
                (index_tip.x, index_tip.y)
            )
            index_middle_dist = self.calculate_distance(
                (index_tip.x, index_tip.y), 
                (middle_tip.x, middle_tip.y)
            )
            thumb_index_mcp_dist = self.calculate_distance(
                (thumb_tip.x, thumb_tip.y), 
                (index_mcp.x, index_mcp.y)
            )
            thumb_ring_dist = self.calculate_distance(
                (thumb_tip.x, thumb_tip.y), 
                (ring_tip.x, ring_tip.y)
            )
            thumb_pinky_dist = self.calculate_distance(
                (thumb_tip.x, thumb_tip.y), 
                (pinky_tip.x, pinky_tip.y)
            )
            
            current_time = time.time()
            
            # Gesture detection with cooldown
            if current_time - self.last_gesture_time < self.gesture_cooldown:
                return self.hand_state.gesture_active
            
            # Detect gestures based on distances
            if thumb_index_dist < self.config.click_threshold:
                self.last_gesture_time = current_time
                self.hand_state.gesture_active = "click"
                return "click"
            elif index_middle_dist < self.config.double_click_threshold:
                self.last_gesture_time = current_time
                self.hand_state.gesture_active = "double_click"
                return "double_click"
            elif thumb_index_mcp_dist < self.config.right_click_threshold:
                self.last_gesture_time = current_time
                self.hand_state.gesture_active = "right_click"
                return "right_click"
            elif thumb_ring_dist < self.config.scroll_threshold:
                self.last_gesture_time = current_time
                self.hand_state.gesture_active = "scroll_up"
                return "scroll_up"
            elif thumb_pinky_dist < self.config.scroll_threshold:
                self.last_gesture_time = current_time
                self.hand_state.gesture_active = "scroll_down"
                return "scroll_down"
            elif thumb_index_dist < self.config.move_threshold:
                self.hand_state.gesture_active = "move"
                return "move"
            else:
                self.hand_state.gesture_active = None
                return None
                
        except (IndexError, AttributeError):
            return None
    
    def execute_action(self, gesture: str, landmarks):
        """Execute mouse actions based on detected gestures"""
        current_time = time.time()
        
        if gesture == "click" and current_time - self.hand_state.last_click_time > self.config.action_cooldown:
            pyautogui.click()
            self.hand_state.last_click_time = current_time
            print("🖱️ Click")
            
        elif gesture == "double_click" and current_time - self.hand_state.last_click_time > self.config.action_cooldown:
            pyautogui.doubleClick()
            self.hand_state.last_click_time = current_time
            print("🖱️ Double Click")
            
        elif gesture == "right_click" and current_time - self.hand_state.last_click_time > self.config.action_cooldown:
            pyautogui.rightClick()
            self.hand_state.last_click_time = current_time
            print("🖱️ Right Click")
            
        elif gesture == "scroll_up":
            pyautogui.scroll(3)
            print("⬆️ Scroll Up")
            
        elif gesture == "scroll_down":
            pyautogui.scroll(-3)
            print("⬇️ Scroll Down")
            
        elif gesture == "move":
            # Get index finger position
            index_tip = landmarks[8]
            screen_x = int(index_tip.x * self.screen_width)
            screen_y = int(index_tip.y * self.screen_height)
            
            # Apply smoothing
            smoothed_pos = self.smooth_position((screen_x, screen_y))
            
            # Move mouse with bounds checking
            bounded_x = max(0, min(self.screen_width - 1, int(smoothed_pos[0])))
            bounded_y = max(0, min(self.screen_height - 1, int(smoothed_pos[1])))
            
            pyautogui.moveTo(bounded_x, bounded_y)
    
    def draw_interface(self, frame, landmarks, gesture):
        """Draw enhanced visual interface"""
        # Draw hand landmarks with custom styling
        self.mp_drawing.draw_landmarks(
            frame, landmarks, self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
        )
        
        # Highlight key points
        key_points = [8, 4, 12, 5, 16, 20]  # Index, thumb, middle, index base, ring, pinky
        colors = [(255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 165, 0), (0, 255, 0), (255, 0, 0)]
        
        for i, point_id in enumerate(key_points):
            if point_id < len(landmarks):
                x = int(landmarks[point_id].x * frame.shape[1])
                y = int(landmarks[point_id].y * frame.shape[0])
                cv2.circle(frame, (x, y), 8, colors[i], -1)
                cv2.circle(frame, (x, y), 10, (255, 255, 255), 2)
        
        # Draw gesture indicator
        if gesture:
            gesture_text = gesture.replace('_', ' ').title()
            cv2.rectangle(frame, (10, 10), (250, 60), (0, 0, 0), -1)
            cv2.putText(frame, f"Gesture: {gesture_text}", (20, 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Draw FPS counter
        self.frame_count += 1
        if self.frame_count % 30 == 0:
            self.fps = 30 / (time.time() - self.start_time)
            self.start_time = time.time()
        
        cv2.putText(frame, f"FPS: {self.fps:.1f}", (frame.shape[1] - 100, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Draw instructions
        instructions = [
            "Move: Thumb + Index close",
            "Click: Thumb + Index very close", 
            "Double Click: Index + Middle close",
            "Right Click: Thumb + Index base close",
            "Scroll: Thumb + Ring/Pinky close",
            "Press 'q' to quit"
        ]
        
        for i, instruction in enumerate(instructions):
            y_pos = frame.shape[0] - 140 + i * 22
            cv2.putText(frame, instruction, (10, y_pos), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    
    def run(self):
        """Main execution loop"""
        print("🚀 Virtual Mouse Started!")
        print("📹 Position your hand in front of the camera")
        print("✋ Make gestures to control the mouse")
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Could not read frame")
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Convert to RGB for MediaPipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)
                
                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0]
                    landmarks = hand_landmarks.landmark
                    
                    # Detect gesture
                    gesture = self.detect_gesture(landmarks)
                    
                    # Execute action
                    if gesture:
                        self.execute_action(gesture, landmarks)
                    
                    # Draw interface
                    self.draw_interface(frame, hand_landmarks, gesture)
                else:
                    # Show "No hand detected" message
                    cv2.putText(frame, "No hand detected", (frame.shape[1]//2 - 100, frame.shape[0]//2), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # Display frame
                cv2.imshow('Enhanced Virtual Mouse', frame)
                
                # Exit on 'q' key
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        cv2.destroyAllWindows()
        self.hands.close()
        print("✅ Resources cleaned up")

def main():
    """Entry point"""
    # Load configuration from file or create default
    try:
        config = GestureConfig.load_from_file()
        print("✅ Configuration loaded from file")
    except:
        print("⚠️ Using default configuration")
        config = GestureConfig()
    
    # Create and run virtual mouse
    virtual_mouse = VirtualMouse(config)
    virtual_mouse.run()

if __name__ == "__main__":
    main()
