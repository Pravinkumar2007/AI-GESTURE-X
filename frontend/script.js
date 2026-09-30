// ============================================================
// GESTUREX - COMPLETE SCRIPT.JS
// ============================================================
// CAMERA
// BACKGROUND VIDEO
// MOUSE CONTROL
// LEFT CLICK
// RIGHT CLICK
// VOLUME
// BRIGHTNESS
// ZOOM
// SCROLL
// AIR WRITING
// OCR
// PERSONALIZED DIALOGUE
// ACCURACY / STABILITY FILTER
// ============================================================

console.log("====================================");
console.log("GESTUREX SCRIPT LOADED");
console.log("====================================");


// ============================================================
// API
// ============================================================

const API = "http://127.0.0.1:5000";


// ============================================================
// PERSONALIZED DIALOGUE AUDIO
// ============================================================

const dialogueAudio = new Audio("./audio/dialogue.mp3");

dialogueAudio.preload = "auto";
dialogueAudio.volume = 1.0;
dialogueAudio.muted = false;

let dialogueReady = false;
let lastDialogueTime = 0;

const DIALOGUE_COOLDOWN = 3000;


// ============================================================
// DIALOGUE STABILITY
// ============================================================

// Dialogue must be detected for several consecutive frames.
// This prevents accidental dialogue activation.

let dialogueCandidateFrames = 0;
let dialogueLostFrames = 0;

const DIALOGUE_REQUIRED_FRAMES = 4;
const DIALOGUE_RELEASE_FRAMES = 3;


// ============================================================
// GENERAL GESTURE STABILITY
// ============================================================

let currentStableGesture = "WAITING";
let candidateGesture = "";
let candidateGestureFrames = 0;

const GENERAL_STABLE_FRAMES = 2;


// ============================================================
// AUDIO UNLOCK
// ============================================================

function unlockDialogueAudio() {

    if (dialogueReady) {
        return;
    }

    try {

        dialogueAudio.muted = true;

        const promise = dialogueAudio.play();

        if (promise !== undefined) {

            promise
                .then(() => {

                    dialogueAudio.pause();
                    dialogueAudio.currentTime = 0;
                    dialogueAudio.muted = false;

                    dialogueReady = true;

                    console.log(
                        "✅ DIALOGUE AUDIO UNLOCKED"
                    );

                })
                .catch(error => {

                    console.log(
                        "Audio unlock waiting:",
                        error
                    );

                    dialogueAudio.muted = false;
                });
        }

    } catch (error) {

        console.error(
            "Audio unlock error:",
            error
        );
    }
}


// ============================================================
// PLAY PERSONALIZED DIALOGUE
// ============================================================

function playPersonalizedDialogue() {

    const now = Date.now();

    if (
        now - lastDialogueTime <
        DIALOGUE_COOLDOWN
    ) {

        console.log(
            "Dialogue cooldown active"
        );

        return;
    }

    lastDialogueTime = now;

    console.log(
        "🔊 PLAYING PERSONALIZED DIALOGUE"
    );

    try {

        dialogueAudio.pause();

        dialogueAudio.currentTime = 0;

        dialogueAudio.muted = false;

        dialogueAudio.volume = 1.0;

        const promise = dialogueAudio.play();

        if (promise !== undefined) {

            promise
                .then(() => {

                    console.log(
                        "✅ PERSONALIZED DIALOGUE PLAYING"
                    );

                })
                .catch(error => {

                    console.error(
                        "❌ DIALOGUE PLAY ERROR:",
                        error
                    );

                    // Attempt unlock again.
                    unlockDialogueAudio();
                });
        }

    } catch (error) {

        console.error(
            "Dialogue playback error:",
            error
        );
    }
}


// ============================================================
// ELEMENTS
// ============================================================

const introScreen =
    document.getElementById("introScreen");

const mainApp =
    document.getElementById("mainApp");

const startButton =
    document.getElementById("startButton");

const stopButton =
    document.getElementById("stopButton");

const backgroundVideo =
    document.getElementById("backgroundVideo");

const cameraFeed =
    document.getElementById("cameraFeed");

const cameraContainer =
    document.getElementById("cameraContainer");

const cameraPlaceholder =
    document.getElementById("cameraPlaceholder");

const cameraDot =
    document.getElementById("cameraDot");

const cameraStatus =
    document.getElementById("cameraStatus");

const systemStatus =
    document.getElementById("systemStatus");

const stateDot =
    document.getElementById("stateDot");

const cameraInfoStatus =
    document.getElementById("cameraInfoStatus");

const aiInfoStatus =
    document.getElementById("aiInfoStatus");

const airWritingInfoStatus =
    document.getElementById("airWritingInfoStatus");

const gestureIcon =
    document.getElementById("gestureIcon");

const gestureName =
    document.getElementById("gestureName");

const gestureDescription =
    document.getElementById("gestureDescription");

const detectionProgress =
    document.getElementById("detectionProgress");

const airWritingToggle =
    document.getElementById("airWritingToggle");

const airWritingToggleText =
    document.getElementById("airWritingToggleText");

const airWritingModuleState =
    document.getElementById("airWritingModuleState");

const recognizedText =
    document.getElementById("recognizedText");

const airWritingOverlayStatus =
    document.getElementById(
        "airWritingOverlayStatus"
    );


