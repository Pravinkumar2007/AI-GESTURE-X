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

print("✅ Movement detection started!")
print("Move your hand UP and DOWN.")
print("Press Q to stop.")

# Previous hand position
previous_y = None

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

    movement = "STABLE"

    # --------------------------------
    # If hand detected
    # --------------------------------

    if results.multi_hand_landmarks:

        hand_landmarks = results.multi_hand_landmarks[0]

        # Use wrist landmark
        wrist = hand_landmarks.landmark[0]

        # Convert normalized Y to pixels
        h, w, _ = frame.shape

        current_y = int(wrist.y * h)

        # Draw landmarks
        mp_draw.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

        # --------------------------------
        # Calculate movement
        # --------------------------------

        if previous_y is not None:

            difference = current_y - previous_y

            # Remember:
            # Smaller Y = UP
            # Larger Y = DOWN

            if difference < -10:
                movement = "MOVING UP"

            elif difference > 10:
                movement = "MOVING DOWN"

            else:
                movement = "STABLE"

        # Save current position
        previous_y = current_y

        # --------------------------------
        # Display Y position
        # --------------------------------

        cv2.putText(
            frame,
            f"Y Position: {current_y}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    else:
        # No hand detected
        previous_y = None
        movement = "NO HAND"

    # --------------------------------
    # Display movement
    # --------------------------------

    cv2.putText(
        frame,
        movement,
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        3
    )

    # --------------------------------
    # Show camera
    # --------------------------------

    cv2.imshow(
        "AI Gesture Control - Movement Test",
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

print("Movement detection stopped.")