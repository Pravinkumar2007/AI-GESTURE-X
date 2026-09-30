import cv2
import mediapipe as mp
import pyautogui

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

print("Screen size:", screen_width, "x", screen_height)

# --------------------------------
# Webcam
# --------------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Camera could not be opened.")
    exit()

print("✅ Mouse control started!")
print("Show ONLY your index finger.")
print("Move your finger to control the mouse.")
print("Press Q to stop.")

# --------------------------------
# Main loop
# --------------------------------

while True:

    success, frame = camera.read()

    if not success:
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    # Get camera dimensions
    frame_height, frame_width, _ = frame.shape

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hand
    results = hands.process(rgb_frame)

    # --------------------------------
    # Hand detected
    # --------------------------------

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]
        landmarks = hand.landmark

        # Draw landmarks
        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

        # --------------------------------
        # Check index finger
        # --------------------------------

        index_open = landmarks[8].y < landmarks[6].y

        middle_open = landmarks[12].y < landmarks[10].y
        ring_open = landmarks[16].y < landmarks[14].y
        pinky_open = landmarks[20].y < landmarks[18].y

        # Only index finger should be open
        if (
            index_open
            and middle_open
            and not ring_open
            and not pinky_open
        ):

            # Index fingertip
            index = landmarks[8]
            middle = landmarks[12]

            # Convert normalized coordinates to camera pixels
            camera_x = int(index.x * frame_width)
            camera_y = int(index.y * frame_height)

            # --------------------------------
            # Map camera coordinates
            # to screen coordinates
            # --------------------------------

            screen_x = int(
                index.x * screen_width
            )

            screen_y = int(
                index.y * screen_height
            )

            # --------------------------------
            # Move mouse
            # --------------------------------

            pyautogui.moveTo(
                screen_x,
                screen_y,
                duration=0.01
            )

            # Draw fingertip
            cv2.circle(
                frame,
                (camera_x, camera_y),
                12,
                (0, 255, 0),
                -1
            )

            cv2.putText(
                frame,
                "MOUSE MODE",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                3
            )

    # --------------------------------
    # Display camera
    # --------------------------------

    cv2.imshow(
        "AI Gesture Control - Mouse Test",
        frame
    )

    # Q = quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# --------------------------------
# Cleanup
# --------------------------------

camera.release()
cv2.destroyAllWindows()
hands.close()

print("Mouse control stopped.")