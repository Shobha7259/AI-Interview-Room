import cv2

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# ✅ REQUIRED FUNCTION
def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return faces

# ✅ MAIN FUNCTION
def process_frame(frame, prev_alert):
    faces = detect_faces(frame)

    alert = None

    if len(faces) == 0:
        if prev_alert != "no_face":
            alert = "⚠️ No Face Detected"
        prev_alert = "no_face"

    elif len(faces) > 1:
        if prev_alert != "multi_face":
            alert = "🚨 Multiple Faces Detected"
        prev_alert = "multi_face"

    else:
        prev_alert = "normal"

    # Draw face box
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return frame, alert, prev_alert