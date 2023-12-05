import tkinter as tk
from tkinter import Canvas
import cv2
from PIL import Image, ImageTk
import threading
import mediapipe as mp


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

        # Initialize Mediapipe FaceMesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh()

        # self.landmark_colors = {
        #     "left_eye": (0, 255, 0),  # Green
        #     "right_eye": (0, 255, 0),  # Green
        #     "nose_bridge": (0, 0, 255),  # Blue
        #     "lips": (255, 255, 0),  # Yellow
        #     "jawline": (255, 0, 255),  # Magenta
        #     "face_border": (0, 255, 255)  # Cyan
        # }

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

                # Use Mediapipe FaceMesh to get facial landmarks
                result = self.face_mesh.process(rgb_frame)
                if result.multi_face_landmarks:
                    for landmarks in result.multi_face_landmarks:
                        # Draw lines to connect all landmarks
                        self.draw_face_mesh(frame, landmarks)

                        landmarks_data = {
                            "frame": int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)),
                            "landmarks": {
                                "face": [(p.x, p.y, p.z) for p in landmarks.landmark],
                            }
                        }

                        # Send or process landmarks_data as needed

                        # Visualize landmarks on the frame
                        self.visualize_landmarks(frame, landmarks_data)

                bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                bgr_frame = cv2.resize(bgr_frame, (360, 320))
                img = Image.fromarray(bgr_frame)
                img = ImageTk.PhotoImage(img)

                # Update the Tkinter Canvas with the new frame
                self.video_canvas.create_image(0, 0, anchor=tk.NW, image=img)
                self.video_canvas.img = img

    def draw_face_mesh(self, frame, landmarks):
        for connection in mp.solutions.face_mesh.FACEMESH_CONTOURS:
            pt1_idx = connection[0]
            pt2_idx = connection[1]

            pt1 = (int(landmarks.landmark[pt1_idx].x * frame.shape[1]),
                   int(landmarks.landmark[pt1_idx].y * frame.shape[0]))
            pt2 = (int(landmarks.landmark[pt2_idx].x * frame.shape[1]),
                   int(landmarks.landmark[pt2_idx].y * frame.shape[0]))

            cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

    def visualize_landmarks(self, frame, landmarks_data):
        for point in landmarks_data["landmarks"]["face"]:
            x, y, z = point
            x = int(x * frame.shape[1])
            y = int(y * frame.shape[0])
            cv2.circle(frame, (x, y), 3, (255, 0, 0), -1)

    def on_closing(self):
        self.cap.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FacialRecognitionApp(root)
    root.mainloop()
