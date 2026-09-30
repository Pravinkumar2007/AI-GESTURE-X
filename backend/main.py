# ============================================================
# GESTUREX - COMPLETE MAIN.PY
# Stable Gesture + Audio Version
#
# GESTURES
# ------------------------------------------------------------
# INDEX ONLY                       = MOUSE MOVE
# FIST                             = LEFT CLICK
# THUMB UP                         = VOLUME UP
# THUMB DOWN                       = VOLUME DOWN
# TWO FINGERS                      = BRIGHTNESS DOWN
# THREE FINGERS                    = BRIGHTNESS UP
# OPEN PALM                        = AIR WRITING
# INDEX + MIDDLE DOWN + 2 UP       = SCROLL
# TWO-HAND CLAP                    = BGM ON / OFF
# OPEN HAND WAVE                   = HELLO AUDIO
#
# REMOVED
# ------------------------------------------------------------
# RIGHT CLICK                      = REMOVED
# ZOOM IN                          = REMOVED
# PINCH                            = NO ACTION
# ============================================================


import base64
import math
import os
import time
import threading

import cv2
import easyocr
import mediapipe as mp
import numpy as np
import pyautogui
import pygame

from flask import Flask, jsonify, request
from flask_cors import CORS

from brightness import BrightnessControl


# ============================================================
# FLASK
# ============================================================

app = Flask(__name__)
CORS(app)


# ============================================================
# OPTIONAL CHARACTER MODEL
# ============================================================

try:

    from handwriting_model import recognize_character

    CHARACTER_MODEL_AVAILABLE = True

    print("AI Character Model: READY")

except Exception as error:

    recognize_character = None

    CHARACTER_MODEL_AVAILABLE = False

    print("AI Character Model unavailable:", error)


# ============================================================
# GLOBAL STATE
# ============================================================

system_running = False
air_writing = False

current_gesture = "WAITING"
current_description = "Press START GESTUREX"
current_confidence = 0


# ============================================================
# AUDIO
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BGM_PATH = os.path.join(BASE_DIR, "bgm.mp3")
HELLO_PATH = os.path.join(BASE_DIR, "hello.mp3")
DIALOGUE_PATH = os.path.join(BASE_DIR, "dialogue.mp3")

audio_available = False

bgm_available = False
hello_available = False
dialogue_available = False

bgm_playing = False

hello_sound = None
dialogue_sound = None

audio_lock = threading.RLock()

last_hello_time = 0.0
last_dialogue_time = 0.0

HELLO_COOLDOWN = 2.5
DIALOGUE_COOLDOWN = 1.5


# ============================================================
# AUDIO INITIALIZATION
# ============================================================

def initialize_audio():

    global audio_available
    global bgm_available
    global hello_available
    global dialogue_available

    global hello_sound
    global dialogue_sound

    print("")
    print("==========================================")
    print("        GESTUREX AUDIO SYSTEM")
    print("==========================================")

    print("Base directory:", BASE_DIR)
    print("BGM:", BGM_PATH)
    print("HELLO:", HELLO_PATH)
    print("DIALOGUE:", DIALOGUE_PATH)

    print("==========================================")
    print("")

    try:

        pygame.mixer.pre_init(
            frequency=44100,
            size=-16,
            channels=2,
            buffer=512
        )

        pygame.mixer.init()

        audio_available = True

        print("AUDIO ENGINE: READY")

    except Exception as error:

        audio_available = False

        print("AUDIO ENGINE ERROR:", error)

        return

    # --------------------------------------------------------
    # BGM
    # --------------------------------------------------------

    if os.path.isfile(BGM_PATH):

        try:

            pygame.mixer.music.load(BGM_PATH)

            bgm_available = True

            print("BGM: READY")

        except Exception as error:

            print("BGM LOAD ERROR:", error)

    else:

        print("BGM NOT FOUND:", BGM_PATH)

    # --------------------------------------------------------
    # HELLO
    # --------------------------------------------------------

    if os.path.isfile(HELLO_PATH):

        try:

            hello_sound = pygame.mixer.Sound(
                HELLO_PATH
            )

            hello_available = True

            print("HELLO: READY")

        except Exception as error:

            print("HELLO LOAD ERROR:", error)

    else:

        print("HELLO NOT FOUND:", HELLO_PATH)

    # --------------------------------------------------------
    # DIALOGUE
    # --------------------------------------------------------

    if os.path.isfile(DIALOGUE_PATH):

        try:

            dialogue_sound = pygame.mixer.Sound(
                DIALOGUE_PATH
            )

            dialogue_available = True

            print("DIALOGUE: READY")

        except Exception as error:

            print("DIALOGUE LOAD ERROR:", error)

    else:

        print("DIALOGUE NOT FOUND:", DIALOGUE_PATH)

    print("")
    print("==========================================")
    print("AUDIO STATUS")
    print("==========================================")

    print(
        "Audio Engine :",
        "READY" if audio_available else "ERROR"
    )

    print(
        "BGM          :",
        "READY" if bgm_available else "NOT FOUND / ERROR"
    )

    print(
        "HELLO        :",
        "READY" if hello_available else "NOT FOUND / ERROR"
    )

    print(
        "DIALOGUE     :",
        "READY" if dialogue_available else "NOT FOUND / ERROR"
    )

    print("==========================================")
    print("")


initialize_audio()


# ============================================================
# AUDIO FUNCTIONS
# ============================================================

def toggle_bgm():

    global bgm_playing

    with audio_lock:

        if not audio_available:

            print("BGM: audio engine unavailable")

            return False

        if not bgm_available:

            print("BGM: bgm.mp3 unavailable")

            return False

        try:

            if bgm_playing:

                pygame.mixer.music.stop()

                bgm_playing = False

                print("👏 CLAP -> BGM OFF")

            else:

                pygame.mixer.music.stop()

                pygame.mixer.music.load(BGM_PATH)

                pygame.mixer.music.play(-1)

                bgm_playing = True

                print("👏 CLAP -> BGM ON")

            return True

        except Exception as error:

            bgm_playing = False

            print("BGM ERROR:", error)

            return False


