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
# Open webcam
# --------------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Camera could not be opened.")
    exit()

print("✅ Open Palm detection started!")
print("Show an open palm ✋")
print("Press Q to stop.")


# --------------------------------
# Main loop
# --------------------------------

while True:

    success, frame = camera.read()

    if not success:
        print("❌ Could not read camera frame.")
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hand
    results = hands.process(rgb_frame)

    gesture = "NO HAND"

    # --------------------------------
    # If hand detected
    # --------------------------------

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        # Draw landmarks
        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

        # Get important landmark positions
        landmarks = hand.landmark

        # --------------------------------
        # Finger detection
        # --------------------------------

        # Index: 8 compared with 6
        index_open = landmarks[8].y < landmarks[6].y

        # Middle: 12 compared with 10
        middle_open = landmarks[12].y < landmarks[10].y

        # Ring: 16 compared with 14
        ring_open = landmarks[16].y < landmarks[14].y

        # Pinky: 20 compared with 18
        pinky_open = landmarks[20].y < landmarks[18].y

        # --------------------------------
        # Open palm condition
        # --------------------------------

        if (
            index_open
            and middle_open
            and ring_open
            and pinky_open
        ):

            gesture = "OPEN PALM - STOP"

        else:

            gesture = "OTHER GESTURE"

    # --------------------------------
    # Display gesture
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
        "AI Gesture Control - Palm Test",
        frame
    )

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# --------------------------------
# Cleanup
# --------------------------------

camera.release()
cv2.destroyAllWindows()
hands.close()

print("Palm detection stopped.")