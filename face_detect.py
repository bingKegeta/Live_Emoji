import tkinter as tk
from tkinter import Canvas
import cv2
import dlib
from PIL import Image, ImageTk
import threading


class FacialRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.frame_rate = 15

        # Create a Tkinter Canvas for the video feed
        self.video_canvas = Canvas(root, width=360, height=320)
        self.video_canvas.place(x=0, y=300)

        # Placeholder for the image
        self.DUMMY_IMAGE = ImageTk.PhotoImage(Image.new('RGB', (360, 320), 'black'))
        self.video_canvas.create_image(0, 0, anchor=tk.NW, image=self.DUMMY_IMAGE)

        # Initialize the video capture.
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FPS, self.frame_rate)

        # Load the Dlib face detector and facial landmark predictor.
        self.face_detector = dlib.get_frontal_face_detector()
        self.landmark_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        self.landmark_colors = {
            "left_eye": (0, 255, 0),  # Green
            "right_eye": (0, 255, 0),  # Green
            "nose_bridge": (0, 0, 255),  # Blue
            "lips": (255, 255, 0),  # Yellow
            "jawline": (255, 0, 255),  # Magenta
            "face_border": (0, 255, 255)  # Cyan
        }

        # Start a thread for facial recognition
        self.facial_recognition_thread = threading.Thread(target=self.run_facial_recognition, daemon=True)
        self.facial_recognition_thread.start()

        # Bind the closing event to the on_closing method
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def run_facial_recognition(self):
        while True:
            ret, frame = self.cap.read()

            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                faces = self.face_detector(rgb_frame)

                for face in faces:
                    landmarks = self.landmark_predictor(rgb_frame, face)

                    landmarks_data = {
                        "frame": int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)),
                        "face_rect": (face.left(), face.top(), face.width(), face.height()),
                        "landmarks": {
                            # These were all manually done :(
                            "left_eye": [(p.x, p.y) for p in landmarks.parts()[36:42]],
                            "right_eye": [(p.x, p.y) for p in landmarks.parts()[42:48]],
                            "nose_bridge": [(p.x, p.y) for p in landmarks.parts()[27:31]],
                            "lips": [(p.x, p.y) for p in landmarks.parts()[48:60]],
                            "jawline": [(p.x, p.y) for p in landmarks.parts()[0:17]],
                            "face_border": [(p.x, p.y) for p in landmarks.parts()[17:27]],
                        }
                    }

                    # Send or process landmarks_data as needed

                    for category, points in landmarks_data["landmarks"].items():
                        color = self.landmark_colors.get(category, (255, 255, 255))
                        for x, y in points:
                            cv2.circle(frame, (x, y), 3, color, -1)

                    x, y, w, h = face.left(), face.top(), face.width(), face.height()
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                bgr_frame = cv2.resize(bgr_frame, (360, 320))
                img = Image.fromarray(bgr_frame)
                img = ImageTk.PhotoImage(img)

                # Update the Tkinter Canvas with the new frame
                self.video_canvas.create_image(0, 0, anchor=tk.NW, image=img)
                self.video_canvas.img = img

    def on_closing(self):
        self.cap.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FacialRecognitionApp(root)
    root.mainloop()