# ============================================================
# HELLO AUDIO
# ============================================================

def play_hello():

    global last_hello_time

    now = time.time()

    if now - last_hello_time < HELLO_COOLDOWN:

        return False

    with audio_lock:

        if not audio_available or not hello_available:

            print("HELLO AUDIO UNAVAILABLE")

            return False

        try:

            hello_sound.stop()

            channel = hello_sound.play()

            if channel is None:

                print("HELLO PLAY FAILED")

                return False

            last_hello_time = now

            print("👋 HELLO -> hello.mp3")

            return True

        except Exception as error:

            print("HELLO AUDIO ERROR:", error)

            return False


# ============================================================
# DIALOGUE AUDIO
# ============================================================

def play_dialogue():

    global last_dialogue_time

    now = time.time()

    if now - last_dialogue_time < DIALOGUE_COOLDOWN:

        return False

    with audio_lock:

        if not audio_available or not dialogue_available:

            print("DIALOGUE AUDIO UNAVAILABLE")

            return False

        try:

            dialogue_sound.stop()

            channel = dialogue_sound.play()

            if channel is None:

                print("DIALOGUE PLAY FAILED")

                return False

            last_dialogue_time = now

            print("🔊 DIALOGUE -> dialogue.mp3")

            return True

        except Exception as error:

            print("DIALOGUE AUDIO ERROR:", error)

            return False


# ============================================================
# STOP ALL AUDIO
# ============================================================

def stop_all_audio():

    global bgm_playing

    with audio_lock:

        try:

            pygame.mixer.music.stop()

        except Exception:

            pass

        try:

            if hello_sound:

                hello_sound.stop()

        except Exception:

            pass

        try:

            if dialogue_sound:

                dialogue_sound.stop()

        except Exception:

            pass

        bgm_playing = False


# ============================================================
# OCR
# ============================================================

print("Loading handwriting recognition engine...")

try:

    ocr_reader = easyocr.Reader(
        ["en"],
        gpu=False
    )

    print("Handwriting OCR: READY")

except Exception as error:

    ocr_reader = None

    print("OCR INITIALIZATION ERROR:", error)


# ============================================================
# BRIGHTNESS
# ============================================================

try:

    brightness = BrightnessControl()

    print("Brightness controller: READY")

except Exception as error:

    brightness = None

    print("Brightness controller ERROR:", error)


# ============================================================
# SCREEN
# ============================================================

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

print(
    "Screen:",
    SCREEN_WIDTH,
    "x",
    SCREEN_HEIGHT
)


# ============================================================
# MEDIAPIPE
# ============================================================

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    model_complexity=0,
    min_detection_confidence=0.60,
    min_tracking_confidence=0.60
)


# ============================================================
# STATES
# ============================================================

lock = threading.Lock()

# LEFT CLICK
last_click_time = 0.0
fist_frames = 0
fist_clicked = False

# GENERAL ACTION
last_action_time = 0.0

# SCROLL
last_scroll_time = 0.0
SCROLL_COOLDOWN = 0.10

previous_scroll_y = None

SCROLL_DEADZONE = 0.012
SCROLL_AMOUNT = 3

# MOUSE
previous_mouse_x = None
previous_mouse_y = None

# IMPORTANT:
# Lower value = smoother
# Higher value = faster mouse
MOUSE_SMOOTHING = 0.65


# ============================================================
# CLAP DETECTOR
# ============================================================

CLAP_HISTORY_SIZE = 7

CLAP_CLOSE_DISTANCE = 1.30
CLAP_REARM_DISTANCE = 1.70

CLAP_MIN_CLOSING_SPEED = 0.008
CLAP_MIN_OPENING_SPEED = 0.004

CLAP_COOLDOWN = 1.40

clap_history = []

clap_armed = True
clap_contact_seen = False

last_clap_time = 0.0


# ============================================================
# RESET CLAP
# ============================================================

def reset_clap_detector():

    global clap_history
    global clap_armed
    global clap_contact_seen

    clap_history = []

    clap_armed = True

    clap_contact_seen = False


# ============================================================
# DETECT CLAP
# ============================================================

def detect_clap(hand_landmarks):

    global clap_history
    global clap_armed
    global clap_contact_seen
    global last_clap_time

    now = time.time()

    if (
        hand_landmarks is None
        or len(hand_landmarks) != 2
    ):

        if len(clap_history) > 3:

            clap_history = clap_history[-3:]

        return False

    d = get_two_hand_distance(
        hand_landmarks[0],
        hand_landmarks[1]
    )

    clap_history.append(d)

    if len(clap_history) > CLAP_HISTORY_SIZE:

        clap_history.pop(0)

    if len(clap_history) < 4:

        return False

    recent_min = min(
        clap_history[-4:]
    )

    newest = clap_history[-1]

    closing_speed = (
        clap_history[-4]
        - clap_history[-1]
    ) / 3.0

    opening_speed = (
        clap_history[-1]
        - clap_history[-2]
    )

    if recent_min <= CLAP_CLOSE_DISTANCE:

        clap_contact_seen = True

    # --------------------------------------------------------
    # MAIN CLAP TRIGGER
    # --------------------------------------------------------

    if (
        clap_armed
        and not clap_contact_seen
        and now - last_clap_time >= CLAP_COOLDOWN
        and recent_min <= CLAP_CLOSE_DISTANCE
        and closing_speed >= CLAP_MIN_CLOSING_SPEED
    ):

        toggle_bgm()

        last_clap_time = now

        clap_armed = False

        clap_contact_seen = True

        print(
            "CLAP CONFIRMED | distance:",
            round(recent_min, 3),
            "| closing:",
            round(closing_speed, 4)
        )

        return True

    # --------------------------------------------------------
    # ALTERNATE TRIGGER
    # --------------------------------------------------------

    if (
        clap_armed
        and now - last_clap_time >= CLAP_COOLDOWN
        and recent_min <= CLAP_CLOSE_DISTANCE
        and closing_speed >= CLAP_MIN_CLOSING_SPEED
    ):

        toggle_bgm()

        last_clap_time = now

        clap_armed = False

        clap_contact_seen = True

        print(
            "CLAP CONFIRMED | distance:",
            round(recent_min, 3)
        )

        return True

    # --------------------------------------------------------
    # REARM
    # --------------------------------------------------------

    if (
        not clap_armed
        and newest >= CLAP_REARM_DISTANCE
        and opening_speed >= CLAP_MIN_OPENING_SPEED
    ):

        clap_armed = True

        clap_contact_seen = False

        clap_history = clap_history[-2:]

        print("CLAP DETECTOR RE-ARMED")

    return False


