import numpy as np
from datetime import datetime
from PIL import Image, ImageDraw

print("starting", datetime.now())
with open("Average Frame Values.txt", "r") as file:
    total_frames = len(file.read().split("\n"))
    
total_red = np.int64(0)
total_green = np.int64(0)
total_blue = np.int64(0)
i = np.int64(0)
with open("Average Frame Values.txt", "r") as file:
    out_image = Image.new("RGB", (total_frames, 2000), (255, 255, 255))
    draw = ImageDraw.Draw(out_image)
    
    line = file.readline()
    while line:
        pixel = line.split(":")[1]
        red, green, blue = pixel.split(",")

        red = int(red)
        green = int(green)
        blue = int(blue)
        total_red += red
        total_green += green
        total_blue += blue
        
        hex_val = "#%02x%02x%02x" % (red, green, blue)
        draw.line((i, 700, i, 1700), fill=hex_val)
        
        i += np.int64(1)
        line = file.readline()

        
tot_avg_red = total_red // i
tot_avg_green = total_green // i
tot_avg_blue = total_blue // i
avg_hex = "#%02x%02x%02x" % (tot_avg_red, tot_avg_green, tot_avg_blue)
print(i//4)
print(i//2)
draw.rectangle((i//2, 100, i, 600), fill=avg_hex)
with open("Totals.txt", "w") as file:
    file.write(f"Total pixels:{total_red+total_green+total_blue}\nTotal red pixels:{total_red}\nTotal green pixels:{total_green}\nTotal blue pixels:{total_blue}\n\nAverage Color of All Frames:{avg_hex}")

print("DONE", datetime.now())

out_image.show()
out_image.save("Image from txt file.png")
