import cv2
import mediapipe as mp
import pyautogui
import time


# ============================================================
# MEDIAPIPE SETUP
# ============================================================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


# ============================================================
# CAMERA
# ============================================================

camera = cv2.VideoCapture(0)

print("Media Control Started")
print("✌️ Two fingers = Play / Pause")
print("Press Q to exit")


# Prevent repeated actions
last_action_time = 0
cooldown = 1.0


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    success, frame = camera.read()

    if not success:
        print("Camera error!")
        break

    # Mirror image
    frame = cv2.flip(frame, 1)

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hand
    result = hands.process(rgb_frame)


    if result.multi_hand_landmarks:

        for hand_landmarks in result.multi_hand_landmarks:

            # Draw 21 landmarks
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )


            # ------------------------------------------------
            # GET FINGER LANDMARKS
            # ------------------------------------------------

            thumb_tip = hand_landmarks.landmark[4]

            index_tip = hand_landmarks.landmark[8]
            index_pip = hand_landmarks.landmark[6]

            middle_tip = hand_landmarks.landmark[12]
            middle_pip = hand_landmarks.landmark[10]

            ring_tip = hand_landmarks.landmark[16]
            ring_pip = hand_landmarks.landmark[14]

            pinky_tip = hand_landmarks.landmark[20]
            pinky_pip = hand_landmarks.landmark[18]


            # ------------------------------------------------
            # FINGER UP DETECTION
            # ------------------------------------------------

            index_up = index_tip.y < index_pip.y
            middle_up = middle_tip.y < middle_pip.y
            ring_up = ring_tip.y < ring_pip.y
            pinky_up = pinky_tip.y < pinky_pip.y


            # =================================================
            # ✌️ TWO FINGER GESTURE
            # =================================================

            two_fingers = (
                index_up
                and middle_up
                and not ring_up
                and not pinky_up
            )


            if two_fingers:

                current_time = time.time()

                if current_time - last_action_time > cooldown:

                    # Play / Pause media
                    pyautogui.press("playpause")

                    print("✌️ PLAY / PAUSE")

                    last_action_time = current_time


                cv2.putText(
                    frame,
                    "PLAY / PAUSE",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )


    # ========================================================
    # SHOW CAMERA
    # ========================================================

    cv2.imshow("AI Gesture - Media Control", frame)


    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ============================================================
# CLEANUP
# ============================================================

camera.release()
cv2.destroyAllWindows()
hands.close()

print("Media Control Stopped.")