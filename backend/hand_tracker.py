import cv2
import mediapipe as mp

print("HAND_TRACKER.PY LOADED")


class HandTracker:

    def __init__(self):

        # =====================================================
        # MEDIAPIPE
        # =====================================================

        self.mp_hands = mp.solutions.hands

        self.mp_draw = mp.solutions.drawing_utils

        # =====================================================
        # HAND DETECTOR
        # =====================================================

        self.hands = self.mp_hands.Hands(

            static_image_mode=False,

            max_num_hands=1,

            model_complexity=1,

            min_detection_confidence=0.7,

            min_tracking_confidence=0.7
        )

        print("HandTracker initialized")

    # =========================================================
    # PROCESS FRAME
    # =========================================================

    def process(self, frame):

        try:

            # -------------------------------------------------
            # BGR → RGB
            # -------------------------------------------------

            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            # -------------------------------------------------
            # MAKE FRAME NON-WRITABLE
            # Improves MediaPipe performance
            # -------------------------------------------------

            rgb_frame.flags.writeable = False

            # -------------------------------------------------
            # PROCESS HAND
            # -------------------------------------------------

            results = self.hands.process(
                rgb_frame
            )

            # -------------------------------------------------
            # RETURN RESULT
            # -------------------------------------------------

            return results

        except Exception as error:

            print(
                "HAND TRACKING ERROR:",
                error
            )

            return None

    # =========================================================
    # DRAW LANDMARKS
    # =========================================================

    def draw_landmarks(
        self,
        frame,
        results
    ):

        try:

            if results is None:

                return frame

            if results.multi_hand_landmarks:

                for hand in results.multi_hand_landmarks:

                    self.mp_draw.draw_landmarks(

                        frame,

                        hand,

                        self.mp_hands.HAND_CONNECTIONS
                    )

            return frame

        except Exception as error:

            print(
                "DRAW LANDMARK ERROR:",
                error
            )

            return frame

    # =========================================================
    # GET LANDMARKS
    # =========================================================

    def get_landmarks(self, results):

        try:

            if results is None:

                return None

            if not results.multi_hand_landmarks:

                return None

            return (
                results
                .multi_hand_landmarks[0]
                .landmark
            )

        except Exception as error:

            print(
                "GET LANDMARK ERROR:",
                error
            )

            return None

    # =========================================================
    # HAND DETECTED
    # =========================================================

    def hand_detected(self, results):

        try:

            if results is None:

                return False

            return bool(
                results.multi_hand_landmarks
            )

        except Exception as error:

            print(
                "HAND DETECTION ERROR:",
                error
            )

            return False

    # =========================================================
    # CLOSE
    # =========================================================

    def close(self):

        try:

            self.hands.close()

            print(
                "HandTracker closed"
            )

        except Exception as error:

            print(
                "HAND TRACKER CLOSE ERROR:",
                error
            )