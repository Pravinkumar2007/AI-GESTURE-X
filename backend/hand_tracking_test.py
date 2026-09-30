import cv2
import mediapipe as mp

# -----------------------------
# MediaPipe setup
# -----------------------------
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# -----------------------------
# Open webcam
# -----------------------------
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Camera could not be opened.")
    exit()

print("✅ Hand tracking started!")
print("Show your hand to the camera.")
print("Press Q to quit.")

# -----------------------------
# Main loop
# -----------------------------
while True:

    success, frame = camera.read()

    if not success:
        print("❌ Could not read camera frame.")
        break

    # Flip image so it behaves like a mirror
    frame = cv2.flip(frame, 1)

    # OpenCV uses BGR
    # MediaPipe expects RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands
    results = hands.process(rgb_frame)

    # -----------------------------
    # Draw hand landmarks
    # -----------------------------
    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    # Display
    cv2.imshow("AI Gesture Control - Hand Tracking", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# -----------------------------
# Cleanup
# -----------------------------
camera.release()
cv2.destroyAllWindows()
hands.close()

print("Hand tracking stopped.")