# ============================================================
# HELLO WAVE
# ============================================================

previous_wave_x = None
wave_direction = None
wave_changes = 0
wave_started = False
wave_start_time = 0.0
last_wave_time = 0.0

HELLO_MIN_MOVEMENT = 0.025
HELLO_REQUIRED_CHANGES = 3
HELLO_MAX_TIME = 2.5
HELLO_WAVE_COOLDOWN = 2.5


# ============================================================
# BASIC FUNCTIONS
# ============================================================

def distance(p1, p2):

    return math.sqrt(
        (p1[0] - p2[0]) ** 2
        +
        (p1[1] - p2[1]) ** 2
    )


# ============================================================
# HAND CENTER
# ============================================================

def hand_center(hand):

    xs = []
    ys = []

    for landmark in hand.landmark:

        xs.append(float(landmark.x))
        ys.append(float(landmark.y))

    if not xs:

        return 0.5, 0.5

    return (
        sum(xs) / len(xs),
        sum(ys) / len(ys)
    )


# ============================================================
# PALM SIZE
# ============================================================

def get_palm_size(hand):

    try:

        wrist = hand.landmark[0]
        middle_mcp = hand.landmark[9]

        return max(
            math.sqrt(
                (wrist.x - middle_mcp.x) ** 2
                +
                (wrist.y - middle_mcp.y) ** 2
            ),
            0.01
        )

    except Exception:

        return 0.1


# ============================================================
# TWO HAND DISTANCE
# ============================================================

def get_two_hand_distance(hand1, hand2):

    x1, y1 = hand_center(hand1)

    x2, y2 = hand_center(hand2)

    raw = math.sqrt(
        (x1 - x2) ** 2
        +
        (y1 - y2) ** 2
    )

    palm = (
        get_palm_size(hand1)
        +
        get_palm_size(hand2)
    ) / 2.0

    return raw / max(palm, 0.01)


# ============================================================
# HELLO WAVE RESET
# ============================================================

def reset_hello_wave():

    global previous_wave_x
    global wave_direction
    global wave_changes
    global wave_started
    global wave_start_time

    previous_wave_x = None
    wave_direction = None
    wave_changes = 0
    wave_started = False
    wave_start_time = 0.0


# ============================================================
# HELLO WAVE DETECTION
# ============================================================

def detect_hello_wave(hand):

    global previous_wave_x
    global wave_direction
    global wave_changes
    global wave_started
    global wave_start_time
    global last_wave_time

    now = time.time()

    center_x, _ = hand_center(hand)

    if previous_wave_x is None:

        previous_wave_x = center_x

        return False

    movement = center_x - previous_wave_x

    previous_wave_x = center_x

    if abs(movement) < HELLO_MIN_MOVEMENT:

        if (
            wave_started
            and now - wave_start_time > HELLO_MAX_TIME
        ):

            reset_hello_wave()

        return False

    current_direction = (
        "RIGHT"
        if movement > 0
        else "LEFT"
    )

    if not wave_started:

        wave_started = True

        wave_start_time = now

        wave_direction = current_direction

        wave_changes = 0

        return False

    if now - wave_start_time > HELLO_MAX_TIME:

        reset_hello_wave()

        return False

    if (
        wave_direction is not None
        and current_direction != wave_direction
    ):

        wave_changes += 1

        wave_direction = current_direction

        if wave_changes >= HELLO_REQUIRED_CHANGES:

            if (
                now - last_wave_time
                >= HELLO_WAVE_COOLDOWN
            ):

                last_wave_time = now

                reset_hello_wave()

                play_hello()

                return True

            reset_hello_wave()

    return False


# ============================================================
# FINGERS
# ============================================================

def get_fingers(points):

    return (
        points[8][1] < points[6][1],
        points[12][1] < points[10][1],
        points[16][1] < points[14][1],
        points[20][1] < points[18][1]
    )


# ============================================================
# THUMB
# ============================================================

def get_thumb(points):

    tip = points[4]
    ip = points[3]
    mcp = points[2]

    if (
        tip[1] < ip[1]
        and tip[1] < mcp[1]
    ):

        return "UP"

    if (
        tip[1] > ip[1]
        and tip[1] > mcp[1]
    ):

        return "DOWN"

    return "OTHER"


# ============================================================
# PINCH
#
# RIGHT CLICK HAS BEEN REMOVED.
#
# This function is intentionally kept only as a helper if
# another part of the project imports it. It performs NO action.
# ============================================================

def is_pinch(points):

    palm = distance(
        points[0],
        points[9]
    )

    if palm < 0.01:

        return False

    return (
        distance(
            points[4],
            points[8]
        ) / palm
        < 0.55
    )


