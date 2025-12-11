from sketchpy import canvas
import os

# Check if file exists
img_path = r"D:\Programs\python\internship\Sketchpy_test\Doraemon.jpg"
if not os.path.exists(img_path):
    print("Image not found!")
else:
    d = canvas.sketch_from_image(img_path)
    d.draw()
