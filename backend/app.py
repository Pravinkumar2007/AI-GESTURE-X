import pyautogui
import time

print("CONTROLS.PY LOADED")


class SystemControls:

    def __init__(self):

        # -----------------------------------------------------
        # SCREEN SIZE
        # -----------------------------------------------------

        self.screen_width, self.screen_height = (
            pyautogui.size()
        )

        # -----------------------------------------------------
        # MOUSE SMOOTHING
        # -----------------------------------------------------

        self.previous_x = 0
        self.previous_y = 0

        self.smoothing = 0.25

        print(
            "SystemControls initialized"
        )

        print(
            "Screen:",
            self.screen_width,
            "x",
            self.screen_height
        )

    # =========================================================
    # MOUSE MOVEMENT
    # =========================================================

    def move_mouse(self, x, y):

        try:

            # Convert MediaPipe coordinates
            # 0.0 - 1.0
            # into screen coordinates

            target_x = int(
                x * self.screen_width
            )

            target_y = int(
                y * self.screen_height
            )

            # -------------------------------------------------
            # Mirror X direction
            # -------------------------------------------------

            target_x = self.screen_width - target_x

            # -------------------------------------------------
            # Keep inside screen
            # -------------------------------------------------

            target_x = max(
                0,
                min(
                    self.screen_width - 1,
                    target_x
                )
            )

            target_y = max(
                0,
                min(
                    self.screen_height - 1,
                    target_y
                )
            )

            # -------------------------------------------------
            # Smooth movement
            # -------------------------------------------------

            if self.previous_x == 0:
                self.previous_x = target_x

            if self.previous_y == 0:
                self.previous_y = target_y

            smooth_x = (
                self.previous_x
                +
                (
                    target_x -
                    self.previous_x
                )
                * self.smoothing
            )

            smooth_y = (
                self.previous_y
                +
                (
                    target_y -
                    self.previous_y
                )
                * self.smoothing
            )

            self.previous_x = smooth_x
            self.previous_y = smooth_y

            pyautogui.moveTo(
                int(smooth_x),
                int(smooth_y),
                duration=0.01
            )

        except Exception as error:

            print(
                "Mouse movement error:",
                error
            )

    # =========================================================
    # LEFT CLICK
    # =========================================================

    def click(self):

        try:

            pyautogui.click()

        except Exception as error:

            print(
                "Left click error:",
                error
            )

    # =========================================================
    # DOUBLE CLICK
    # =========================================================

    def double_click(self):

        try:

            pyautogui.doubleClick(
                interval=0.1
            )

        except Exception as error:

            print(
                "Double click error:",
                error
            )

    # =========================================================
    # RIGHT CLICK
    # =========================================================

    def right_click(self):

        try:

            pyautogui.rightClick()

        except Exception as error:

            print(
                "Right click error:",
                error
            )

    # =========================================================
    # VOLUME UP
    # =========================================================

    def volume_up(self):

        try:

            pyautogui.press(
                "volumeup"
            )

        except Exception as error:

            print(
                "Volume up error:",
                error
            )

    # =========================================================
    # VOLUME DOWN
    # =========================================================

    def volume_down(self):

        try:

            pyautogui.press(
                "volumedown"
            )

        except Exception as error:

            print(
                "Volume down error:",
                error
            )

    # =========================================================
    # VOLUME MUTE
    # =========================================================

    def volume_mute(self):

        try:

            pyautogui.press(
                "volumemute"
            )

        except Exception as error:

            print(
                "Volume mute error:",
                error
            )

    # =========================================================
    # NEXT MEDIA
    # =========================================================

    def next_media(self):

        try:

            pyautogui.press(
                "nexttrack"
            )

        except Exception as error:

            print(
                "Next media error:",
                error
            )

    # =========================================================
    # PREVIOUS MEDIA
    # =========================================================

    def previous_media(self):

        try:

            pyautogui.press(
                "prevtrack"
            )

        except Exception as error:

            print(
                "Previous media error:",
                error
            )

    # =========================================================
    # PLAY / PAUSE
    # =========================================================

    def play_pause(self):

        try:

            pyautogui.press(
                "playpause"
            )

        except Exception as error:

            print(
                "Play pause error:",
                error
            )

    # =========================================================
    # RESET MOUSE
    # =========================================================

    def reset_mouse(self):

        self.previous_x = 0
        self.previous_y = 0

        print(
            "Mouse control reset"
        )