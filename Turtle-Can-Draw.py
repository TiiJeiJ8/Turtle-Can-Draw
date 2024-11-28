import sys
import turtle
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
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

        # Set container and layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image files (*.jpg *.jpeg *.png)")
        if file_path:
            try:
                # Display image
                pixmap = QPixmap(file_path)
                self.image_label.setPixmap(pixmap.scaled(400, 400))

                # Transform the image into RGB and redraw with Turtle
                img = Image.open(file_path).convert("RGB")
                width, height = img.size
                pixels = img.load()

                # Start Turtle drawing
                self.turtle_drawing(width, height, pixels)

            except Exception as e:
                print(f"Error loading image: {e}")

    def turtle_drawing(self, width, height, pixels):
        # Create a new Turtle screen
        turtle_screen = turtle.Screen()
        turtle_screen.title("Turtle Drawing")
        turtle_screen.setworldcoordinates(-width // 2, -height // 2, width // 2, height // 2)

        turtle.speed(0)
        turtle.clear()
        turtle.penup()

        # Draw layer by layer, not pixel by pixel
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                # Skip white pixels
                if (r, g, b) == (255, 255, 255):
                    continue

                # Move the turtle to the pixel's position (only if it’s drawing)
                turtle.goto(x - width // 2, height // 2 - y)
                turtle.dot(1)

        turtle.done()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageRepaintApp()
    window.show()
    sys.exit(app.exec_())