// ============================================================
// CANVAS
// ============================================================

const airWritingCanvas =
    document.getElementById(
        "airWritingOverlay"
    );

const airCtx =
    airWritingCanvas
        ? airWritingCanvas.getContext("2d")
        : null;


// ============================================================
// STATE
// ============================================================

let stream = null;

let running = false;

let processing = false;

let frameTimer = null;

let drawingActive = false;

let drawingStarted = false;

let lastDrawPoint = null;


// ============================================================
// DIALOGUE STATE
// ============================================================

let dialogueGestureActive = false;


// ============================================================
// AIR WRITING SETTINGS
// ============================================================

let brushColor = "#67e8f9";

let brushThickness = 5;

let eraserActive = false;


// ============================================================
// RESIZE CANVAS
// ============================================================

function resizeAirWritingCanvas() {

    if (
        !airWritingCanvas ||
        !cameraContainer ||
        !airCtx
    ) {
        return;
    }

    const rect =
        cameraContainer.getBoundingClientRect();

    if (
        rect.width <= 0 ||
        rect.height <= 0
    ) {
        return;
    }

    const width =
        Math.floor(rect.width);

    const height =
        Math.floor(rect.height);

    if (
        airWritingCanvas.width === width &&
        airWritingCanvas.height === height
    ) {
        return;
    }

    let oldCanvas = null;

    if (
        airWritingCanvas.width > 0 &&
        airWritingCanvas.height > 0
    ) {

        oldCanvas =
            document.createElement("canvas");

        oldCanvas.width =
            airWritingCanvas.width;

        oldCanvas.height =
            airWritingCanvas.height;

        const oldCtx =
            oldCanvas.getContext("2d");

        oldCtx.drawImage(
            airWritingCanvas,
            0,
            0
        );
    }

    airWritingCanvas.width =
        width;

    airWritingCanvas.height =
        height;

    if (oldCanvas) {

        airCtx.drawImage(
            oldCanvas,
            0,
            0,
            oldCanvas.width,
            oldCanvas.height,
            0,
            0,
            width,
            height
        );
    }

    applyBrushStyle();
}


// ============================================================
// BRUSH STYLE
// ============================================================

function applyBrushStyle() {

    if (!airCtx) {
        return;
    }

    airCtx.lineWidth =
        brushThickness;

    airCtx.lineCap =
        "round";

    airCtx.lineJoin =
        "round";

    if (eraserActive) {

        airCtx.globalCompositeOperation =
            "destination-out";

        airCtx.shadowBlur = 0;

    } else {

        airCtx.globalCompositeOperation =
            "source-over";

        airCtx.strokeStyle =
            brushColor;

        airCtx.shadowColor =
            brushColor;

        airCtx.shadowBlur = 8;
    }
}


// ============================================================
// CLEAR CANVAS
// ============================================================

function clearAirWritingCanvas() {

    if (
        !airWritingCanvas ||
        !airCtx
    ) {
        return;
    }

    airCtx.save();

    airCtx.globalCompositeOperation =
        "source-over";

    airCtx.clearRect(
        0,
        0,
        airWritingCanvas.width,
        airWritingCanvas.height
    );

    airCtx.restore();

    drawingStarted = false;

    lastDrawPoint = null;
}


// ============================================================
// SAVE DRAWING
// ============================================================

function saveAirWriting() {

    if (!airWritingCanvas) {

        alert(
            "Air Writing canvas not available."
        );

        return;
    }

    const saveCanvas =
        document.createElement("canvas");

    saveCanvas.width =
        airWritingCanvas.width;

    saveCanvas.height =
        airWritingCanvas.height;

    const saveCtx =
        saveCanvas.getContext("2d");

    saveCtx.fillStyle =
        "#ffffff";

    saveCtx.fillRect(
        0,
        0,
        saveCanvas.width,
        saveCanvas.height
    );

    saveCtx.drawImage(
        airWritingCanvas,
        0,
        0
    );

    const link =
        document.createElement("a");

    link.download =
        "GestureX-Air-Writing-" +
        new Date()
            .toISOString()
            .replace(/[:.]/g, "-") +
        ".png";

    link.href =
        saveCanvas.toDataURL(
            "image/png"
        );

    link.click();

    if (recognizedText) {

        recognizedText.textContent =
            "Drawing saved successfully";
    }
}


// ============================================================
// COLOR
// ============================================================

function setBrushColor(color) {

    if (!color) {
        return;
    }

    brushColor = color;

    eraserActive = false;

    applyBrushStyle();

    updateAirWritingUI();
}


// ============================================================
// THICKNESS
// ============================================================

function setBrushThickness(value) {

    const thickness =
        Number(value);

    if (
        !Number.isFinite(thickness) ||
        thickness <= 0
    ) {
        return;
    }

    brushThickness =
        thickness;

    applyBrushStyle();

    updateAirWritingUI();
}


// ============================================================
// ERASER
// ============================================================

function toggleEraser() {

    eraserActive =
        !eraserActive;

    applyBrushStyle();

    updateAirWritingUI();

    if (recognizedText) {

        recognizedText.textContent =
            eraserActive
                ? "Eraser ON"
                : "Pencil ON";
    }
}


