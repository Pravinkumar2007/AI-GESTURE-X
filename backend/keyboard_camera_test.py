import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("CAMERA NOT OPEN")
    exit()

print("--------------------------------")
print("CAMERA KEYBOARD TEST")
print("--------------------------------")
print("Click the camera window.")
print("ress Q to quit.")
print("Press ESC to quit.")
print("--------------------------------")

while True:

    ret, frame = cap.read()

    if not ret:
        print("FRAME ERROR")
        break

    cv2.putText(
        frame,
        "PRESS Q TO EXIT",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "Keyboard Camera Test",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key != 255:
        print("KEY:", key)

    if key == ord("q"):
        print("Q WORKING!")
        break

    if key == 27:
        print("ESC WORKING!")
        break


cap.release()
cv2.destroyAllWindows()

print("TEST CLOSED")