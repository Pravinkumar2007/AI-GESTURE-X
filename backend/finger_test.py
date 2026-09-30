import cv2
import mediapipe as mp

# -----------------------------
# MediaPipe setup
# -----------------------------

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# -----------------------------
# Open webcam
# -----------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Camera could not be opened.")
    exit()

print("✅ Finger detection started!")
print("Press Q to stop.")

# -----------------------------
# Main loop
# -----------------------------

while True:

    success, frame = camera.read()

    if not success:
        print("❌ Could not read camera frame.")
        break

    # Flip camera so it behaves like a mirror
    frame = cv2.flip(frame, 1)

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands
    results = hands.process(rgb_frame)

    # -----------------------------
    # If hand detected
    # -----------------------------

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Draw all 21 landmarks
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Get landmark positions
            h, w, _ = frame.shape

            # Important fingertip positions
            thumb = hand_landmarks.landmark[4]
            index = hand_landmarks.landmark[8]
            middle = hand_landmarks.landmark[12]
            ring = hand_landmarks.landmark[16]
            pinky = hand_landmarks.landmark[20]

            # Convert normalized coordinates to pixels
            thumb_x = int(thumb.x * w)
            thumb_y = int(thumb.y * h)

            index_x = int(index.x * w)
            index_y = int(index.y * h)

            # -----------------------------
            # Display fingertip labels
            # -----------------------------

            cv2.putText(
                frame,
                "THUMB",
                (thumb_x + 10, thumb_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "INDEX",
                (index_x + 10, index_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2
            )

            # -----------------------------
            # Draw circles on fingertips
            # -----------------------------

            cv2.circle(
                frame,
                (thumb_x, thumb_y),
                10,
                (0, 255, 0),
                -1
            )

            cv2.circle(
                frame,
                (index_x, index_y),
                10,
                (255, 0, 0),
                -1
            )

    # -----------------------------
    # Show camera
    # -----------------------------

    cv2.imshow("AI Gesture Control - Finger Test", frame)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# -----------------------------
# Cleanup
# -----------------------------

camera.release()
cv2.destroyAllWindows()
hands.close()

print("Finger detection stopped.")