// ============================================================
// AIR WRITING UI
// ============================================================

function updateAirWritingUI() {

    const eraserButton =
        document.getElementById(
            "airEraserButton"
        );

    const colorInput =
        document.getElementById(
            "airColorPicker"
        );

    const thicknessInput =
        document.getElementById(
            "airThickness"
        );

    const thicknessValue =
        document.getElementById(
            "airThicknessValue"
        );

    if (eraserButton) {

        if (eraserActive) {

            eraserButton.classList.add(
                "active"
            );

            eraserButton.textContent =
                "🧽 ERASER ON";

        } else {

            eraserButton.classList.remove(
                "active"
            );

            eraserButton.textContent =
                "🧽 ERASER";
        }
    }

    if (colorInput) {
        colorInput.value =
            brushColor;
    }

    if (thicknessInput) {
        thicknessInput.value =
            brushThickness;
    }

    if (thicknessValue) {

        thicknessValue.textContent =
            brushThickness + " px";
    }
}


// ============================================================
// START CAMERA
// ============================================================

async function startCamera() {

    try {

        if (
            !navigator.mediaDevices ||
            !navigator.mediaDevices.getUserMedia
        ) {

            throw new Error(
                "Browser does not support camera access."
            );
        }

        stream =
            await navigator.mediaDevices.getUserMedia({

                video: {

                    width: {
                        ideal: 640
                    },

                    height: {
                        ideal: 480
                    },

                    facingMode: "user"
                },

                audio: false
            });

        cameraFeed.srcObject =
            stream;

        cameraFeed.muted = true;

        cameraFeed.autoplay = true;

        cameraFeed.playsInline = true;

        await cameraFeed.play();

        cameraFeed.classList.add(
            "active"
        );

        if (cameraPlaceholder) {
            cameraPlaceholder.style.display =
                "none";
        }

        if (cameraDot) {
            cameraDot.classList.add(
                "active"
            );
        }

        if (cameraStatus) {
            cameraStatus.textContent =
                "CAMERA ACTIVE";
        }

        if (cameraInfoStatus) {
            cameraInfoStatus.textContent =
                "ON";
        }

        if (cameraContainer) {
            cameraContainer.classList.add(
                "active"
            );
        }

        resizeAirWritingCanvas();

        console.log(
            "CAMERA STARTED"
        );

        return true;

    } catch (error) {

        console.error(
            "Camera error:",
            error
        );

        alert(
            "Camera could not start.\n\n" +
            error.name +
            "\n" +
            error.message
        );

        return false;
    }
}


// ============================================================
// STOP CAMERA
// ============================================================

function stopCamera() {

    if (stream) {

        stream
            .getTracks()
            .forEach(track => {
                track.stop();
            });

        stream = null;
    }

    if (cameraFeed) {

        cameraFeed.pause();

        cameraFeed.srcObject =
            null;

        cameraFeed.classList.remove(
            "active"
        );
    }

    if (cameraPlaceholder) {
        cameraPlaceholder.style.display =
            "flex";
    }

    if (cameraDot) {
        cameraDot.classList.remove(
            "active"
        );
    }

    if (cameraStatus) {
        cameraStatus.textContent =
            "CAMERA OFF";
    }

    if (cameraInfoStatus) {
        cameraInfoStatus.textContent =
            "OFF";
    }

    if (cameraContainer) {
        cameraContainer.classList.remove(
            "active"
        );
    }
}


// ============================================================
// BACKGROUND VIDEO
// ============================================================

function startBackgroundVideo() {

    if (!backgroundVideo) {
        return;
    }

    backgroundVideo.muted = true;

    backgroundVideo.loop = true;

    backgroundVideo.playsInline = true;

    backgroundVideo
        .play()
        .catch(error => {

            console.log(
                "Background video autoplay blocked:",
                error
            );
        });
}


// ============================================================
// START BACKEND
// ============================================================

async function startBackend() {

    try {

        const response =
            await fetch(
                `${API}/api/start`,
                {
                    method: "POST"
                }
            );

        if (!response.ok) {

            throw new Error(
                "HTTP " +
                response.status
            );
        }

        const data =
            await response.json();

        if (!data.success) {

            throw new Error(
                data.message ||
                "Backend failed"
            );
        }

        console.log(
            "BACKEND STARTED"
        );

        return true;

    } catch (error) {

        console.error(
            "Backend error:",
            error
        );

        alert(
            "Flask backend is not running.\n\n" +
            "Open CMD inside backend and run:\n\n" +
            "python main.py"
        );

        return false;
    }
}


// ============================================================
// STOP BACKEND
// ============================================================

async function stopBackend() {

    try {

        await fetch(
            `${API}/api/stop`,
            {
                method: "POST"
            }
        );

    } catch (error) {

        console.error(
            "Stop backend error:",
            error
        );
    }
}


// ============================================================
// START SYSTEM
// ============================================================

