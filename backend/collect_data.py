import cv2
import os

from hand_tracker import HandTracker


DATASET_DIR = "dataset"
SAMPLES_PER_LETTER = 20


# ==========================================
# DATASET
# ==========================================

os.makedirs(DATASET_DIR, exist_ok=True)


# ==========================================
# ASK LETTER
# ==========================================

while True:

    label = input("Enter the letter to collect (A-Z): ").strip().upper()

    if len(label) == 1 and label in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        break

    print("Please enter ONE letter only.")


# ==========================================
# FOLDER
# ==========================================

letter_folder = os.path.join(
    DATASET_DIR,
    label
)

os.makedirs(letter_folder, exist_ok=True)


# ==========================================
# EXISTING SAMPLES
# ==========================================

files = [
    f
    for f in os.listdir(letter_folder)
    if f.endswith(".txt")
]

sample_number = len(files)


# ==========================================
# CAMERA DIRECTLY
# ==========================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("ERROR: Camera could not open.")

    exit()


# ==========================================
# HAND TRACKER
# ==========================================

tracker = HandTracker()


# ==========================================
# STARTUP
# ==========================================

print()
print("------------------------------------------")
print("       AIR WRITING DATA COLLECTOR")
print("------------------------------------------")
print("Letter:", label)
print()
print("Draw with your INDEX finger.")
print()
print("SPACE = Save")
print("C     = Clear")
print("Q     = Quit")
print("ESC   = Quit")
print("------------------------------------------")


# ==========================================
# VARIABLES
# ==========================================

points = []


# ==========================================
# MAIN LOOP
# ==========================================

try:

    while sample_number < SAMPLES_PER_LETTER:

        # ----------------------------------
        # CAMERA
        # ----------------------------------

        ret, frame = cap.read()

        if not ret:

            print("Camera frame error.")

            break


        # ----------------------------------
        # HAND TRACKING
        # ----------------------------------

        results = tracker.process(frame)


        # ----------------------------------
        # DRAW LANDMARKS
        # ----------------------------------

        frame = tracker.draw_landmarks(
            frame,
            results
        )


        # ----------------------------------
        # INDEX FINGER
        # ----------------------------------

        if results.multi_hand_landmarks:

            hand = results.multi_hand_landmarks[0]

            index_tip = hand.landmark[8]


            x = int(
                index_tip.x * frame.shape[1]
            )

            y = int(
                index_tip.y * frame.shape[0]
            )


            x = max(
                0,
                min(x, frame.shape[1] - 1)
            )

            y = max(
                0,
                min(y, frame.shape[0] - 1)
            )


            points.append(
                (x, y)
            )


            cv2.circle(
                frame,
                (x, y),
                8,
                (0, 255, 0),
                -1
            )


            # Draw line

            if len(points) > 1:

                cv2.line(
                    frame,
                    points[-2],
                    points[-1],
                    (255, 0, 255),
                    4
                )


        # ----------------------------------
        # TEXT
        # ----------------------------------

        cv2.putText(
            frame,
            f"LETTER: {label}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )


        cv2.putText(
            frame,
            f"SAMPLES: {sample_number}/{SAMPLES_PER_LETTER}",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )


        cv2.putText(
            frame,
            f"POINTS: {len(points)}",
            (20, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )


        cv2.putText(
            frame,
            "SPACE=SAVE  C=CLEAR  Q/ESC=EXIT",
            (20, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )


        # ----------------------------------
        # SHOW
        # ----------------------------------

        cv2.imshow(
            "Air Writing Data Collector",
            frame
        )


        # ----------------------------------
        # KEYBOARD
        # ----------------------------------

        key = cv2.waitKey(1) & 0xFF


        # ----------------------------------
        # Q
        # ----------------------------------

        if key == ord("q"):

            print("Q pressed - exiting.")

            break


        # ----------------------------------
        # ESC
        # ----------------------------------

        elif key == 27:

            print("ESC pressed - exiting.")

            break


        # ----------------------------------
        # C
        # ----------------------------------

        elif key == ord("c"):

            points.clear()

            print("Drawing cleared.")


        # ----------------------------------
        # SPACE
        # ----------------------------------

        elif key == 32:

            if len(points) < 10:

                print("Not enough points.")

                continue


            sample_number += 1


            filename = os.path.join(
                letter_folder,
                f"{label}_{sample_number}.txt"
            )


            with open(
                filename,
                "w"
            ) as file:

                for x, y in points:

                    file.write(
                        f"{x},{y}\n"
                    )


            print(
                f"Saved sample "
                f"{sample_number}/{SAMPLES_PER_LETTER}"
            )


            points.clear()


finally:

    print()
    print("Cleaning up...")


    cap.release()


    tracker.close()


    cv2.destroyAllWindows()


    print(
        f"Samples: "
        f"{sample_number}/{SAMPLES_PER_LETTER}"
    )

    print("Collector closed.")