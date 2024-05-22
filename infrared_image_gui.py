import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtGui

# Define the infared_effect function
def infared_effect(image):
    # Convert image to BGR format (if not already in BGR)
    if len(image.shape) == 2:
        cimg = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    else:
        cimg = image

    # Convert BGR image to RGB 
    plt_image = cv2.cvtColor(cimg, cv2.COLOR_BGR2RGB)

    # Create inverted image
    inv_cimg = ~cimg.copy()
    inv_cimg[:, :, 1] = 0
    inv_cimg[:, :, 2] = 0

    # Convert inverted image to RGB 
    plt_image = cv2.cvtColor(inv_cimg, cv2.COLOR_BGR2RGB)

    # Convert inverted image to HSV
    inv_hsv = cv2.cvtColor(inv_cimg, cv2.COLOR_BGR2HSV)
    img_hsv = cv2.cvtColor(cimg, cv2.COLOR_BGR2HSV)

    # Apply effect to hue channel
    dst = cv2.addWeighted(inv_hsv[:, :, 0], .9, img_hsv[:, :, 0], .9, 0)
    img_hsv[:, :, 0] = dst
    hue_cimg = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

    # Convert image back to RGB for display
    plt_image = cv2.cvtColor(hue_cimg, cv2.COLOR_BGR2RGB)

    return plt_image

class InfraredEffectApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("inFrared Image by PastLands @paastdb")
        self.setGeometry(100, 100, 600, 400)

        self.input_image_path = None
        self.output_image_path = None
        self.infrared_image = None

        self.initUI()

    def initUI(self):
        self.label = QLabel("No image selected")
        self.btn_select_image = QPushButton("Select Image")
        self.btn_apply_effect = QPushButton("Apply Infrared Effect")
        self.btn_save_image = QPushButton("Save Image")

        self.image_label = QLabel()
        self.setWindowIcon(QtGui.QIcon(r"D:\Downloads\Past Lands\Infrared\gui\iF.png"))

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_select_image)
        layout.addWidget(self.btn_apply_effect)
        layout.addWidget(self.btn_save_image)
        layout.addWidget(self.image_label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.btn_select_image.clicked.connect(self.selectImage)
        self.btn_apply_effect.clicked.connect(self.applyEffect)
        self.btn_save_image.clicked.connect(self.saveImage)

    def selectImage(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_path:
            self.input_image_path = file_path
            self.label.setText("Image selected: " + self.input_image_path)

    def applyEffect(self):
        if self.input_image_path:
            image = cv2.imread(self.input_image_path)
            # Apply infrared effect
            self.infrared_image = infared_effect(image)

            # Display the processed image
            h, w, ch = self.infrared_image.shape
            bytesPerLine = ch * w
            qImg = QImage(self.infrared_image.data, w, h, bytesPerLine, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qImg)
            self.image_label.setPixmap(pixmap)
        else:
            self.label.setText("Error: No image selected")

    def saveImage(self):
        if self.infrared_image is not None:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
            if file_path:
                # Save the image without any text or border
                cv2.imwrite(file_path, self.infrared_image)
                self.output_image_path = file_path
                self.label.setText("Image saved: " + self.output_image_path)
        else:
            self.label.setText("Error: Apply infrared effect first")

if __name__ == "__main__":
    app = QApplication([])
    mainWindow = InfraredEffectApp()
    mainWindow.show()
    app.exec_()