async function startSystem() {

    if (running) {
        return;
    }

    // IMPORTANT:
    // This is a real user interaction.
    // Unlock audio here.
    unlockDialogueAudio();

    if (startButton) {

        startButton.disabled =
            true;

        startButton.textContent =
            "INITIALIZING...";
    }

    startBackgroundVideo();

    const cameraOK =
        await startCamera();

    if (!cameraOK) {

        if (startButton) {

            startButton.disabled =
                false;

            startButton.textContent =
                "▶ START SYSTEM";
        }

        return;
    }

    const backendOK =
        await startBackend();

    if (!backendOK) {

        stopCamera();

        if (startButton) {

            startButton.disabled =
                false;

            startButton.textContent =
                "▶ START SYSTEM";
        }

        return;
    }

    running = true;

    if (systemStatus) {
        systemStatus.textContent =
            "SYSTEM ACTIVE";
    }

    if (stateDot) {
        stateDot.classList.add(
            "active"
        );
    }

    if (aiInfoStatus) {
        aiInfoStatus.textContent =
            "RUNNING";
    }

    if (startButton) {
        startButton.textContent =
            "SYSTEM ACTIVE";
    }

    if (stopButton) {
        stopButton.disabled =
            false;
    }

    resetGesture();

    startProcessing();

    resizeAirWritingCanvas();

    console.log(
        "GESTUREX RUNNING"
    );
}


// ============================================================
// STOP SYSTEM
// ============================================================

async function stopSystem() {

    running = false;

    stopProcessing();

    await stopDrawing();

    stopCamera();

    await stopBackend();

    dialogueGestureActive = false;

    dialogueCandidateFrames = 0;
    dialogueLostFrames = 0;

    candidateGesture = "";
    candidateGestureFrames = 0;

    currentStableGesture =
        "WAITING";

    if (systemStatus) {
        systemStatus.textContent =
            "SYSTEM STANDBY";
    }

    if (stateDot) {
        stateDot.classList.remove(
            "active"
        );
    }

    if (aiInfoStatus) {
        aiInfoStatus.textContent =
            "STANDBY";
    }

    if (startButton) {

        startButton.disabled =
            false;

        startButton.textContent =
            "▶ START SYSTEM";
    }

    if (stopButton) {
        stopButton.disabled =
            true;
    }

    resetGesture();

    console.log(
        "GESTUREX STOPPED"
    );
}


// ============================================================
// PROCESS FRAME
// ============================================================

async function processFrame() {

    if (
        !running ||
        processing ||
        !cameraFeed
    ) {
        return;
    }

    if (
        cameraFeed.readyState < 2 ||
        cameraFeed.videoWidth === 0 ||
        cameraFeed.videoHeight === 0
    ) {
        return;
    }

    processing = true;

    try {

        const canvas =
            document.createElement(
                "canvas"
            );

        canvas.width =
            cameraFeed.videoWidth;

        canvas.height =
            cameraFeed.videoHeight;

        const context =
            canvas.getContext("2d");

        context.drawImage(
            cameraFeed,
            0,
            0,
            canvas.width,
            canvas.height
        );

        const image =
            canvas.toDataURL(
                "image/jpeg",
                0.65
            );

        const response =
            await fetch(
                `${API}/api/process_frame`,
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            image: image
                        })
                }
            );

        if (!response.ok) {

            throw new Error(
                "HTTP " +
                response.status
            );
        }

        const data =
            await response.json();

        // ====================================================
        // RAW GESTURE
        // ====================================================

        const rawGesture =
            data.gesture;

        // ====================================================
        // NORMALIZE
        // ====================================================

        const gesture =
            normalizeGesture(
                rawGesture
            );

        // ====================================================
        // STABLE GESTURE
        // ====================================================

        const stableGesture =
            stabilizeGesture(
                gesture
            );

        updateGesture(
            stableGesture,
            data.description,
            data.confidence
        );

        // ====================================================
        // DIALOGUE
        // ====================================================

        handleDialogueGesture(
            gesture
        );

        // ====================================================
        // AIR WRITING
        // ====================================================

        if (drawingActive) {

            drawFromBackend(data);
        }

    } catch (error) {

        console.error(
            "Frame processing error:",
            error
        );

    } finally {

        processing = false;
    }
}


// ============================================================
// STABILIZE GESTURE
// ============================================================

function stabilizeGesture(gesture) {

    if (!gesture) {
        return currentStableGesture;
    }

    if (
        gesture ===
        currentStableGesture
    ) {
        candidateGesture = "";
        candidateGestureFrames = 0;

        return currentStableGesture;
    }

    if (
        gesture !==
        candidateGesture
    ) {

        candidateGesture =
            gesture;

        candidateGestureFrames =
            1;

        return currentStableGesture;
    }

    candidateGestureFrames++;

    if (
        candidateGestureFrames >=
        GENERAL_STABLE_FRAMES
    ) {

        currentStableGesture =
            gesture;

        candidateGesture = "";

        candidateGestureFrames = 0;
    }

    return currentStableGesture;
}


// ============================================================
// DIALOGUE GESTURE HANDLER
// ============================================================

