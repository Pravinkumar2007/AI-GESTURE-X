import math


class AirRecognizer:

    def __init__(self):
        pass

    def recognize(self, points):

        if len(points) < 15:
            return None

        # ==========================================
        # BOUNDING BOX
        # ==========================================

        xs = [p[0] for p in points]
        ys = [p[1] for p in points]

        min_x = min(xs)
        max_x = max(xs)

        min_y = min(ys)
        max_y = max(ys)

        width = max_x - min_x
        height = max_y - min_y

        if width < 10 or height < 10:
            return None

        ratio = width / height

        # ==========================================
        # START / END POINT
        # ==========================================

        start = points[0]
        end = points[-1]

        start_end_distance = math.sqrt(
            (end[0] - start[0]) ** 2 +
            (end[1] - start[1]) ** 2
        )

        # ==========================================
        # 1. HORIZONTAL LINE
        # ==========================================

        if ratio > 3:

            return "-"

        # ==========================================
        # 2. VERTICAL LINE
        # ==========================================

        if ratio < 0.33:

            return "I"

        # ==========================================
        # CLOSED SHAPE
        # ==========================================

        closed = (
            start_end_distance <
            min(width, height) * 0.35
        )

        if closed:

            # --------------------------------------
            # O
            # --------------------------------------

            if 0.65 < ratio < 1.5:

                return "O"

            # --------------------------------------
            # C
            # --------------------------------------

            if 0.6 < ratio < 1.6:

                return "C"

        # ==========================================
        # DIAGONAL MOVEMENT
        # ==========================================

        diagonal = (
            width > height * 0.6 and
            height > width * 0.6
        )

        if diagonal:

            # ======================================
            # V
            # ======================================

            middle_index = len(points) // 2

            middle = points[middle_index]

            # V normally reaches a lower middle point
            if middle[1] > start[1] and middle[1] > end[1]:

                return "V"

            # ======================================
            # /
            # ======================================

            if end[0] > start[0]:

                return "/"

            return "\\"

        # ==========================================
        # L SHAPE
        # ==========================================

        if ratio < 1:

            if abs(end[0] - start[0]) < width * 0.4:

                return "L"

        # ==========================================
        # UNKNOWN
        # ==========================================

        return "?"