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

        # Vertical layout for widgets
        layout = QVBoxLayout()
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(400, 400)
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

    #todo Load images
    def load_image(self):
        # Load an image file and process it
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image files (*.jpg *.jpeg *.png)")
        if file_path:
            try:
                self.status_label.setText("Status: Loading image...")

                # Display the loaded image
                pixmap = QPixmap(file_path)
                self.image_label.setPixmap(pixmap.scaled(400, 400))

                # Open the image and convert it to RGB
                img = Image.open(file_path).convert("RGB")
                # img.thumbnail((400, 400), Image.LANCZOS) # Resize the image
                width, height = img.size
                pixels = img.load() # Load pixel data for processing

                # Start turtle drawing
                self.turtle_drawing(width, height, pixels)
                self.status_label.setText("Status: Drawing completed!")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error loading image: {e}")
                self.status_label.setText("Status: Error loading image")

    #todo Clear the screen for the next drawing
    def clear_drawing(self):
        # Clear the turtle screen
        turtle.clear()
        turtle.penup() # Lift the pen to avoid drawing while clearing
        self.status_label.setText("Status: Drawing cleared")
        self.clear_button.setEnabled(False)  # Disable the clear button again

    #todo Turtle, Go!
    def turtle_drawing(self, width, height, pixels):
        # Set up the turtle screen for drawing
        turtle_screen = turtle.Screen()
        turtle_screen.title("Turtle Drawing")
        turtle_screen.setworldcoordinates(-width // 2, -height // 2, width // 2, height // 2)

        turtle.speed(0) # Set fastest drawing speed
        turtle.clear()
        turtle.penup()

        block_size = 10 # Block size for area processing

        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                # Analyze the color of the current block
                color_counts = {}
                for dy in range(block_size):
                    for dx in range(block_size):
                        if x + dx < width and y + dy < height:
                            r, g, b = pixels[x + dx, y + dy]
                            color_counts[(r, g, b)] = color_counts.get((r, g, b), 0) + 1

                # Find the most common color in the block
                if color_counts:
                    main_color = max(color_counts, key=color_counts.get)
                    r, g, b = main_color
                    # Skip white blocks
                    if (r, g, b) != (255, 255, 255):
                        turtle.goto(x - width // 2 + block_size // 2, height // 2 - y - block_size // 2)
                        turtle.fillcolor(r / 255, g / 255, b / 255)
                        turtle.begin_fill()
                        for _ in range(4): # Draw a square
                            turtle.forward(block_size)
                            turtle.right(90)
                        turtle.end_fill()

        turtle.done()
        #* Finish the drawing

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageRepaintApp()
    window.show()
    sys.exit(app.exec_())