function handleDialogueGesture(gesture) {

    if (!gesture) {

        dialogueLostFrames++;

        if (
            dialogueLostFrames >=
            DIALOGUE_RELEASE_FRAMES
        ) {

            dialogueCandidateFrames = 0;

            dialogueGestureActive =
                false;
        }

        return;
    }

    const g =
        String(gesture)
            .trim()
            .toUpperCase();

    // ========================================================
    // IMPORTANT
    // Dialogue names.
    // ========================================================

    const isDialogueGesture =
        isDialogueGestureName(g);

    if (isDialogueGesture) {

        dialogueLostFrames = 0;

        dialogueCandidateFrames++;

        console.log(
            "DIALOGUE CANDIDATE:",
            dialogueCandidateFrames
        );

        // ----------------------------------------------------
        // Do not allow any other frontend action here.
        // ----------------------------------------------------

        if (
            dialogueCandidateFrames >=
            DIALOGUE_REQUIRED_FRAMES
        ) {

            if (
                !dialogueGestureActive
            ) {

                dialogueGestureActive =
                    true;

                console.log(
                    "===================================="
                );

                console.log(
                    "🤙 THUMB + PINKY CONFIRMED"
                );

                console.log(
                    "🔊 PERSONALIZED DIALOGUE"
                );

                console.log(
                    "===================================="
                );

                playPersonalizedDialogue();
            }
        }

        return;
    }

    // ========================================================
    // NON-DIALOGUE
    // ========================================================

    dialogueLostFrames++;

    if (
        dialogueLostFrames >=
        DIALOGUE_RELEASE_FRAMES
    ) {

        dialogueCandidateFrames = 0;

        dialogueGestureActive =
            false;
    }
}


// ============================================================
// DIALOGUE NAME DETECTOR
// ============================================================

function isDialogueGestureName(g) {

    if (!g) {
        return false;
    }

    // Exact names
    const exactNames = [

        "DIALOGUE",

        "PERSONALIZED DIALOGUE",

        "PLAY DIALOGUE",

        "DIALOGUE GESTURE",

        "THUMB PINKY",

        "THUMB + PINKY",

        "THUMB AND PINKY",

        "THUMB_PINKY",

        "THUMB-PINKY",

        "THUMB PINKIE",

        "THUMB + LITTLE",

        "THUMB LITTLE",

        "THUMB AND LITTLE",

        "PINKY THUMB",

        "PINKY + THUMB"

    ];

    if (
        exactNames.includes(g)
    ) {

        return true;
    }

    // More tolerant backend naming
    const compact =
        g.replace(
            /[\s_\-+]/g,
            ""
        );

    if (
        compact === "THUMBPINKY" ||
        compact === "PINKYTHUMB" ||
        compact === "THUMBLITTLE" ||
        compact === "LITTLETHUMB"
    ) {

        return true;
    }

    if (
        compact.includes("DIALOGUE")
    ) {

        return true;
    }

    return false;
}


// ============================================================
// NORMALIZE GESTURE
// ============================================================

function normalizeGesture(value) {

    if (!value) {
        return "WAITING";
    }

    const gesture =
        String(value)
            .trim()
            .toUpperCase();

    const compact =
        gesture.replace(
            /[\s_\-+]/g,
            ""
        );

    // ========================================================
    // DIALOGUE MUST BE CHECKED FIRST
    // ========================================================

    if (
        isDialogueGestureName(
            gesture
        )
    ) {

        return "DIALOGUE";
    }

    if (
        compact === "THUMBPINKY" ||
        compact === "PINKYTHUMB" ||
        compact === "THUMBLITTLE" ||
        compact === "LITTLETHUMB"
    ) {

        return "DIALOGUE";
    }

    // ========================================================
    // MOUSE
    // ========================================================

    const aliases = {

        "INDEX":
            "MOVE",

        "INDEX FINGER":
            "MOVE",

        "MOUSE":
            "MOVE",

        "MOUSE MOVE":
            "MOVE",

        // ====================================================
        // VOLUME
        // ====================================================

        "THUMB UP":
            "VOLUME UP",

        "THUMBS UP":
            "VOLUME UP",

        "VOLUME INCREASE":
            "VOLUME UP",

        "THUMB DOWN":
            "VOLUME DOWN",

        "THUMBS DOWN":
            "VOLUME DOWN",

        "VOLUME DECREASE":
            "VOLUME DOWN",

        // ====================================================
        // BRIGHTNESS
        // ====================================================

        "INDEX MIDDLE RING":
            "BRIGHTNESS UP",

        "INDEX + MIDDLE + RING":
            "BRIGHTNESS UP",

        "BRIGHTNESS INCREASE":
            "BRIGHTNESS UP",

        "INDEX MIDDLE":
            "BRIGHTNESS DOWN",

        "INDEX + MIDDLE":
            "BRIGHTNESS DOWN",

        "BRIGHTNESS DECREASE":
            "BRIGHTNESS DOWN",

        // ====================================================
        // ZOOM
        // ====================================================

        "OPEN PALM INDEX DOWN":
            "ZOOM IN",

        "INDEX DOWN":
            "ZOOM IN",

        "ZOOM IN":
            "ZOOM IN",

        "ZOOM OUT":
            "ZOOM OUT",

        // ====================================================
        // SCROLL
        // ====================================================

        "OPEN PALM INDEX MIDDLE DOWN":
            "SCROLL",

        "INDEX MIDDLE DOWN":
            "SCROLL",

        "SCROLL":
            "SCROLL",

        // ====================================================
        // RIGHT CLICK
        // ====================================================

        "RIGHT CLICK":
            "RIGHT CLICK",

        "RIGHT_CLICK":
            "RIGHT CLICK",

        // ====================================================
        // LEFT CLICK
        // ====================================================

        "LEFT CLICK":
            "LEFT CLICK",

        "LEFT_CLICK":
            "LEFT CLICK",

        // ====================================================
        // AIR WRITING
        // ====================================================

        "AIR WRITING":
            "AIR WRITING",

        "AIR_WRITING":
            "AIR WRITING",

        "WRITING":
            "AIR WRITING"
    };

    return (
        aliases[gesture] ||
        gesture
    );
}


