# Turtle Can Draw
Overall Workflow:
    The program opens a dialog to load an image and then displays it in the PyQt5 window.
    Once the image is loaded, it uses the Pillow library to read the image data.
    The Turtle library is then employed to recreate the image on its canvas, skipping any white pixels to avoid unnecessary drawing.

It's slow but intresting...

Very very slow.......
It takes four and a half hours to finish drawing half of an 800 by 800 resolution image...

Now with new method, it becomes fast seemingly.

Versions:
V1.0.8 (29.11.2024):
    Abandon the latest drawing version that uses edge and contour detection, as it is in the wrong direction. Use the original S1mpleVersion version as the new main version for this update. Of course, if the input image is simple and has clear contours, using a version with edge detection can provide a more unique experience!

V1.0.7 (28.11.2024):
    Seperate a simple version to draw pixelation work. In the main program, image processing is carried out through edge detection and contour recognition, the slider function of adjusting the rendering resolution is added to control the rendering accuracy, and the interactive interface is optimized to improve the interactive epxperience.
    With this update, the redraw speed has now reached new level and the process of the redrawing is more ornamental!

V1.0.6 (28.11.2024):
    Optimized image loading and drawing annotations, clarified layout and functional descriptions. Updated the drawing logic, adopted block processing to improve drawing efficiency, adjusted the relevant code structure and comments to make it clearer and easier to understand.

V1.0.5 (28.11.2024):
    the UI design is optimized to improve the user experience. Algorithm logic is optimizing.

V1.0.4 (28.11.2024):  
    Add more restrictions to optimize drawing logic(Optimize the logic of skipping for white pixels, drawing logic and turtle screen setup)

V1.0.3 (28.11.2024):  
    Temporarily remove multiple tortoise synchornization drawing and add restrictions to optimize drawing logic.

V1.0.2 (28.11.2024):  
    Multiple Turtles were added for alternate drawing.

V1.0.1 (28.11.2024):  
    Basically realize the function of drawing with Turtle.
