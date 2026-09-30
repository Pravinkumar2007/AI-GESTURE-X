import cv2
import mediapipe as mp
import pyautogui
import math
import time

# --------------------------------
# MediaPipe setup
# --------------------------------

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# --------------------------------
# Screen size
# --------------------------------

screen_width, screen_height = pyautogui.size()

# --------------------------------
# Webcam
# --------------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Camera could not be opened.")
    exit()

print("✅ Mouse + Click control started!")
print("☝️ Move cursor")
print("🤏 Pinch = Left Click")
print("Press Q to stop.")

# --------------------------------
# Click cooldown
# --------------------------------

last_click_time = 0
click_cooldown = 0.5

# --------------------------------
# Main loop
# --------------------------------

while True:

    success, frame = camera.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    frame_height, frame_width, _ = frame.shape

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]
        landmarks = hand.landmark

        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

        # --------------------------------
        # Finger states
        # --------------------------------

        index_open = landmarks[8].y < landmarks[6].y

        middle_open = landmarks[12].y < landmarks[10].y
        ring_open = landmarks[16].y < landmarks[14].y
        pinky_open = landmarks[20].y < landmarks[18].y

        # --------------------------------
        # Index fingertip
        # --------------------------------

        index = landmarks[8]

        index_x = int(index.x * frame_width)
        index_y = int(index.y * frame_height)

        # --------------------------------
        # Cursor movement
        # --------------------------------

        if (
            index_open
            and middle_open
            and not ring_open
            and not pinky_open
        ):

            screen_x = int(
                index.x * screen_width
            )

            screen_y = int(
                index.y * screen_height
            )

            pyautogui.moveTo(
                screen_x,
                screen_y,
                duration=7.0
            )

        # --------------------------------
        # Thumb + Index distance
        # --------------------------------

        thumb = landmarks[4]

        thumb_x = int(thumb.x * frame_width)
        thumb_y = int(thumb.y * frame_height)

        distance = math.sqrt(
            (index_x - thumb_x) ** 2 +
            (index_y - thumb_y) ** 2
        )

        # Draw line
        cv2.line(
            frame,
            (thumb_x, thumb_y),
            (index_x, index_y),
            (255, 255, 255),
            2
        )

        # --------------------------------
        # PINCH → CLICK
        # --------------------------------

        current_time = time.time()

        if distance < 40:

            cv2.putText(
                frame,
                "PINCH",
                (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                3
            )

            if current_time - last_click_time > click_cooldown:

                pyautogui.click()

                last_click_time = current_time

                print("🖱️ LEFT CLICK")

        else:

            cv2.putText(
                frame,
                "MOVE",
                (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                3
            )

    # --------------------------------
    # Display
    # --------------------------------

    cv2.imshow(
        "AI Gesture Control - Mouse Click Test",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# --------------------------------
# Cleanup
# --------------------------------

camera.release()
cv2.destroyAllWindows()
hands.close()

print("Mouse control stopped.")