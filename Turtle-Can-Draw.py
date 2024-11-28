import sys
import turtle
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image
from PyQt5.QtCore import QElapsedTimer

class ImageRepaintApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Turtle can Draw :)")
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

        # Label to display the time taken
        self.time_label = QLabel("Time taken: 0 s", self)
        layout.addWidget(self.time_label)

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

                # Start the timer
                timer = QElapsedTimer()
                timer.start()

                # Transform the image into RGB and redraw with Turtle
                img = Image.open(file_path).convert("RGB")
                width, height = img.size
                pixels = img.load()

                # Start Turtle drawing
                self.turtle_drawing(width, height, pixels)

                # Calculate elapsed time
                elapsed_time = timer.elapsed()
                self.time_label.setText(f"Time taken: {elapsed_time / 1000:.2f} s")

            except Exception as e:
                print(f"Error loading image: {e}")

    def turtle_drawing(self, width, height, pixels):
        # Create a new Turtle screen
        turtle_screen = turtle.Screen()
        turtle_screen.title("Turtle Drawing")

        # Set the world coordinates based on image size
        turtle_screen.setworldcoordinates(-width // 2, -height // 2, width // 2, height // 2)

        # Set Turtle window size based on image
        turtle_screen.setup(width + 50, height + 50)  # Adding some margin for the window

        # Create multiple turtles
        turtles = [turtle.Turtle() for _ in range(5)]  # Create 5 turtles
        for t in turtles:
            t.speed(0)  # Set to the fastest speed
            t.penup()

        # Draw with multiple turtles
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                # Choose a turtle based on the x coordinate
                t = turtles[x % len(turtles)]  # Cycle through turtles
                t.pencolor(r / 255, g / 255, b / 255)
                t.goto(x - width // 2, height // 2 - y)
                t.pendown()
                t.dot(1)

        turtle.done()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageRepaintApp()
    window.show()
    sys.exit(app.exec_())