# ============================================================
# CLOSED FIST
# ============================================================

def is_closed_fist(points):

    palm = distance(
        points[0],
        points[9]
    )

    if palm < 0.01:

        return False

    checks = []

    pairs = [
        (8, 5, 6, 5),
        (12, 9, 10, 9),
        (16, 13, 14, 13),
        (20, 17, 18, 17)
    ]

    for tip, mcp, pip, pip_mcp in pairs:

        tip_ratio = (
            distance(
                points[tip],
                points[mcp]
            )
            / palm
        )

        pip_ratio = (
            distance(
                points[pip],
                points[pip_mcp]
            )
            / palm
        )

        checks.append(
            tip_ratio
            < pip_ratio * 1.30
        )

    return all(checks)


# ============================================================
# GESTURE DETECTION
#
# IMPORTANT:
# NO ZOOM
# NO RIGHT CLICK
# ============================================================

def detect_gesture(hand):

    points = [
        (
            float(l.x),
            float(l.y)
        )
        for l in hand.landmark
    ]

    (
        index_up,
        middle_up,
        ring_up,
        pinky_up
    ) = get_fingers(points)

    thumb = get_thumb(points)

    # --------------------------------------------------------
    # FIST = LEFT CLICK
    # --------------------------------------------------------

    if is_closed_fist(points):

        return (
            "LEFT CLICK",
            "Closed Fist = Left Click",
            98
        )

    # --------------------------------------------------------
    # OPEN PALM = AIR WRITING
    # --------------------------------------------------------

    if (
        index_up
        and middle_up
        and ring_up
        and pinky_up
    ):

        return (
            "AIR WRITING",
            "Open Palm = Air Writing",
            96
        )

    # --------------------------------------------------------
    # SCROLL
    #
    # Index + Middle DOWN
    # Ring + Pinky UP
    # --------------------------------------------------------

    if (
        not index_up
        and not middle_up
        and ring_up
        and pinky_up
    ):

        return (
            "SCROLL",
            "Index + Middle Down + Ring + Pinky Up = Scroll",
            95
        )

    # --------------------------------------------------------
    # THUMB UP = VOLUME UP
    # --------------------------------------------------------

    if (
        thumb == "UP"
        and not index_up
        and not middle_up
        and not ring_up
        and not pinky_up
    ):

        return (
            "VOLUME UP",
            "Thumb Up = Volume Increase",
            95
        )

    # --------------------------------------------------------
    # THUMB DOWN = VOLUME DOWN
    # --------------------------------------------------------

    if (
        thumb == "DOWN"
        and not index_up
        and not middle_up
        and not ring_up
        and not pinky_up
    ):

        return (
            "VOLUME DOWN",
            "Thumb Down = Volume Decrease",
            95
        )

    # --------------------------------------------------------
    # THREE FINGERS = BRIGHTNESS UP
    # --------------------------------------------------------

    if (
        index_up
        and middle_up
        and ring_up
        and not pinky_up
    ):

        return (
            "BRIGHTNESS UP",
            "Three Fingers = Brightness Increase",
            94
        )

    # --------------------------------------------------------
    # TWO FINGERS = BRIGHTNESS DOWN
    # --------------------------------------------------------

    if (
        index_up
        and middle_up
        and not ring_up
        and not pinky_up
    ):

        return (
            "BRIGHTNESS DOWN",
            "Two Fingers = Brightness Decrease",
            94
        )

    # --------------------------------------------------------
    # INDEX ONLY = MOUSE MOVE
    # --------------------------------------------------------

    if (
        index_up
        and not middle_up
        and not ring_up
        and not pinky_up
    ):

        return (
            "MOVE",
            "Index Finger = Mouse Control",
            93
        )

    # --------------------------------------------------------
    # PINCH IS NOT AN ACTION
    # --------------------------------------------------------
    # No RIGHT CLICK.
    # No gesture is returned for pinch.
    # --------------------------------------------------------

    return (
        "UNKNOWN",
        "Gesture not recognized",
        20
    )


# ============================================================
# MOUSE / SCROLL
# ============================================================

def reset_mouse():

    global previous_mouse_x
    global previous_mouse_y

    previous_mouse_x = None
    previous_mouse_y = None


# ============================================================
# RESET SCROLL
# ============================================================

def reset_scroll():

    global previous_scroll_y

    previous_scroll_y = None


# ============================================================
# MOUSE CONTROL
#
# IMPORTANT:
# This version makes mouse movement more responsive.
#
# INDEX ONLY -> MOVE
#
# Camera X is mirrored so the cursor follows natural
# hand movement.
# ============================================================

def mouse_control(hand):

    global previous_mouse_x
    global previous_mouse_y

    try:

        # ----------------------------------------------------
        # INDEX TIP
        # ----------------------------------------------------

        tip = hand.landmark[8]

        raw_x = float(tip.x)
        raw_y = float(tip.y)

        # ----------------------------------------------------
        # CLAMP CAMERA VALUES
        # ----------------------------------------------------

        raw_x = max(
            0.0,
            min(1.0, raw_x)
        )

        raw_y = max(
            0.0,
            min(1.0, raw_y)
        )

        # ----------------------------------------------------
        # MIRROR X
        # ----------------------------------------------------

        target_x = 1.0 - raw_x
        target_y = raw_y

        # ----------------------------------------------------
        # SCREEN COORDINATES
        # ----------------------------------------------------

        tx = target_x * (
            SCREEN_WIDTH - 1
        )

        ty = target_y * (
            SCREEN_HEIGHT - 1
        )

        # ----------------------------------------------------
        # FIRST FRAME
        # ----------------------------------------------------

        if (
            previous_mouse_x is None
            or previous_mouse_y is None
        ):

            previous_mouse_x = tx
            previous_mouse_y = ty

            pyautogui.moveTo(
                int(tx),
                int(ty),
                duration=0
            )

            return

        # ----------------------------------------------------
        # SMOOTH MOVEMENT
        # ----------------------------------------------------

        previous_mouse_x += (
            tx - previous_mouse_x
        ) * MOUSE_SMOOTHING

        previous_mouse_y += (
            ty - previous_mouse_y
        ) * MOUSE_SMOOTHING

        # ----------------------------------------------------
        # FINAL CLAMP
        # ----------------------------------------------------

        previous_mouse_x = max(
            0,
            min(
                SCREEN_WIDTH - 1,
                previous_mouse_x
            )
        )

        previous_mouse_y = max(
            0,
            min(
                SCREEN_HEIGHT - 1,
                previous_mouse_y
            )
        )

        # ----------------------------------------------------
        # MOVE CURSOR
        # ----------------------------------------------------

        pyautogui.moveTo(
            int(previous_mouse_x),
            int(previous_mouse_y),
            duration=0
        )

    except Exception as error:

        print(
            "MOUSE ERROR:",
            error
        )


