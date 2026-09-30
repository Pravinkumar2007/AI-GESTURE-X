import cv2
import mediapipe as mp

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

print("✅ Gesture detection started!")
print("Try: ☝️  ✌️  ✊  ✋")
print("Press Q to stop.")


# --------------------------------
# Main loop
# --------------------------------

while True:

    success, frame = camera.read()

    if not success:
        print("❌ Could not read camera frame.")
        break

    # Mirror image
    frame = cv2.flip(frame, 1)

    # BGR → RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hand
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
        # Detect fingers
        # --------------------------------

        index_open = landmarks[8].y < landmarks[6].y

        middle_open = landmarks[12].y < landmarks[10].y

        ring_open = landmarks[16].y < landmarks[14].y

        pinky_open = landmarks[20].y < landmarks[18].y

        # --------------------------------
        # Count extended fingers
        # --------------------------------

        fingers = sum([
            index_open,
            middle_open,
            ring_open,
            pinky_open
        ])

        # --------------------------------
        # Gesture recognition
        # --------------------------------

        if fingers == 0:

            gesture = "✊ FIST"

        elif (
            index_open
            and not middle_open
            and not ring_open
            and not pinky_open
        ):

            gesture = "☝️ INDEX"

        elif (
            index_open
            and middle_open
            and not ring_open
            and not pinky_open
        ):

            gesture = "✌️ TWO FINGERS"

        elif (
            index_open
            and middle_open
            and ring_open
            and pinky_open
        ):

            gesture = "✋ OPEN PALM"

        else:

            gesture = "OTHER"

    # --------------------------------
    # Display gesture
    # --------------------------------

    cv2.putText(
        frame,
        gesture,
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        3
    )

    # --------------------------------
    # Display
    # --------------------------------

    cv2.imshow(
        "AI Gesture Control - Gesture Test",
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

print("Gesture detection stopped.")