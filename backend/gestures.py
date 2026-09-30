import math

print("GESTURES.PY LOADED")


class GestureDetector:

    def __init__(self):
        print("GestureDetector initialized")

    # =========================================================
    # DISTANCE BETWEEN TWO LANDMARKS
    # =========================================================

    def distance(self, p1, p2):
        return math.sqrt(
            (p1.x - p2.x) ** 2 +
            (p1.y - p2.y) ** 2
        )

    # =========================================================
    # CHECK FINGER UP
    # =========================================================

    def finger_up(self, landmarks, tip, pip):

        return (
            landmarks[tip].y <
            landmarks[pip].y
        )

    # =========================================================
    # CHECK THUMB UP
    # =========================================================

    def thumb_is_up(self, landmarks):

        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]

        return (
            thumb_tip.y <
            thumb_ip.y - 0.02
        )

    # =========================================================
    # CHECK THUMB DOWN
    # =========================================================

    def thumb_is_down(self, landmarks):

        thumb_tip = landmarks[4]
        thumb_ip = landmarks[3]

        return (
            thumb_tip.y >
            thumb_ip.y + 0.02
        )

    # =========================================================
    # DETECT GESTURE
    # =========================================================

    def detect(self, landmarks):

        # -----------------------------------------------------
        # SAFETY CHECK
        # -----------------------------------------------------

        if landmarks is None:
            return "NO HAND"

        if len(landmarks) < 21:
            return "UNKNOWN"

        # =====================================================
        # FINGER STATUS
        # =====================================================

        index_up = self.finger_up(
            landmarks,
            8,
            6
        )

        middle_up = self.finger_up(
            landmarks,
            12,
            10
        )

        ring_up = self.finger_up(
            landmarks,
            16,
            14
        )

        pinky_up = self.finger_up(
            landmarks,
            20,
            18
        )

        # =====================================================
        # THUMB STATUS
        # =====================================================

        thumb_up = self.thumb_is_up(
            landmarks
        )

        thumb_down = self.thumb_is_down(
            landmarks
        )

        # =====================================================
        # COUNT FINGERS
        # =====================================================

        finger_count = 0

        if index_up:
            finger_count += 1

        if middle_up:
            finger_count += 1

        if ring_up:
            finger_count += 1

        if pinky_up:
            finger_count += 1

        # =====================================================
        # THUMBS UP
        #
        # 👍
        # =====================================================

        if (
            thumb_up
            and
            not index_up
            and
            not middle_up
            and
            not ring_up
            and
            not pinky_up
        ):

            return "THUMBS_UP"

        # =====================================================
        # THUMBS DOWN
        #
        # 👎
        # =====================================================

        if (
            thumb_down
            and
            not index_up
            and
            not middle_up
            and
            not ring_up
            and
            not pinky_up
        ):

            return "THUMBS_DOWN"

        # =====================================================
        # OPEN PALM
        #
        # ✋
        #
        # All four fingers + thumb open
        # =====================================================

        if (
            index_up
            and
            middle_up
            and
            ring_up
            and
            pinky_up
        ):

            return "PALM"

        # =====================================================
        # THREE FINGERS
        #
        # 🤟
        #
        # Index + Middle + Ring
        # =====================================================

        if (
            index_up
            and
            middle_up
            and
            ring_up
            and
            not pinky_up
        ):

            return "THREE_FINGERS"

        # =====================================================
        # TWO FINGERS
        #
        # ✌️
        #
        # Index + Middle
        # =====================================================

        if (
            index_up
            and
            middle_up
            and
            not ring_up
            and
            not pinky_up
        ):

            return "TWO_FINGERS"

        # =====================================================
        # INDEX FINGER
        #
        # ☝️
        # =====================================================

        if (
            index_up
            and
            not middle_up
            and
            not ring_up
            and
            not pinky_up
        ):

            return "INDEX"

        # =====================================================
        # PINKY FINGER
        #
        # 🤙 / PINKY
        # =====================================================

        if (
            pinky_up
            and
            not index_up
            and
            not middle_up
            and
            not ring_up
        ):

            return "PINKY"

        # =====================================================
        # FIST
        #
        # ✊
        # =====================================================

        if (
            not index_up
            and
            not middle_up
            and
            not ring_up
            and
            not pinky_up
        ):

            return "FIST"

        # =====================================================
        # UNKNOWN
        # =====================================================

        return "UNKNOWN"