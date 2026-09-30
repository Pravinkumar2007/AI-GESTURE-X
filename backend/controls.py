# =========================================================
# GESTUREX — SYSTEM CONTROLS
# =========================================================

import time
import pyautogui

print("CONTROLS.PY LOADED")


class SystemControls:

    def __init__(self):

        # -------------------------------------------------
        # SCREEN
        # -------------------------------------------------

        self.screen_width, self.screen_height = pyautogui.size()

        # -------------------------------------------------
        # MOUSE SMOOTHING
        # -------------------------------------------------

        self.previous_x = 0
        self.previous_y = 0

        self.smoothing = 0.25

        # -------------------------------------------------
        # ACTION COOLDOWN
        # -------------------------------------------------

        self.last_action_time = {}

        self.cooldowns = {

            "click": 0.45,

            "right_click": 0.45,

            "double_click": 0.70,

            "volume_up": 0.20,

            "volume_down": 0.20,

            "next_media": 0.50,

            "previous_media": 0.50,

            "play_pause": 0.70

        }

        print("SystemControls initialized")

        print(
            "Screen:",
            self.screen_width,
            "x",
            self.screen_height
        )

    # =========================================================
    # ACTION COOLDOWN
    # =========================================================

    def can_execute(self, action):

        current_time = time.time()

        last_time = self.last_action_time.get(
            action,
            0
        )

        cooldown = self.cooldowns.get(
            action,
            0
        )

        if current_time - last_time >= cooldown:

            self.last_action_time[action] = current_time

            return True

        return False

    # =========================================================
    # MOUSE
    # =========================================================

    def move_mouse(self, x, y):

        try:

            # ---------------------------------------------
            # Convert normalized coordinates to screen
            # ---------------------------------------------

            target_x = int(
                x * self.screen_width
            )

            target_y = int(
                y * self.screen_height
            )

            # ---------------------------------------------
            # Mirror webcam movement
            # ---------------------------------------------

            target_x = (
                self.screen_width -
                target_x
            )

            # ---------------------------------------------
            # Keep cursor inside screen
            # ---------------------------------------------

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

            # ---------------------------------------------
            # Initialize previous position
            # ---------------------------------------------

            if self.previous_x == 0:

                self.previous_x = target_x

            if self.previous_y == 0:

                self.previous_y = target_y

            # ---------------------------------------------
            # Smooth movement
            # ---------------------------------------------

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

            # ---------------------------------------------
            # Save position
            # ---------------------------------------------

            self.previous_x = smooth_x
            self.previous_y = smooth_y

            # ---------------------------------------------
            # Move mouse
            # ---------------------------------------------

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

            if not self.can_execute("click"):

                return

            pyautogui.click()

            print("LEFT CLICK")

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

            if not self.can_execute("double_click"):

                return

            pyautogui.doubleClick(
                interval=0.1
            )

            print("DOUBLE CLICK")

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

            if not self.can_execute("right_click"):

                return

            pyautogui.rightClick()

            print("RIGHT CLICK")

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

            if not self.can_execute("volume_up"):

                return

            pyautogui.press("volumeup")

            print("VOLUME UP")

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

            if not self.can_execute("volume_down"):

                return

            pyautogui.press("volumedown")

            print("VOLUME DOWN")

        except Exception as error:

            print(
                "Volume down error:",
                error
            )

    # =========================================================
    # NEXT MEDIA
    # =========================================================

    def next_media(self):

        try:

            if not self.can_execute("next_media"):

                return

            pyautogui.press("nexttrack")

            print("NEXT MEDIA")

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

            if not self.can_execute("previous_media"):

                return

            pyautogui.press("prevtrack")

            print("PREVIOUS MEDIA")

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

            if not self.can_execute("play_pause"):

                return

            pyautogui.press("playpause")

            print("PLAY / PAUSE")

        except Exception as error:

            print(
                "Play/pause error:",
                error
            )

    # =========================================================
    # SCROLL UP
    # =========================================================

    def scroll_up(self):

        try:

            pyautogui.scroll(3)

            print("SCROLL UP")

        except Exception as error:

            print(
                "Scroll up error:",
                error
            )

    # =========================================================
    # SCROLL DOWN
    # =========================================================

    def scroll_down(self):

        try:

            pyautogui.scroll(-3)

            print("SCROLL DOWN")

        except Exception as error:

            print(
                "Scroll down error:",
                error
            )

    # =========================================================
    # RESET MOUSE
    # =========================================================

    def reset_mouse(self):

        self.previous_x = 0
        self.previous_y = 0

        print("Mouse control reset")

    # =========================================================
    # RESET ALL
    # =========================================================

    def reset(self):

        self.reset_mouse()

        self.last_action_time.clear()

        print("System controls reset")