// ============================================================
// PROCESSING
// ============================================================

function startProcessing() {

    stopProcessing();

    frameTimer =
        setInterval(
            processFrame,
            100
        );
}


function stopProcessing() {

    if (frameTimer) {

        clearInterval(
            frameTimer
        );

        frameTimer = null;
    }
}


// ============================================================
// GESTURE ICONS
// ============================================================

const gestureIcons = {

    "VOLUME UP":
        "👍",

    "VOLUME DOWN":
        "👎",

    "BRIGHTNESS UP":
        "🤟",

    "BRIGHTNESS DOWN":
        "✌️",

    "MOVE":
        "☝️",

    "LEFT CLICK":
        "👆",

    "RIGHT CLICK":
        "✊",

    "ZOOM IN":
        "🖐️",

    "ZOOM OUT":
        "🤘",

    "SCROLL":
        "🖐️",

    "AIR WRITING":
        "✍️",

    "DIALOGUE":
        "🤙",

    "NO HAND":
        "◌",

    "UNKNOWN":
        "◌",

    "WAITING":
        "◌",

    "SYSTEM OFF":
        "◌",

    "ERROR":
        "⚠️"
};


// ============================================================
// GESTURE DESCRIPTIONS
// ============================================================

const gestureDescriptions = {

    "MOVE":
        "Index finger controls mouse movement",

    "LEFT CLICK":
        "Left click gesture detected",

    "RIGHT CLICK":
        "Right click gesture detected",

    "VOLUME UP":
        "Thumb Up — Increasing system volume",

    "VOLUME DOWN":
        "Thumb Down — Decreasing system volume",

    "BRIGHTNESS UP":
        "Index + Middle + Ring — Increasing brightness",

    "BRIGHTNESS DOWN":
        "Index + Middle — Decreasing brightness",

    "ZOOM IN":
        "Zoom In gesture detected",

    "ZOOM OUT":
        "Zoom Out gesture detected",

    "SCROLL":
        "Scrolling gesture detected",

    "AIR WRITING":
        "Move your index finger to write in the air",

    "DIALOGUE":
        "🤙 Thumb + Pinky — Personalized dialogue",

    "NO HAND":
        "No hand detected",

    "WAITING":
        "Show your hand to the camera"
};


// ============================================================
// UPDATE GESTURE
// ============================================================

function updateGesture(
    gesture,
    description,
    confidence
) {

    if (gestureName) {

        gestureName.textContent =
            gesture;
    }

    if (gestureIcon) {

        gestureIcon.textContent =
            gestureIcons[gesture] ||
            "◌";
    }

    if (gestureDescription) {

        gestureDescription.textContent =
            gestureDescriptions[gesture] ||
            description ||
            "Gesture detected";
    }

    let percent =
        Number(confidence);

    if (percent <= 1) {
        percent *= 100;
    }

    if (
        Number.isNaN(percent) ||
        percent <= 0
    ) {
        percent = 10;
    }

    percent =
        Math.max(
            5,
            Math.min(
                100,
                percent
            )
        );

    if (detectionProgress) {

        detectionProgress.style.width =
            percent + "%";
    }
}


// ============================================================
// RESET GESTURE
// ============================================================

function resetGesture() {

    currentStableGesture =
        "WAITING";

    candidateGesture =
        "";

    candidateGestureFrames =
        0;

    dialogueCandidateFrames =
        0;

    dialogueLostFrames =
        0;

    dialogueGestureActive =
        false;

    if (gestureIcon) {
        gestureIcon.textContent =
            "◌";
    }

    if (gestureName) {
        gestureName.textContent =
            "WAITING";
    }

    if (gestureDescription) {
        gestureDescription.textContent =
            "Show your hand to the camera";
    }

    if (detectionProgress) {
        detectionProgress.style.width =
            "10%";
    }
}


// ============================================================
// AIR WRITING TOGGLE
// ============================================================

function toggleAirWriting() {

    if (!running) {

        alert(
            "Start GestureX first."
        );

        return;
    }

    if (drawingActive) {

        stopDrawing();

    } else {

        startDrawing();
    }
}


// ============================================================
// START AIR WRITING
// ============================================================

async function startDrawing() {

    drawingActive = true;

    drawingStarted = false;

    lastDrawPoint = null;

    resizeAirWritingCanvas();

    if (airWritingCanvas) {

        airWritingCanvas.style.display =
            "block";
    }

    if (airWritingToggle) {

        airWritingToggle.classList.add(
            "active"
        );
    }

    if (airWritingToggleText) {

        airWritingToggleText.textContent =
            "AIR WRITING ON";
    }

    if (airWritingModuleState) {

        airWritingModuleState.textContent =
            "ACTIVE";
    }

    if (airWritingInfoStatus) {

        airWritingInfoStatus.textContent =
            "ACTIVE";
    }

    if (airWritingOverlayStatus) {

        airWritingOverlayStatus.textContent =
            "AIR WRITING ON";
    }

    if (recognizedText) {

        recognizedText.textContent =
            "Writing... Move your index finger";
    }

    clearAirWritingCanvas();

    try {

        await fetch(
            `${API}/api/drawing/start`,
            {
                method: "POST"
            }
        );

    } catch (error) {

        console.error(
            "Drawing start error:",
            error
        );
    }

    applyBrushStyle();

    updateAirWritingUI();
}


