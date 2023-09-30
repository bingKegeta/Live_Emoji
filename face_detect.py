import cv2
import dlib

# Initialize the video capture.
cap = cv2.VideoCapture(0)

# Load the Dlib face detector and facial landmark predictor.
face_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Loop over the video frames.
while True:

    # Capture the next frame.
    ret, frame = cap.read()

    # If the frame is not empty, process it.
    if ret:

        # Convert the frame to grayscale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect the face in the frame.
        faces = face_detector(gray)

        # If a face is detected, track the facial features.
        if len(faces) > 0:

            # Get the facial landmarks for the face.
            landmarks = landmark_predictor(gray, faces[0])

            # Draw the facial landmarks on the frame.
            for landmark in landmarks.parts():

                # Get the x and y coordinates of the landmark.
                x = landmark.x
                y = landmark.y

                # Draw a circle at the landmark.
                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

    # Show the frame.
    cv2.imshow("Frame", frame)

    # Press the 'q' key to quit.
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture.
cap.release()

# Destroy all windows.
cv2.destroyAllWindows()
