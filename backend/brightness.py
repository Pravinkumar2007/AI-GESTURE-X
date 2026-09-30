import screen_brightness_control as sbc

print("BRIGHTNESS.PY LOADED")


class BrightnessControl:

    def __init__(self):

        self.step = 10

        print("BrightnessControl initialized")

    # =========================================================
    # GET CURRENT BRIGHTNESS
    # =========================================================

    def get_current(self):

        try:

            brightness = sbc.get_brightness(display=0)

            if isinstance(brightness, list):

                return int(brightness[0])

            return int(brightness)

        except Exception as error:

            print(
                "GET BRIGHTNESS ERROR:",
                error
            )

            return None

    # =========================================================
    # SET BRIGHTNESS
    # =========================================================

    def set_brightness(self, value):

        try:

            value = int(value)

            value = max(
                0,
                min(100, value)
            )

            sbc.set_brightness(
                value,
                display=0
            )

            print(
                "BRIGHTNESS SET:",
                value
            )

            return value

        except Exception as error:

            print(
                "SET BRIGHTNESS ERROR:",
                error
            )

            return None

    # =========================================================
    # INCREASE
    # =========================================================

    def increase(self):

        try:

            current = self.get_current()

            if current is None:
                return None

            new_value = min(
                100,
                current + self.step
            )

            result = self.set_brightness(
                new_value
            )

            if result is not None:

                print(
                    "☀️ BRIGHTNESS UP:",
                    result
                )

            return result

        except Exception as error:

            print(
                "BRIGHTNESS UP ERROR:",
                error
            )

            return None

    # =========================================================
    # DECREASE
    # =========================================================

    def decrease(self):

        try:

            current = self.get_current()

            if current is None:
                return None

            new_value = max(
                0,
                current - self.step
            )

            result = self.set_brightness(
                new_value
            )

            if result is not None:

                print(
                    "🌙 BRIGHTNESS DOWN:",
                    result
                )

            return result

        except Exception as error:

            print(
                "BRIGHTNESS DOWN ERROR:",
                error
            )

            return None

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        try:

            result = self.set_brightness(50)

            if result is not None:

                print(
                    "BRIGHTNESS RESET:",
                    result
                )

            return result

        except Exception as error:

            print(
                "BRIGHTNESS RESET ERROR:",
                error
            )

            return None