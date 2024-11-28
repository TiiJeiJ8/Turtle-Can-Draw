import sys
import turtle
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PIL import Image

class ImageRepaintApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Turtle can Draw  :)")
        self.setGeometry(100, 100, 800, 600)

        # Vertical layout
        layout = QVBoxLayout()

        # Display label of the original image
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(400, 400)
        layout.addWidget(self.image_label)

        # Button for loading the image
        self.load_button = QPushButton("Load Image", self)
        self.load_button.clicked.connect(self.load_image)
        layout.addWidget(self.load_button)

        # Button for clearing Turtle drawing
        self.clear_button = QPushButton("Clear Drawing", self)
        self.clear_button.clicked.connect(self.clear_drawing)
        self.clear_button.setEnabled(False) # Initially disabled
        layout.addWidget(self.clear_button)

        # Status label
        self.status_label = QLabel("Status: Ready", self)
        layout.addWidget(self.status_label)

        # Author label
        self.Author_label = QLabel('''---------------------------------    Author: TiiJeiJ8    ---------------------------------''', self)
        layout.addWidget(self.Author_label)

        # Set container and layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    #todo Load images
    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image files (*.jpg *.jpeg *.png)")
        if file_path:
            try:
                self.status_label.setText("Status: Loading image...")

                # Display image
                pixmap = QPixmap(file_path)
                self.image_label.setPixmap(pixmap.scaled(400, 400))
            
                # Transform the image into RGB and redraw with Turtle
                img = Image.open(file_path).convert("RGB")
                img.thumbnail((400, 400), Image.LANCZOS)  # Resize the image appropriately
                width, height = img.size
                pixels = img.load()
            
                # Start Turtle drawing
                self.turtle_drawing(width, height, pixels)
                self.status_label.setText("Status: Drawing completed!")
            
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error loading image: {e}")
                self.status_label.setText("Status: Error loading image")

    #todo Clear the screen for the next drawing
    def clear_drawing(self):
        turtle.clear()
        turtle.penup() # Move pen up to avoid drawing while clearing
        self.status_label.setText("Status: Drawing cleared")
        self.clear_button.setEnabled(False) # Disable the clear button again

    #todo Turtle, Go!
    def turtle_drawing(self, width, height, pixels):
        # Create a new Turtle screen
        turtle_screen = turtle.Screen()
        turtle_screen.title("Turtle Drawing")
        turtle_screen.setworldcoordinates(-width // 2, -height // 2, width // 2, height // 2)

        turtle.speed(0) # Fastest speed
        turtle.clear()
        turtle.penup()

        # Draw with multiple turtles
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                # Skip white pixels
                if (r, g, b) == (255, 255, 255):
                    continue

                # Set pencil color
                turtle.pencolor(r / 255, g / 255, b / 255)
                
                # Move to position and draw a bigger dot
                turtle.goto(x - width // 2, height // 2 - y)
                turtle.dot(5) # The size of the dot

        turtle.done()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageRepaintApp()
    window.show()
    sys.exit(app.exec_())
