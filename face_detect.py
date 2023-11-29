import tkinter as tk
from tkinter import ttk, Canvas, Label
import cv2
import dlib
import json
import socket
import threading
from PIL import Image, ImageTk


class FacialRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1080x720")

        # Create a Tkinter Canvas for the video feed
        self.video_canvas = Canvas(root, width=720, height=720)
        self.video_canvas.place(x=360, y=0)

        # Placeholder for the image
        # Can add some goofy stuff here if needed
        self.DUMMY_IMAGE = ImageTk.PhotoImage(Image.new('RGB', (360, 720), 'black'))
        self.video_canvas.create_image(0, 0, anchor=tk.NW, image=self.DUMMY_IMAGE)

        # Create a socket for communication with the Blender script
        # self.blender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.blender_socket.connect(("localhost", 12345))  # Adjust the host and port as needed

        # Initialize the video capture.
        self.cap = cv2.VideoCapture(0)

        # Load the Dlib face detector and facial landmark predictor.
        self.face_detector = dlib.get_frontal_face_detector()
        self.landmark_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

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
                        "landmarks": [(p.x, p.y) for p in landmarks.parts()]
                    }

                    # self.blender_socket.send(json.dumps(landmarks_data).encode())

                    x, y, w, h = face.left(), face.top(), face.width(), face.height()
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    for landmark in landmarks.parts():
                        x = landmark.x
                        y = landmark.y
                        cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

                bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                bgr_frame = cv2.resize(bgr_frame, (720, 720))
                img = Image.fromarray(bgr_frame)
                img = ImageTk.PhotoImage(img)

                # Update the Tkinter Canvas with the new frame
                self.video_canvas.create_image(0, 0, anchor=tk.NW, image=img)
                self.video_canvas.img = img

    def on_closing(self):
        self.cap.release()
        # self.blender_socket.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FacialRecognitionApp(root)
    root.mainloop()
