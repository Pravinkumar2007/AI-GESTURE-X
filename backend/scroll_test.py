import cv2
import mediapipe as mp
import pyautogui
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
# Webcam
# --------------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Camera could not be opened.")
    exit()

print("✅ Scroll control started!")
print("✌️ Two fingers + UP/DOWN = Scroll")
print("Press Q to stop.")

# Previous hand position
previous_y = None

# Prevent extremely fast scrolling
last_scroll_time = 0
scroll_cooldown = 0.05

# --------------------------------
# Main loop
# --------------------------------

while True:

    success, frame = camera.read()

    if not success:
        print("❌ Camera frame failed.")
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    frame_height, frame_width, _ = frame.shape

    # BGR → RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = hands.process(rgb_frame)

    gesture = "NO HAND"

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
        # Finger states
        # --------------------------------

        index_open = (
            landmarks[8].y <
            landmarks[6].y
        )

        middle_open = (
            landmarks[12].y <
            landmarks[10].y
        )

        ring_open = (
            landmarks[16].y <
            landmarks[14].y
        )

        pinky_open = (
            landmarks[20].y <
            landmarks[18].y
        )

        # --------------------------------
        # Detect TWO FINGERS
        # --------------------------------

        two_fingers = (
            index_open
            and middle_open
            and not ring_open
            and not pinky_open
        )

        # --------------------------------
        # Two-finger mode
        # --------------------------------

        if two_fingers:

            gesture = "SCROLL MODE"

            # Use wrist position
            wrist = landmarks[0]

            current_y = int(
                wrist.y * frame_height
            )

            # --------------------------------
            # Compare previous position
            # --------------------------------

            if previous_y is not None:

                difference = current_y - previous_y

                current_time = time.time()

                # Hand moving UP
                if (
                    difference < -15
                    and current_time - last_scroll_time
                    > scroll_cooldown
                ):

                    pyautogui.scroll(8)
                    print("SCROLL UP COMMAND SENT")

                    last_scroll_time = current_time

                    print("⬆️ SCROLL UP")

                # Hand moving DOWN
                elif (
                    difference > 15
                    and current_time - last_scroll_time
                    > scroll_cooldown
                ):

                    pyautogui.scroll(-8)
                    print("SCROLL DOWN COMMAND SENT")

                    last_scroll_time = current_time

                    print("⬇️ SCROLL DOWN")

            previous_y = current_y

        else:

            gesture = "OTHER"

            # Reset position when ✌️ disappears
            previous_y = None

    else:

        gesture = "NO HAND"

        previous_y = None

    # --------------------------------
    # Display status
    # --------------------------------

    cv2.putText(
        frame,
        gesture,
        (20, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        3
    )

    # --------------------------------
    # Show camera
    # --------------------------------

    cv2.imshow(
        "AI Gesture Control - Scroll Test",
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

print("Scroll control stopped.")