// ============================================================
// STOP AIR WRITING
// ============================================================

async function stopDrawing() {

    drawingActive = false;

    drawingStarted = false;

    lastDrawPoint = null;

    if (airWritingToggle) {

        airWritingToggle.classList.remove(
            "active"
        );
    }

    if (airWritingToggleText) {

        airWritingToggleText.textContent =
            "AIR WRITING OFF";
    }

    if (airWritingModuleState) {

        airWritingModuleState.textContent =
            "OFF";
    }

    if (airWritingInfoStatus) {

        airWritingInfoStatus.textContent =
            "OFF";
    }

    if (airWritingOverlayStatus) {

        airWritingOverlayStatus.textContent =
            "AIR WRITING OFF";
    }

    if (recognizedText) {

        recognizedText.textContent =
            "Pencil mode is OFF";
    }

    try {

        await fetch(
            `${API}/api/drawing/stop`,
            {
                method: "POST"
            }
        );

    } catch (error) {

        console.error(
            "Drawing stop error:",
            error
        );
    }
}


// ============================================================
// GET INDEX POINT
// ============================================================

function getIndexPoint(data) {

    if (
        data &&
        data.index_finger &&
        typeof data.index_finger === "object"
    ) {

        const x =
            Number(
                data.index_finger.x
            );

        const y =
            Number(
                data.index_finger.y
            );

        if (
            Number.isFinite(x) &&
            Number.isFinite(y)
        ) {

            return {
                x: x,
                y: y
            };
        }
    }

    return null;
}


// ============================================================
// DRAW FROM BACKEND
// ============================================================

function drawFromBackend(data) {

    if (
        !drawingActive ||
        !airWritingCanvas ||
        !airCtx
    ) {
        return;
    }

    const point =
        getIndexPoint(data);

    if (!point) {

        drawingStarted = false;

        lastDrawPoint = null;

        return;
    }

    let x =
        point.x;

    let y =
        point.y;

    if (
        x >= 0 &&
        x <= 1 &&
        y >= 0 &&
        y <= 1
    ) {

        x =
            (1 - x) *
            airWritingCanvas.width;

        y =
            y *
            airWritingCanvas.height;
    }

    drawPoint(
        x,
        y
    );
}


// ============================================================
// DRAW POINT
// ============================================================

function drawPoint(x, y) {

    if (
        !airWritingCanvas ||
        !airCtx
    ) {
        return;
    }

    x =
        Math.max(
            0,
            Math.min(
                airWritingCanvas.width,
                x
            )
        );

    y =
        Math.max(
            0,
            Math.min(
                airWritingCanvas.height,
                y
            )
        );

    if (!drawingStarted) {

        lastDrawPoint = {
            x: x,
            y: y
        };

        drawingStarted = true;

        return;
    }

    if (!lastDrawPoint) {

        lastDrawPoint = {
            x: x,
            y: y
        };

        return;
    }

    const dx =
        x -
        lastDrawPoint.x;

    const dy =
        y -
        lastDrawPoint.y;

    const distance =
        Math.sqrt(
            dx * dx +
            dy * dy
        );

    if (distance > 150) {

        lastDrawPoint = {
            x: x,
            y: y
        };

        return;
    }

    applyBrushStyle();

    airCtx.beginPath();

    airCtx.moveTo(
        lastDrawPoint.x,
        lastDrawPoint.y
    );

    airCtx.lineTo(
        x,
        y
    );

    airCtx.stroke();

    lastDrawPoint = {
        x: x,
        y: y
    };
}


// ============================================================
// CLEAR BUTTON
// ============================================================

function clearDrawing() {

    clearAirWritingCanvas();

    if (recognizedText) {

        recognizedText.textContent =
            "Canvas cleared";
    }
}


// ============================================================
// RECOGNIZE AIR WRITING
// ============================================================

async function recognizeAirWriting() {

    if (!airWritingCanvas) {
        return;
    }

    if (!drawingStarted) {

        if (recognizedText) {

            recognizedText.textContent =
                "Draw something first.";
        }

        return;
    }

    if (recognizedText) {

        recognizedText.textContent =
            "✨ Recognizing...";
    }

    try {

        const image =
            airWritingCanvas.toDataURL(
                "image/png"
            );

        const response =
            await fetch(
                `${API}/api/recognize-writing`,
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            image: image
                        })
                }
            );

        const data =
            await response.json();

        if (
            !response.ok ||
            !data.success
        ) {

            throw new Error(
                data.message ||
                "Recognition failed"
            );
        }

        const text =
            String(
                data.text || ""
            ).trim();

        if (text) {

            if (recognizedText) {

                recognizedText.textContent =
                    text;
            }

        } else {

            if (recognizedText) {

                recognizedText.textContent =
                    "No text detected. Try writing larger.";
            }
        }

    } catch (error) {

        console.error(
            "Recognition error:",
            error
        );

        if (recognizedText) {

            recognizedText.textContent =
                "Recognition failed";
        }
    }
}


