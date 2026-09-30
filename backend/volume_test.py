import cv2
import mediapipe as mp
import time

from pycaw.pycaw import AudioUtilities


# ==========================================
# WINDOWS VOLUME SETUP
# ==========================================

device = AudioUtilities.GetSpeakers()
volume_control = device.EndpointVolume


# ==========================================
# MEDIAPIPE SETUP
# ==========================================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


# ==========================================
# CAMERA
# ==========================================

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Camera could not be opened.")
    exit()

print("----------------------------------")
print("🔊 THUMB VOLUME CONTROL")
print("----------------------------------")
print("👍 = Volume UP")
print("👎 = Volume DOWN")
print("✋ = No volume action")
print("Press Q to exit.")
print("----------------------------------")


# ==========================================
# SETTINGS
# ==========================================

last_action_time = 0

# Time between volume changes
cooldown = 0.35

# Volume change amount
volume_step = 0.03


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    success, frame = camera.read()

    if not success:
        print("❌ Camera frame failed.")
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    height, width, _ = frame.shape

    # Convert BGR → RGB
    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = hands.process(rgb)

    status = "NO HAND"


    # ======================================
    # HAND DETECTED
    # ======================================

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        landmarks = hand.landmark

        # Draw 21 landmarks
        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )


        # ==================================
        # FINGER STATES
        # ==================================

        index_folded = (
            landmarks[8].y >
            landmarks[6].y
        )

        middle_folded = (
            landmarks[12].y >
            landmarks[10].y
        )

        ring_folded = (
            landmarks[16].y >
            landmarks[14].y
        )

        pinky_folded = (
            landmarks[20].y >
            landmarks[18].y
        )


        # ==================================
        # THUMB POSITION
        # ==================================

        thumb_tip_y = landmarks[4].y
        thumb_ip_y = landmarks[3].y
        thumb_mcp_y = landmarks[2].y


        # ==================================
        # THUMBS UP / DOWN
        # ==================================

        other_fingers_folded = (
            index_folded
            and middle_folded
            and ring_folded
            and pinky_folded
        )


        current_time = time.time()


        if other_fingers_folded:

            # --------------------------------
            # 👍 THUMBS UP
            # --------------------------------

            if (
                thumb_tip_y < thumb_ip_y
                and thumb_tip_y < thumb_mcp_y
            ):

                status = "👍 VOLUME UP"

                if current_time - last_action_time > cooldown:

                    current_volume = (
                        volume_control.GetMasterVolumeLevelScalar()
                    )

                    new_volume = min(
                        1.0,
                        current_volume + volume_step
                    )

                    volume_control.SetMasterVolumeLevelScalar(
                        new_volume,
                        None
                    )

                    print(
                        "🔊 Volume UP:",
                        int(new_volume * 100),
                        "%"
                    )

                    last_action_time = current_time


            # --------------------------------
            # 👎 THUMBS DOWN
            # --------------------------------

            elif (
                thumb_tip_y > thumb_ip_y
                and thumb_tip_y > thumb_mcp_y
            ):

                status = "👎 VOLUME DOWN"

                if current_time - last_action_time > cooldown:

                    current_volume = (
                        volume_control.GetMasterVolumeLevelScalar()
                    )

                    new_volume = max(
                        0.0,
                        current_volume - volume_step
                    )

                    volume_control.SetMasterVolumeLevelScalar(
                        new_volume,
                        None
                    )

                    print(
                        "🔉 Volume DOWN:",
                        int(new_volume * 100),
                        "%"
                    )

                    last_action_time = current_time

            else:

                status = "✊ HAND"


        else:

            status = "OTHER GESTURE"


    # ======================================
    # DISPLAY STATUS
    # ======================================

    cv2.putText(
        frame,
        status,
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2
    )


    # ======================================
    # SHOW CAMERA
    # ======================================

    cv2.imshow(
        "AI Gesture Control - Volume Test",
        frame
    )


    # ======================================
    # QUIT
    # ======================================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ==========================================
# CLEANUP
# ==========================================

camera.release()
cv2.destroyAllWindows()
hands.close()

print("🔊 Volume control stopped.")