# ============================================================
# ZOOM REMOVED
# ============================================================
#
# There is intentionally NO perform_zoom_in()
#
# ============================================================


# ============================================================
# SCROLL
# ============================================================

def perform_scroll(hand):

    global previous_scroll_y
    global last_scroll_time

    try:

        now = time.time()

        y = (
            float(hand.landmark[8].y)
            +
            float(hand.landmark[12].y)
        ) / 2.0

        if previous_scroll_y is None:

            previous_scroll_y = y

            return

        movement = (
            previous_scroll_y
            - y
        )

        previous_scroll_y = y

        if abs(movement) < SCROLL_DEADZONE:

            return

        if (
            now - last_scroll_time
            < SCROLL_COOLDOWN
        ):

            return

        pyautogui.scroll(
            SCROLL_AMOUNT
            if movement > 0
            else -SCROLL_AMOUNT
        )

        last_scroll_time = now

    except Exception as error:

        print(
            "SCROLL ERROR:",
            error
        )


# ============================================================
# ACTION
# ============================================================

def perform_action(
    gesture,
    hand=None
):

    global last_click_time
    global last_action_time

    global fist_frames
    global fist_clicked

    now = time.time()

    # --------------------------------------------------------
    # MOUSE MOVE
    # --------------------------------------------------------

    if gesture == "MOVE":

        fist_frames = 0
        fist_clicked = False

        reset_scroll()

        return

    # --------------------------------------------------------
    # AIR WRITING / HELLO / CLAP
    # --------------------------------------------------------

    if gesture in (
        "AIR WRITING",
        "HELLO",
        "CLAP"
    ):

        fist_frames = 0
        fist_clicked = False

        reset_mouse()
        reset_scroll()

        return

    # --------------------------------------------------------
    # SCROLL
    # --------------------------------------------------------

    if gesture == "SCROLL":

        fist_frames = 0
        fist_clicked = False

        reset_mouse()

        if hand is not None:

            perform_scroll(hand)

        return

    # --------------------------------------------------------
    # EVERYTHING ELSE
    # --------------------------------------------------------

    reset_scroll()

    # --------------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------------

    if gesture in (
        "UNKNOWN",
        "NO HAND"
    ):

        return

    # --------------------------------------------------------
    # LEFT CLICK
    # --------------------------------------------------------

    if gesture == "LEFT CLICK":

        fist_frames += 1

        if (
            fist_frames >= 5
            and not fist_clicked
        ):

            if (
                now - last_click_time
                >= 0.65
            ):

                try:

                    pyautogui.click(
                        button="left"
                    )

                    print(
                        ">>> LEFT CLICK <<<"
                    )

                    last_click_time = now

                    last_action_time = now

                    fist_clicked = True

                except Exception as error:

                    print(
                        "CLICK ERROR:",
                        error
                    )

        return

    # --------------------------------------------------------
    # RESET FIST
    # --------------------------------------------------------

    fist_frames = 0
    fist_clicked = False

    # --------------------------------------------------------
    # ACTION DELAY
    # --------------------------------------------------------

    if (
        now - last_action_time
        < 0.65
    ):

        return

    # --------------------------------------------------------
    # ACTIONS
    # --------------------------------------------------------

    try:

        if gesture == "VOLUME UP":

            pyautogui.press(
                "volumeup"
            )

            print(
                "VOLUME UP"
            )

        elif gesture == "VOLUME DOWN":

            pyautogui.press(
                "volumedown"
            )

            print(
                "VOLUME DOWN"
            )

        elif gesture == "BRIGHTNESS UP":

            if brightness:

                brightness.increase()

            print(
                "BRIGHTNESS UP"
            )

        elif gesture == "BRIGHTNESS DOWN":

            if brightness:

                brightness.decrease()

            print(
                "BRIGHTNESS DOWN"
            )

        else:

            return

        last_action_time = now

    except Exception as error:

        print(
            "ACTION ERROR:",
            error
        )


# ============================================================
# SET GESTURE
# ============================================================

def set_gesture(
    name,
    description,
    confidence=0
):

    global current_gesture
    global current_description
    global current_confidence

    with lock:

        current_gesture = name

        current_description = description

        current_confidence = confidence


# ============================================================
# PROCESS IMAGE
# ============================================================