// ============================================================
// CONTROL EVENTS
// ============================================================

function setupControls() {

    if (startButton) {

        startButton.addEventListener(
            "click",
            startSystem
        );
    }

    if (stopButton) {

        stopButton.addEventListener(
            "click",
            stopSystem
        );

        stopButton.disabled =
            true;
    }

    if (airWritingToggle) {

        airWritingToggle.addEventListener(
            "click",
            toggleAirWriting
        );
    }

    const eraserButton =
        document.getElementById(
            "airEraserButton"
        );

    const clearButton =
        document.getElementById(
            "airClearButton"
        );

    const saveButton =
        document.getElementById(
            "airSaveButton"
        );

    const colorInput =
        document.getElementById(
            "airColorPicker"
        );

    const thicknessInput =
        document.getElementById(
            "airThickness"
        );

    if (eraserButton) {

        eraserButton.addEventListener(
            "click",
            toggleEraser
        );
    }

    if (clearButton) {

        clearButton.addEventListener(
            "click",
            clearDrawing
        );
    }

    if (saveButton) {

        saveButton.addEventListener(
            "click",
            saveAirWriting
        );
    }

    if (colorInput) {

        colorInput.addEventListener(
            "input",
            event => {

                setBrushColor(
                    event.target.value
                );
            }
        );
    }

    if (thicknessInput) {

        thicknessInput.addEventListener(
            "input",
            event => {

                setBrushThickness(
                    event.target.value
                );
            }
        );
    }

    updateAirWritingUI();
}


// ============================================================
// KEYBOARD SHORTCUTS
// ============================================================

document.addEventListener(
    "keydown",
    event => {

        if (
            event.key === "Escape" &&
            running
        ) {

            stopSystem();
        }

        if (
            event.key.toLowerCase() === "e" &&
            drawingActive
        ) {

            toggleEraser();
        }

        if (
            event.key.toLowerCase() === "c" &&
            drawingActive
        ) {

            clearDrawing();
        }

        if (
            event.key.toLowerCase() === "s" &&
            drawingActive
        ) {

            saveAirWriting();
        }

        if (
            event.key.toLowerCase() === "r" &&
            drawingActive
        ) {

            recognizeAirWriting();
        }
    }
);


// ============================================================
// WINDOW RESIZE
// ============================================================

window.addEventListener(
    "resize",
    resizeAirWritingCanvas
);


// ============================================================
// INITIALIZATION
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        console.log(
            "GESTUREX PAGE READY"
        );

        // ----------------------------------------------------
        // AUDIO PRELOAD
        // ----------------------------------------------------

        dialogueAudio.load();

        dialogueAudio.addEventListener(
            "canplaythrough",
            () => {

                dialogueReady = true;

                console.log(
                    "✅ dialogue.mp3 READY"
                );
            }
        );

        dialogueAudio.addEventListener(
            "error",
            event => {

                console.error(
                    "❌ dialogue.mp3 NOT FOUND"
                );

                console.error(
                    "Expected file:"
                );

                console.error(
                    "audio/dialogue.mp3"
                );
            }
        );

        // ----------------------------------------------------
        // BACKGROUND
        // ----------------------------------------------------

        startBackgroundVideo();

        // ----------------------------------------------------
        // BUTTONS
        // ----------------------------------------------------

        if (startButton) {

            startButton.disabled =
                false;

            startButton.textContent =
                "▶ START SYSTEM";
        }

        if (stopButton) {

            stopButton.disabled =
                true;
        }

        // ----------------------------------------------------
        // STATUS
        // ----------------------------------------------------

        if (systemStatus) {

            systemStatus.textContent =
                "SYSTEM STANDBY";
        }

        if (aiInfoStatus) {

            aiInfoStatus.textContent =
                "STANDBY";
        }

        if (cameraInfoStatus) {

            cameraInfoStatus.textContent =
                "OFF";
        }

        if (airWritingInfoStatus) {

            airWritingInfoStatus.textContent =
                "OFF";
        }

        if (airWritingToggleText) {

            airWritingToggleText.textContent =
                "AIR WRITING OFF";
        }

        if (airWritingOverlayStatus) {

            airWritingOverlayStatus.textContent =
                "AIR WRITING OFF";
        }

        // ----------------------------------------------------
        // CANVAS
        // ----------------------------------------------------

        resizeAirWritingCanvas();

        setTimeout(
            resizeAirWritingCanvas,
            500
        );

        // ----------------------------------------------------
        // CONTROLS
        // ----------------------------------------------------

        setupControls();

        // ----------------------------------------------------
        // INTRO
        // ----------------------------------------------------

        if (introScreen) {

            introScreen.classList.remove(
                "hide"
            );
        }

        if (mainApp) {

            setTimeout(
                () => {

                    if (introScreen) {

                        introScreen.classList.add(
                            "hide"
                        );
                    }

                    mainApp.classList.add(
                        "show"
                    );

                    resizeAirWritingCanvas();

                },
                2500
            );
        }
    }
);