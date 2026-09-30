import pyautogui
import time

print("SCROLL.PY LOADED")


class ScrollControl:

    def __init__(self):

        # =====================================================
        # POSITION
        # =====================================================

        self.last_x = None
        self.last_y = None

        # =====================================================
        # TIMING
        # =====================================================

        self.last_scroll_time = 0
        self.last_swipe_time = 0

        # =====================================================
        # SETTINGS
        # =====================================================

        self.scroll_threshold = 0.035
        self.swipe_threshold = 0.18

        self.scroll_amount = 3

        self.scroll_cooldown = 0.12
        self.swipe_cooldown = 0.6

        print("ScrollControl initialized")

    # =========================================================
    # MAIN SCROLL
    # Compatible with server.py
    # =========================================================

    def update(self, y):

        try:

            current_time = time.time()

            # -------------------------------------------------
            # FIRST FRAME
            # -------------------------------------------------

            if self.last_y is None:

                self.last_y = y

                return None

            # -------------------------------------------------
            # CALCULATE MOVEMENT
            # -------------------------------------------------

            movement = y - self.last_y

            self.last_y = y

            # -------------------------------------------------
            # COOLDOWN
            # -------------------------------------------------

            if (
                current_time -
                self.last_scroll_time
                < self.scroll_cooldown
            ):

                return None

            # =================================================
            # SCROLL UP
            # =================================================

            if movement < -self.scroll_threshold:

                pyautogui.scroll(
                    self.scroll_amount
                )

                self.last_scroll_time = current_time

                print("⬆️ SCROLL UP")

                return "SCROLL UP"

            # =================================================
            # SCROLL DOWN
            # =================================================

            elif movement > self.scroll_threshold:

                pyautogui.scroll(
                    -self.scroll_amount
                )

                self.last_scroll_time = current_time

                print("⬇️ SCROLL DOWN")

                return "SCROLL DOWN"

            return None

        except Exception as error:

            print(
                "SCROLL ERROR:",
                error
            )

            return None

    # =========================================================
    # SCROLL WITH X + Y
    # =========================================================

    def update_scroll(self, x, y):

        try:

            return self.update(y)

        except Exception as error:

            print(
                "UPDATE SCROLL ERROR:",
                error
            )

            return None

    # =========================================================
    # SWIPE DETECTION
    # =========================================================

    def update_swipe(self, x, y):

        try:

            current_time = time.time()

            # -------------------------------------------------
            # FIRST FRAME
            # -------------------------------------------------

            if self.last_x is None:

                self.last_x = x
                self.last_y = y

                return None

            # -------------------------------------------------
            # MOVEMENT
            # -------------------------------------------------

            movement_x = x - self.last_x
            movement_y = y - self.last_y

            self.last_x = x
            self.last_y = y

            # -------------------------------------------------
            # COOLDOWN
            # -------------------------------------------------

            if (
                current_time -
                self.last_swipe_time
                < self.swipe_cooldown
            ):

                return None

            # =================================================
            # VERTICAL SWIPE
            # =================================================

            if abs(movement_y) > self.swipe_threshold:

                self.last_swipe_time = current_time

                if movement_y < 0:

                    print("⬆️ SWIPE UP")

                    return "SWIPE UP"

                else:

                    print("⬇️ SWIPE DOWN")

                    return "SWIPE DOWN"

            # =================================================
            # HORIZONTAL SWIPE
            # =================================================

            if abs(movement_x) > self.swipe_threshold:

                self.last_swipe_time = current_time

                if movement_x > 0:

                    print("➡️ SWIPE RIGHT")

                    return "SWIPE RIGHT"

                else:

                    print("⬅️ SWIPE LEFT")

                    return "SWIPE LEFT"

            return None

        except Exception as error:

            print(
                "SWIPE ERROR:",
                error
            )

            return None

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        self.last_x = None
        self.last_y = None

        self.last_scroll_time = 0
        self.last_swipe_time = 0

        print("Scroll control reset")