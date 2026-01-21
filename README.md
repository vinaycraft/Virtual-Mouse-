# Virtual Mouse

A hand gesture-controlled virtual mouse using MediaPipe and OpenCV.

## Features

- **Move Cursor**: Control mouse movement with hand gestures
- **Left Click**: Thumb and index finger close together
- **Double Click**: Index and middle fingers close together  
- **Right Click**: Thumb and index finger base close together
- **Scroll Up/Down**: Ring finger + thumb or thumb + pinky close together

## Requirements

- Python 3.7+
- OpenCV
- MediaPipe
- PyAutoGUI

## Installation

```bash
pip install opencv-python mediapipe pyautogui
```

## Usage

```bash
python virtual_mouse.py
```

Press 'q' to exit the application.

## How it Works

The application uses your computer's camera to detect hand landmarks through MediaPipe. Different finger combinations trigger different mouse actions:

- **Index finger (landmark 8)**: Controls cursor position
- **Thumb (landmark 4)**: Used in combination with other fingers for clicks
- **Middle finger (landmark 12)**: Double click gesture
- **Index base (landmark 5)**: Right click gesture
- **Ring finger (landmark 16)**: Scroll up gesture
- **Pinky finger (landmark 20)**: Scroll down gesture

## Configuration

You can adjust gesture sensitivity by modifying the threshold constants at the top of the script:

- `CLICK_THRESHOLD`: Distance for left click (default: 20)
- `DOUBLE_CLICK_THRESHOLD`: Distance for double click (default: 10)
- `RIGHT_CLICK_THRESHOLD`: Distance for right click (default: 20)
- `SCROLL_THRESHOLD`: Distance for scroll gestures (default: 20)
- `MOVE_THRESHOLD`: Distance for mouse movement (default: 100)
- `ACTION_DELAY`: Delay between actions (default: 0.2 seconds)

## License

MIT License
