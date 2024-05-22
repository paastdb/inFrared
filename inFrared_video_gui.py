from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QLabel, QTextEdit
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import sys
from PyQt5 import QtGui
import cv2
from moviepy.editor import VideoFileClip


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "inFrared Video by PastLands @paastdb"
        self.top = 100
        self.left = 100
        self.width = 1200
        self.height = 600

        self.input_video_path = None  # To store the selected input video path

        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon(r"D:\Downloads\Past Lands\Infrared\gui\iF.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Add buttons
        self.select_file_button = QPushButton('Select File', self)
        self.select_file_button.clicked.connect(self.openFileNameDialog)
        self.select_file_button.move(20, 20)

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.startProcess)
        self.start_button.move(120, 20)

        # Add label to display processed frames
        self.label = QLabel(self)
        self.label.setGeometry(20, 60, 640, 480)

        # Add console widget
        self.console = QTextEdit(self)
        self.console.setGeometry(680, 60, 500, 480)
        self.console.setReadOnly(True)

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Video Files (*.mp4)", options=options)
        if fileName:
            self.input_video_path = fileName

    def startProcess(self):
        if self.input_video_path:
            apply_infrared_to_video(self, self.input_video_path)
        else:
            self.console.append("Error: Please select a video file first.")


def apply_infrared_to_video(window, input_video_path):
    def apply_infrared(frame):
        processed_frame = infared_effect(frame)
        return processed_frame

    def infared_effect(frame):
        # Apply infrared effect to the frame
        cimg = frame
        plt_image = cv2.cvtColor(cimg, cv2.COLOR_BGR2RGB)

        inv_cimg = ~cimg.copy()
        inv_cimg[:, :, 1] = 0
        inv_cimg[:, :, 2] = 0

        plt_image = cv2.cvtColor(inv_cimg, cv2.COLOR_BGR2RGB)

        inv_hsv = cv2.cvtColor(inv_cimg, cv2.COLOR_BGR2HSV)
        img_hsv = cv2.cvtColor(cimg, cv2.COLOR_BGR2HSV)

        dst = cv2.addWeighted(inv_hsv[:, :, 0], .9, img_hsv[:, :, 0], .9, 0)
        img_hsv[:, :, 0] = dst
        hue_cimg = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

        plt_image = hue_cimg

        plt_image = cv2.cvtColor(hue_cimg, cv2.COLOR_BGR2RGB)
        frame = plt_image

        return frame

    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        window.console.append("Error: Unable to open video file")
        return

    # Get input video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    codec = cv2.VideoWriter_fourcc(*'mp4v')

    # Define codec and create VideoWriter object
    out = cv2.VideoWriter('video-output.mp4', codec, fps, (width, height))

    # Process each frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Apply infrared effect to the frame
        processed_frame = apply_infrared(frame)

        # Write the processed frame to output video
        out.write(processed_frame)

        # Display the processed frame
        processed_frame = cv2.resize(processed_frame, (640, 480))
        processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = processed_frame.shape
        bytesPerLine = ch * w
        qImg = QImage(processed_frame.data, w, h, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)
        window.label.setPixmap(pixmap)
        window.label.setAlignment(Qt.AlignCenter)
        QApplication.processEvents()  # Update the GUI

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Merge processed video with original audio using moviepy
    original_clip = VideoFileClip(input_video_path)
    processed_clip = VideoFileClip('video-output.mp4')
    final_clip = processed_clip.set_audio(original_clip.audio)
    final_clip.write_videofile('video-output-audio.mp4', codec='libx264', audio_codec='aac')

    window.console.append("Video processing complete.")

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())