def process_image(image):

    global fist_frames
    global fist_clicked

    try:

        if "," in image:

            image = image.split(
                ",",
                1
            )[1]

        image_bytes = base64.b64decode(
            image
        )

        frame = cv2.imdecode(
            np.frombuffer(
                image_bytes,
                dtype=np.uint8
            ),
            cv2.IMREAD_COLOR
        )

    except Exception as error:

        print(
            "IMAGE ERROR:",
            error
        )

        return (
            "ERROR",
            "Invalid camera image",
            0,
            None
        )

    if frame is None:

        return (
            "ERROR",
            "Could not decode camera image",
            0,
            None
        )

    # --------------------------------------------------------
    # RGB
    # --------------------------------------------------------

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # --------------------------------------------------------
    # MEDIAPIPE
    # --------------------------------------------------------

    results = hands.process(
        rgb
    )

    # ========================================================
    # NO HAND
    # ========================================================

    if not results.multi_hand_landmarks:

        fist_frames = 0
        fist_clicked = False

        reset_mouse()
        reset_scroll()
        reset_hello_wave()

        if len(clap_history) > 3:

            pass

        set_gesture(
            "NO HAND",
            "Show your hand to the camera",
            10
        )

        return (
            "NO HAND",
            "Show your hand to the camera",
            10,
            None
        )

    # ========================================================
    # CLAP FIRST
    # ========================================================

    clap_detected = detect_clap(
        results.multi_hand_landmarks
    )

    if clap_detected:

        reset_mouse()
        reset_scroll()
        reset_hello_wave()

        set_gesture(
            "CLAP",
            "Two-hand clap = BGM ON / OFF",
            99
        )

        hand = results.multi_hand_landmarks[0]

        return (
            "CLAP",
            "Two-hand clap = BGM ON / OFF",
            99,
            {
                "x": float(
                    hand.landmark[8].x
                ),
                "y": float(
                    hand.landmark[8].y
                )
            }
        )

    # ========================================================
    # SINGLE MAIN HAND
    # ========================================================

    hand = results.multi_hand_landmarks[0]

    points = [
        (
            float(l.x),
            float(l.y)
        )
        for l in hand.landmark
    ]

    (
        index_up,
        middle_up,
        ring_up,
        pinky_up
    ) = get_fingers(points)

    open_palm = (
        index_up
        and middle_up
        and ring_up
        and pinky_up
    )

    hello_detected = False

    if (
        open_palm
        and len(results.multi_hand_landmarks) == 1
    ):

        hello_detected = detect_hello_wave(
            hand
        )

    else:

        reset_hello_wave()

    # ========================================================
    # HELLO
    # ========================================================

    if hello_detected:

        reset_mouse()
        reset_scroll()

        set_gesture(
            "HELLO",
            "Hand Wave = Hello",
            99
        )

        return (
            "HELLO",
            "Hand Wave = Hello",
            99,
            {
                "x": float(
                    hand.landmark[8].x
                ),
                "y": float(
                    hand.landmark[8].y
                )
            }
        )

    # ========================================================
    # NORMAL GESTURE
    # ========================================================

    gesture, description, confidence = detect_gesture(
        hand
    )

    # --------------------------------------------------------
    # MOUSE
    # --------------------------------------------------------

    if gesture == "MOVE":

        mouse_control(hand)

    else:

        reset_mouse()

    # --------------------------------------------------------
    # ACTION
    # --------------------------------------------------------

    perform_action(
        gesture,
        hand
    )

    # --------------------------------------------------------
    # INDEX POINT
    # --------------------------------------------------------

    index_point = {
        "x": float(
            hand.landmark[8].x
        ),
        "y": float(
            hand.landmark[8].y
        )
    }

    set_gesture(
        gesture,
        description,
        confidence
    )

    return (
        gesture,
        description,
        confidence,
        index_point
    )


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return jsonify({

        "success": True,

        "message":
            "GestureX Backend Online",

        "status":
            "online",

        "audio_available":
            audio_available,

        "bgm_available":
            bgm_available,

        "bgm_playing":
            bgm_playing,

        "hello_available":
            hello_available,

        "dialogue_available":
            dialogue_available,

        "character_model_available":
            CHARACTER_MODEL_AVAILABLE
    })


# ============================================================
# STATUS
# ============================================================

@app.route(
    "/api/status",
    methods=["GET"]
)
def status():

    with lock:

        return jsonify({

            "success": True,

            "system_running":
                system_running,

            "camera_running":
                system_running,

            "gesture":
                current_gesture,

            "description":
                current_description,

            "confidence":
                current_confidence,

            "air_writing":
                air_writing,

            "audio_available":
                audio_available,

            "bgm_available":
                bgm_available,

            "bgm_playing":
                bgm_playing,

            "hello_available":
                hello_available,

            "dialogue_available":
                dialogue_available,

            "character_model_available":
                CHARACTER_MODEL_AVAILABLE
        })


# ============================================================
# AUDIO STATUS
# ============================================================

@app.route(
    "/api/audio/status",
    methods=["GET"]
)
def audio_status():

    return jsonify({

        "success": True,

        "audio_available":
            audio_available,

        "bgm_available":
            bgm_available,

        "bgm_playing":
            bgm_playing,

        "hello_available":
            hello_available,

        "dialogue_available":
            dialogue_available
    })


# ============================================================
# PLAY DIALOGUE
# ============================================================

@app.route(
    "/api/play-dialogue",
    methods=["POST", "GET"]
)
def api_play_dialogue():

    success = play_dialogue()

    return jsonify({

        "success":
            success,

        "dialogue_available":
            dialogue_available,

        "message":
            (
                "Dialogue playing"
                if success
                else
                "Dialogue unavailable"
            )
    })


# ============================================================
# AUDIO TEST
# ============================================================

@app.route(
    "/api/audio/test",
    methods=["POST", "GET"]
)
def audio_test():

    hello_ok = play_hello()

    dialogue_ok = play_dialogue()

    return jsonify({

        "success": True,

        "hello_played":
            hello_ok,

        "dialogue_played":
            dialogue_ok,

        "bgm_available":
            bgm_available,

        "hello_available":
            hello_available,

        "dialogue_available":
            dialogue_available
    })


