# Turtle Can Draw
Overall Workflow:
    The program opens a dialog to load an image and then displays it in the PyQt5 window.
    Once the image is loaded, it uses the Pillow library to read the image data.
    The Turtle library is then employed to recreate the image on its canvas, skipping any white pixels to avoid unnecessary drawing.

It's slow but intresting...

Very very slow.......
It takes four and a half hours to finish drawing half of an 800 by 800 resolution image...

Plan:
    Trying to increase drawing speed and keep learning.

Versions:
V1.0.4 (28.11.2024):  
    Add more restrictions to optimize drawing logic(Optimize the logic of skipping for white pixels, drawing logic and turtle screen setup)
    
V1.0.3 (28.11.2024):  
    Temporarily remove multiple tortoise synchornization drawing and add restrictions to optimize drawing logic.

V1.0.2 (28.11.2024):  
    Multiple Turtles were added for alternate drawing.

V1.0.1 (28.11.2024):  
    Basically realize the function of drawing with Turtle.
