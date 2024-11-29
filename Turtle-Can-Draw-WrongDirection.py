import sys
import turtle
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QSlider
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image

class ImageRepaintApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Turtle can Draw  :)")
        self.setGeometry(100, 100, 800, 600)

        # Vertical layout for widgets
        layout = QVBoxLayout()
        self.placeholder_label = QLabel(self)
        self.placeholder_label.setFixedSize(800, 450)
        self.placeholder_label.setStyleSheet("background-color: lightgray;")
        layout.addWidget(self.placeholder_label)
        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        # Button to load the image
        self.load_button = QPushButton("Load Image", self)
        self.load_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_button)

        # Button to clear the turtle drawing
        self.clear_button = QPushButton("Clear Drawing", self)
        self.clear_button.clicked.connect(self.clear_drawing)
        self.clear_button.setEnabled(False) # Initially disabled
        layout.addWidget(self.clear_button)

        # Slider to adjust drawing resolution (block size)
        self.resolution_slider = QSlider(Qt.Horizontal, self)
        self.resolution_slider.setMinimum(1)
        self.resolution_slider.setMaximum(50)
        self.resolution_slider.setValue(10) # Default value
        self.resolution_slider.setTickPosition(QSlider.TicksBelow)
        self.resolution_slider.setTickInterval(1)
        layout.addWidget(QLabel("Adjust Drawing Resolution (1-50):"))
        layout.addWidget(self.resolution_slider)

        # Label to show the current value of the slider
        self.resolution_value_label = QLabel("Current Resolution: 10", self)
        layout.addWidget(self.resolution_value_label)

        # Connect the slider value change to a method
        self.resolution_slider.valueChanged.connect(self.update_resolution_label)

        # Status label to show current operation status
        self.status_label = QLabel("Status: Ready", self)
        layout.addWidget(self.status_label)

        # Author label
        self.Author_label = QLabel('''---------------------------------    Author: TiiJeiJ8    ---------------------------------''', self)
        layout.addWidget(self.Author_label)

        # Set a container widget and its layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_resolution_label(self):
        # Update the label to show the current slider value
        current_value = self.resolution_slider.value()
        self.resolution_value_label.setText(f'Current Resolution: {current_value}')

    def load_image(self):
        # Load an image file and process it
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image files (*.jpg *.jpeg *.png)")
        if file_path:
            try:
                self.status_label.setText("Status: Loading image...")
        
                # Display the loaded image
                pixmap = QPixmap(file_path)
                scaled_pixmap = pixmap.scaled(450, 450, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.placeholder_label.setPixmap(scaled_pixmap)
                self.placeholder_label.setAlignment(Qt.AlignCenter)
        
                # Open the image and convert it to RGB
                img = Image.open(file_path).convert("RGB")
                width, height = img.size
                pixels = img.load()  # Load pixel data for processing
        
                # Convert image to grayscale and apply GaussianBlur for smoothing
                gray_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)  # Use Gaussian Blur to reduce the noice
    
                # Detect edges with adjusted parameters
                edges = cv2.Canny(blurred_image, 50, 150)
    
                # Find contours to divide into blocks
                contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Start turtle drawing
                self.turtle_drawing(width, height, pixels, contours)
                self.status_label.setText("Status: Drawing completed!")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error loading image: {e}")
                self.status_label.setText("Status: Error loading image")

    def clear_drawing(self):
        # Clear the turtle screen
        turtle.clear()
        turtle.penup() # Lift the pen to avoid drawing while clearing
        self.status_label.setText("Status: Drawing cleared")
        self.clear_button.setEnabled(False) # Disable the clear button again

    def turtle_drawing(self, width, height, pixels, contours):
        # Set up the turtle screen for drawing
        turtle_screen = turtle.Screen()
        turtle_screen.title("Turtle Can Draw :)")
        turtle_screen.setworldcoordinates(-width // 2, -height // 2, width // 2, height // 2)

        turtle.speed(0) # Set fastest drawing speed
        turtle.clear()
        turtle.penup()

        # Get the block size based on slider value
        block_size = self.resolution_slider.value()

        # Adjust the origin coordinate for Turtle
        origin_x = -width // 2
        origin_y = height // 2

        for contour in contours:
            # Create a bounding box around the contour
            x, y, w, h = cv2.boundingRect(contour)
            if w > 0 and h > 0:
                # Draw small blocks within the bounding box
                for dy in range(0, h, block_size): # Use block size to step through pixels
                    for dx in range(0, w, block_size):
                        pixel_x = x + dx
                        pixel_y = y + dy
                        if pixel_x < width and pixel_y < height:
                            r, g, b = pixels[pixel_x, pixel_y]
                            # Skip white pixels (or background)
                            if (r, g, b) != (255, 255, 255):
                                # Calculate turtle position
                                turtle.goto(origin_x + pixel_x, origin_y - pixel_y)
                                turtle.fillcolor(r / 255, g / 255, b / 255)
                                turtle.begin_fill()
                                for _ in range(4): # Draw a square
                                    turtle.forward(block_size)
                                    turtle.right(90)
                                turtle.end_fill()

        turtle.done()  # Finish the drawing
        QMessageBox.critical(self, "Done", f"Images redrawed!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageRepaintApp()
    window.show()
    sys.exit(app.exec_())