# ============================================================
# START
# ============================================================

@app.route(
    "/api/start",
    methods=["POST", "GET"]
)
def start_system():

    global system_running

    global last_click_time
    global last_action_time

    global last_clap_time
    global last_wave_time
    global last_hello_time
    global last_dialogue_time

    global fist_frames
    global fist_clicked

    system_running = True

    last_click_time = 0
    last_action_time = 0

    last_clap_time = 0
    last_wave_time = 0

    last_hello_time = 0
    last_dialogue_time = 0

    fist_frames = 0
    fist_clicked = False

    reset_mouse()
    reset_scroll()
    reset_clap_detector()
    reset_hello_wave()

    set_gesture(
        "WAITING",
        "Show your hand to the camera",
        0
    )

    print("")
    print("------------------------------------------")
    print("GESTUREX SYSTEM STARTED")
    print("------------------------------------------")
    print("")

    return jsonify({

        "success": True,

        "message":
            "AI Gesture System started",

        "system_running":
            True
    })


# ============================================================
# STOP
# ============================================================

@app.route(
    "/api/stop",
    methods=["POST", "GET"]
)
def stop_system():

    global system_running
    global air_writing

    system_running = False

    air_writing = False

    reset_mouse()
    reset_scroll()
    reset_clap_detector()
    reset_hello_wave()

    stop_all_audio()

    set_gesture(
        "SYSTEM OFF",
        "Press START GESTUREX",
        0
    )

    print("")
    print("------------------------------------------")
    print("GESTUREX SYSTEM STOPPED")
    print("------------------------------------------")
    print("")

    return jsonify({

        "success": True,

        "message":
            "AI Gesture System stopped",

        "system_running":
            False
    })


# ============================================================
# PROCESS FRAME
# ============================================================

@app.route(
    "/api/process_frame",
    methods=["POST"]
)
def process_frame():

    if not system_running:

        return jsonify({

            "success": False,

            "gesture":
                "SYSTEM OFF",

            "description":
                "Press START GESTUREX",

            "confidence": 0,

            "index_finger": None,

            "audio_available":
                audio_available,

            "bgm_available":
                bgm_available,

            "bgm_playing":
                bgm_playing,

            "hello_available":
                hello_available,

            "dialogue_available":
                dialogue_available
        })

    data = request.get_json(
        silent=True
    )

    if not data:

        return jsonify({

            "success": False,

            "gesture": "ERROR",

            "description":
                "No image data received",

            "confidence": 0

        }), 400

    image = data.get("image")

    if not image:

        return jsonify({

            "success": False,

            "gesture": "ERROR",

            "description":
                "Image field is missing",

            "confidence": 0

        }), 400

    try:

        (
            gesture,
            description,
            confidence,
            index_point
        ) = process_image(image)

        return jsonify({

            "success": True,

            "gesture":
                gesture,

            "description":
                description,

            "confidence":
                confidence,

            "air_writing":
                air_writing,

            "audio_available":
                audio_available,

            "bgm_available":
                bgm_available,

            "bgm_playing":
                bgm_playing,

            "hello_available":
                hello_available,

            "dialogue_available":
                dialogue_available,

            "index_finger":
                index_point
        })

    except Exception as error:

        print(
            "PROCESS ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "gesture":
                "ERROR",

            "description":
                str(error),

            "confidence": 0,

            "index_finger": None

        }), 500


# ============================================================
# AIR WRITING START
# ============================================================

@app.route(
    "/api/drawing/start",
    methods=["POST", "GET"]
)
def start_drawing():

    global air_writing

    air_writing = True

    return jsonify({

        "success": True,

        "air_writing": True
    })


# ============================================================
# AIR WRITING STOP
# ============================================================

@app.route(
    "/api/drawing/stop",
    methods=["POST", "GET"]
)
def stop_drawing():

    global air_writing

    air_writing = False

    return jsonify({

        "success": True,

        "air_writing": False
    })


# ============================================================
# OCR
# ============================================================

