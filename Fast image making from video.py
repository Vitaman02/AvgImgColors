import cv2
import numpy as np
from PIL import Image, ImageDraw
from datetime import datetime

path = input("Please input the absolute path of the video:\n")

print("Starting...", datetime.now())
cap = cv2.VideoCapture(path)
success, image = cap.read()

totalframes = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print("Total frames to read:", totalframes//24)

fps = cap.get(cv2.CAP_PROP_FPS)
print("FPS:", fps)

loops = np.int64(0)
x = np.int64(0)
frame_counter = np.int64(0)
with open("Average Frame Values.txt", "a") as file:
    while success:
        con_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        frame = np.asarray(con_image, dtype="int64")

        red = 0
        green = 0
        blue = 0
        pixels = 0
        for i in frame:
            for j in i:
                red += j[0]
                green += j[1]
                blue += j[2]
                pixels += 1
                
        avg_red = red // pixels
        avg_green = green // pixels
        avg_blue = blue // pixels

        file.write(f"Frame{x}:{avg_red},{avg_green},{avg_blue}\n")
        if loops % 1000 == 0:
            print("Current frame:", frame_counter)
        frame_counter += int(fps)
        cap.set(1, frame_counter)
        succes, image = cap.read()
        loops += 1

print("File is done. Creating image...", datetime.now())

outimg = Image.new("RGB", (loops, 2000), (255, 255, 255))
draw = ImageDraw.Draw(outimg)

i = np.int64(0)
with open("Average Frame Values.txt", "r") as file:
    line = file.readline()
    while line:
        pixel = line.split(":")[1]
        red, green, blue = pixel.split(",")

        hex_val = "#%02x%02x%02x" % (red, green, blue)
        draw.line((i, 700, i, 1900), fill=hex_val)

        total_red += red
        total_green += green
        total_blue += blue

        line = file.readline()

tot_avg_red = total_red // i
tot_avg_green = total_green // i
tot_avg_blue = total_blue // i

avg_hex = "#%02x%02x%02x" % (tot_avg_red, tot_avg_green, tot_avg_blue)
draw.rectangle((loops//2, 100, loops, 600), fill=avg_hex)

print("The image is done.", datetime.now())

outimg.show()
outimg.save("Output.png")
