import cv2


class AirWriter:

    def __init__(self):
        self.drawing = False
        self.points = []

        self.last_x = None
        self.last_y = None

    # ==========================================
    # START
    # ==========================================

    def start(self, x, y):

        self.drawing = True

        self.last_x = x
        self.last_y = y

        self.points.append((x, y))

    # ==========================================
    # UPDATE
    # ==========================================

    def update(self, x, y):

        if not self.drawing:
            return

        if self.last_x is not None:

            self.points.append((x, y))

        self.last_x = x
        self.last_y = y

    # ==========================================
    # STOP
    # ==========================================

    def stop(self):

        self.drawing = False

        self.last_x = None
        self.last_y = None

    # ==========================================
    # DRAW
    # ==========================================

    def draw(self, frame):

        if len(self.points) < 2:
            return frame

        for i in range(1, len(self.points)):

            cv2.line(
                frame,
                self.points[i - 1],
                self.points[i],
                (255, 0, 255),
                4
            )

        return frame

    # ==========================================
    # CLEAR
    # ==========================================

    def clear(self):

        self.points.clear()
        self.last_x = None
        self.last_y = None