@app.route(
    "/api/recognize-writing",
    methods=["POST"]
)
def recognize_writing():

    if ocr_reader is None:

        return jsonify({

            "success": False,

            "text": "",

            "message":
                "OCR engine unavailable"

        }), 500

    try:

        data = request.get_json(
            silent=True
        )

        if not data:

            return jsonify({

                "success": False,

                "text": "",

                "message":
                    "No drawing data received"

            }), 400

        image = data.get("image")

        if not image:

            return jsonify({

                "success": False,

                "text": "",

                "message":
                    "Drawing image missing"

            }), 400

        if "," in image:

            image = image.split(
                ",",
                1
            )[1]

        frame = cv2.imdecode(
            np.frombuffer(
                base64.b64decode(image),
                dtype=np.uint8
            ),
            cv2.IMREAD_UNCHANGED
        )

        if frame is None:

            return jsonify({

                "success": False,

                "text": "",

                "message":
                    "Invalid drawing image"

            }), 400

        if len(frame.shape) == 3:

            if frame.shape[2] == 4:

                gray = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGRA2GRAY
                )

            else:

                gray = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2GRAY
                )

        else:

            gray = frame

        _, binary = cv2.threshold(
            gray,
            40,
            255,
            cv2.THRESH_BINARY
        )

        contours, _ = cv2.findContours(
            binary,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:

            return jsonify({

                "success": True,

                "text": "",

                "message":
                    "No handwriting detected"

            })

        x_min = binary.shape[1]
        y_min = binary.shape[0]

        x_max = 0
        y_max = 0

        valid = 0

        for contour in contours:

            area = cv2.contourArea(
                contour
            )

            if area < 2:

                continue

            x, y, w, h = cv2.boundingRect(
                contour
            )

            x_min = min(
                x_min,
                x
            )

            y_min = min(
                y_min,
                y
            )

            x_max = max(
                x_max,
                x + w
            )

            y_max = max(
                y_max,
                y + h
            )

            valid += 1

        if valid == 0:

            return jsonify({

                "success": True,

                "text": "",

                "message":
                    "No handwriting detected"

            })

        padding = 30

        x_min = max(
            0,
            x_min - padding
        )

        y_min = max(
            0,
            y_min - padding
        )

        x_max = min(
            binary.shape[1],
            x_max + padding
        )

        y_max = min(
            binary.shape[0],
            y_max + padding
        )

        cropped = binary[
            y_min:y_max,
            x_min:x_max
        ]

        cropped = cv2.resize(
            cropped,
            None,
            fx=3,
            fy=3,
            interpolation=cv2.INTER_CUBIC
        )

        kernel = np.ones(
            (2, 2),
            np.uint8
        )

        cropped = cv2.morphologyEx(
            cropped,
            cv2.MORPH_CLOSE,
            kernel
        )

        processed = (
            np.ones_like(cropped)
            * 255
        )

        processed[
            cropped > 0
        ] = 0

        results = ocr_reader.readtext(
            processed,
            detail=1,
            paragraph=False,
            width_ths=0.7,
            height_ths=0.5,
            text_threshold=0.3,
            low_text=0.2
        )

        detected = []

        for result in results:

            if len(result) < 3:

                continue

            text = str(
                result[1]
            ).strip()

            confidence = float(
                result[2]
            )

            if (
                text
                and confidence >= 0.15
            ):

                detected.append(text)

        final_text = " ".join(
            detected
        ).strip()

        print(
            "OCR:",
            final_text
        )

        return jsonify({

            "success": True,

            "text":
                final_text,

            "message":
                "Handwriting processed successfully"
        })

    except Exception as error:

        print(
            "OCR ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "text": "",

            "message":
                str(error)

        }), 500


# ============================================================
# CHARACTER RECOGNITION
# ============================================================

@app.route(
    "/api/recognize-character",
    methods=["POST"]
)
def recognize_character_api():

    if not CHARACTER_MODEL_AVAILABLE:

        return jsonify({

            "success": False,

            "character": "",

            "confidence": 0,

            "message":
                "Character model unavailable"

        }), 503

    try:

        data = request.get_json(
            silent=True
        )

        if not data:

            return jsonify({

                "success": False,

                "character": "",

                "confidence": 0,

                "message":
                    "No image data"

            }), 400

        image = data.get("image")

        if not image:

            return jsonify({

                "success": False,

                "character": "",

                "confidence": 0,

                "message":
                    "Character image missing"

            }), 400

        if "," in image:

            image = image.split(
                ",",
                1
            )[1]

        frame = cv2.imdecode(
            np.frombuffer(
                base64.b64decode(image),
                dtype=np.uint8
            ),
            cv2.IMREAD_UNCHANGED
        )

        if frame is None:

            return jsonify({

                "success": False,

                "character": "",

                "confidence": 0,

                "message":
                    "Invalid image"

            }), 400

        result = recognize_character(
            frame
        )

        return jsonify({

            "success":
                result.get(
                    "success",
                    False
                ),

            "character":
                result.get(
                    "character",
                    ""
                ),

            "confidence":
                result.get(
                    "confidence",
                    0
                ),

            "message":
                result.get(
                    "message",
                    ""
                )
        })

    except Exception as error:

        print(
            "CHARACTER ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "character": "",

            "confidence": 0,

            "message":
                str(error)

        }), 500


# ============================================================
# SHUTDOWN
# ============================================================

@app.route(
    "/api/shutdown",
    methods=["POST", "GET"]
)
def shutdown():

    global system_running
    global air_writing

    system_running = False

    air_writing = False

    reset_mouse()
    reset_scroll()
    reset_clap_detector()
    reset_hello_wave()

    stop_all_audio()

    return jsonify({

        "success": True,

        "message":
            "Backend stopped"
    })


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    print("")
    print("==========================================")
    print("          GESTUREX BACKEND")
    print("==========================================")

    print(
        "Backend : http://127.0.0.1:5000"
    )

    print(
        "Frontend: http://127.0.0.1:5501"
    )

    print("")

    print("GESTURES")
    print("------------------------------------------")

    print(
        "INDEX ONLY                  = MOVE"
    )

    print(
        "FIST                        = LEFT CLICK"
    )

    print(
        "THUMB UP                    = VOLUME UP"
    )

    print(
        "THUMB DOWN                  = VOLUME DOWN"
    )

    print(
        "TWO FINGERS                 = BRIGHTNESS DOWN"
    )

    print(
        "THREE FINGERS               = BRIGHTNESS UP"
    )

    print(
        "OPEN PALM                   = AIR WRITING"
    )

    print(
        "INDEX + MIDDLE DOWN + 2 UP  = SCROLL"
    )

    print(
        "TWO-HAND CLAP               = BGM ON/OFF"
    )

    print(
        "OPEN HAND WAVE              = HELLO"
    )

    print("")
    print("REMOVED")
    print("------------------------------------------")

    print(
        "RIGHT CLICK                 = REMOVED"
    )

    print(
        "ZOOM IN                     = REMOVED"
    )

    print(
        "PINCH                       = NO ACTION"
    )

    print("")

    print("AUDIO")
    print("------------------------------------------")

    print(
        "BGM      :",
        "READY"
        if bgm_available
        else
        "NOT FOUND"
    )

    print(
        "HELLO    :",
        "READY"
        if hello_available
        else
        "NOT FOUND"
    )

    print(
        "DIALOGUE :",
        "READY"
        if dialogue_available
        else
        "NOT FOUND"
    )

    print("==========================================")
    print("")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        threaded=True,
        use_reloader=False
    )