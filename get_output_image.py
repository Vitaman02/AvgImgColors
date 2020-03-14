import cv2
import os
import numpy as np
from PIL import Image, ImageDraw

path = input("Input the absolute path of your mp4 video:\n")

cwd = os.getcwd()
out_path = f"{cwd}/Output"
os.mkdir(out_path)
os.mkdir(f"{out_path}/Frames")


vidcap = cv2.VideoCapture(path)
success, image = vidcap.read()
count = 0
print("getting all the frames from the video...")
while success:
    cv2.imwrite(f"{out_path}/Frames/frame%d.jpg" % count, image)
    success, image = vidcap.read()
    count += 1

print("counting pixels...")
dirs = os.listdir(f"{out_path}/Frames/")

with open(f"{out_path}/Average Color per Frame.txt", "a") as file:
    total_red = 0
    total_green = 0
    total_blue = 0
    total_frames = 0
    total_pixels = 0
    for item in dirs:
        red = 0
        green = 0
        blue = 0
        pixels = 0

        frame = Image.open(f"{out_path}/Frames/{item}")
        frame.load()
        data = np.asarray(frame, dtype="int64")
        for i in data:
            for j in i:
                red += j[0]
                green += j[1]
                blue += j[2]
                pixels += 1
        
        file.write(f"Frame{total_frames}:{red//pixels},{green//pixels},{blue//pixels}\n")
            
        total_pixels += pixels
        total_frames += 1
        total_red += red
        total_green += green
        total_blue += blue


print("making image...")
out_img = Image.new("RGB", (total_pixels, 2000), (255, 255, 255))
draw = ImageDraw.Draw(out_img)
with open(f"{out_path}/Average Color per Frame.txt", "r") as file:
    line = file.readline()
    while line:
        pixel = line.split(":")[1]
        red, green, blue = pixel

        total_red += int(red)
        total_green += int(green)
        total_blue += int(blue)

        hex_val = "#%02x%02x%02x" % (int(red), int(green), int(blue))
        draw.line((i, 100, i, 600), fill=hex_val)

        i += 1
        line = file.readline()

print("writing total values...")
avg_red = total_red // total_pixels
avg_green = total_green // total_pixels
avg_blue = total_blue // total_pixels
avg_hex = "#%02x%02x%02x" % (avg_red, avg_green, avg_blue)

point1 = total_pixels // 2

with open(f"{out_path}/Totals.txt", "w") as file:
    file.write(f"Total pixels:{i}\n\Total Red:{total_red}\n\Total Green:{total_green}\n\Total blue:{total_blue}\n\n\Average Color: {avg_red}, {avg_green}, {avg_blue} (RGB) (HEX='{avg_hex}')")
    
out_img.show()
out_img.save(f"{out_path}/output_image.png")

    
