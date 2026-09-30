import cv2
import mediapipe as mp
import math

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

print("✅ Pinch detection started!")
print("Press Q to stop.")

# --------------------------------
# Main loop
# --------------------------------

while True:

    success, frame = camera.read()

    if not success:
        print("❌ Could not read camera frame.")
        break

    # Mirror the camera
    frame = cv2.flip(frame, 1)

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hand
    results = hands.process(rgb_frame)

    # --------------------------------
    # If hand detected
    # --------------------------------

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Draw hand landmarks
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            h, w, _ = frame.shape

            # Thumb tip = landmark 4
            thumb = hand_landmarks.landmark[4]

            # Index fingertip = landmark 8
            index = hand_landmarks.landmark[8]

            # Convert to pixel coordinates
            thumb_x = int(thumb.x * w)
            thumb_y = int(thumb.y * h)

            index_x = int(index.x * w)
            index_y = int(index.y * h)

            # --------------------------------
            # Calculate distance
            # --------------------------------

            distance = math.sqrt(
                (index_x - thumb_x) ** 2 +
                (index_y - thumb_y) ** 2
            )

            # --------------------------------
            # Draw line between thumb & index
            # --------------------------------

            cv2.line(
                frame,
                (thumb_x, thumb_y),
                (index_x, index_y),
                (255, 255, 255),
                3
            )

            # --------------------------------
            # Display distance
            # --------------------------------

            cv2.putText(
                frame,
                f"Distance: {int(distance)}",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

            # --------------------------------
            # Detect PINCH
            # --------------------------------

            if distance < 40:

                status = "PINCH DETECTED"

                cv2.putText(
                    frame,
                    status,
                    (20, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    3
                )

            else:

                status = "OPEN"

                cv2.putText(
                    frame,
                    status,
                    (20, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

            # --------------------------------
            # Draw fingertip circles
            # --------------------------------

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

    # --------------------------------
    # Show camera
    # --------------------------------

    cv2.imshow(
        "AI Gesture Control - Pinch Test",
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

print("Pinch detection stopped.")