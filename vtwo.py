import numpy as np
from pynput.keyboard import Key, Controller, Listener
from pynput.mouse import Button, Controller
import pyperclip
import math
from PIL import Image
import itertools
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw()
filename = askopenfilename(title="Open Image", filetypes=[("Image Files",".png .jpg")])

bind = Controller()

#SETUP
actiondelay = 0.1
textboxpos = (0, 0)
donebuttonpos = (0, 0)
#END OF SETUP

holdingctrl = False
canstart = False

outputlist = []
outstring = ""

def on_press(key):
    try:
        if key.char == "k":
            if holdingctrl:
                textboxpos = bind.position
                print("Set textbox position!")
        elif key.char == "l":
            if holdingctrl:
                donebuttonpos = bind.position
                print("Set done button position!")
        elif key.char == "p":
            if canstart:
                canstart = False
                for indx, lst in enumerate(outputlist):
                    pyperclip.copy(lst)
                    bind.click(Button.left)
                    time.sleep(actiondelay)
                    bind.position = textboxpos
                    bind.click(Button.left, 1)
                    time.sleep(actiondelay)
                    pyperclip.paste()
                    bind.position = donebuttonpos
                    bind.click()
                    time.sleep(actiondelay)
                    bind.press(key.tab)
                    bind.release(key.tab)
                    time.sleep(actiondelay)
                    bind.click(Button.right)
                    time.sleep(actiondelay)
    except:
        if key == key.ctrl:
            holdingctrl = True
                
            

def on_release(key):
    if key == key.ctrl:
        holdingctrl = False
        
# Collect events until released
listener = Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

im = Image.open(filename)
newsize = (500, 500)
print(im.size)
im = im.resize(newsize)

im = np.asarray(im)
print(im.shape[0])
print(im.shape[1])
print(im.shape[2])

new_shape = (im.shape[0],im.shape[1],1,3)
image = im.reshape(new_shape)  

totalcolors ={
    (224, 83, 80)  :"$",
    (210, 30, 45)  :"???",
    (127, 24, 42)  :"??",
    (133, 52, 57)  :"???",
    (235, 128, 80) :"=",
    (238, 95, 47)  :"???",
    (194, 61, 42)  :"???",
    (135, 71, 57)  :">",

    (240, 208, 100):"<",
    (239, 192, 46) :"???",
    (184, 102, 38) :"???",
    (139, 99, 63)  :"(",
    (147, 174, 81) :")",
    (116, 160, 44) :"[",
    (50, 81, 42)   :"]",
    (75, 86, 55)   :"+",

    (116, 184, 115):"-",
    (0, 103, 50)   :"??",
    (0, 64, 42)    :"*",
    (55, 79, 63)   :"??",
    (116, 210, 187):"??",
    (1, 154, 128)  :"/",
    (1, 83, 76)    :"???",
    (59, 90, 83)   :".",

    (114, 194, 215):"^",
    (0, 168, 213)  :"???",
    (0, 90, 111)   :"%",
    (56, 94, 102)  :"???",
    (113, 159, 221):"??",
    (8, 108, 201)  :"|",
    (0, 61, 120)   :"??",
    (55, 83, 114)  :"???",

    (171, 134, 220):"{",
    (89, 31, 201)  :"}",
    (49, 31, 113)  :"!",
    (97, 77, 113)  :"???",
    (223, 148, 220):"???",
    (130, 71, 123) :"??",
    (72, 31, 76)   :"??",
    (98, 66, 91)   :"???",

    (232, 121, 164):"??",
    (230, 52, 80)  :"??",
    (139, 24, 69)  :"??",
    (114, 61, 79)  :"??",
    (134, 69, 45)  :"??",
    (77, 45, 45)   :"??",
    (69, 36, 42)   :"??",
    (37, 24, 39)   :"??",

    (198, 133, 90) :"??",
    (151, 102, 74) :"??",
    (100, 69, 60)  :"??",
    (37, 36, 45)   :"??",
    (240, 229, 211):"??",
    (193, 183, 169):"??",
    (161, 148, 135):"??",
    (133, 121, 112):"??",

    (108, 102, 98) :"?",
    (83, 77, 79)   :"??",
    (45, 52, 60)   :"??",
    (31,32,36)     :"'",
    (24,24,24)     :"`",
    (255,255,255)  :"??" 
}

colors = list(totalcolors.keys())

print("Starting...")

colors_container = np.ones(shape=[image.shape[0],image.shape[1],len(colors),3])
for i,color in enumerate(colors):
    colors_container[:,:,i,:] = color



def closest(image,color_container):
    shape = image.shape[:2]
    total_shape = shape[0]*shape[1]

    # calculate distances
    ### shape =  (x,y,number of colors)
    distances = np.sqrt(np.sum((color_container-image)**2,axis=3))

    min_index = np.argmin(distances,axis=2).reshape(-1)
    natural_index = np.arange(total_shape)

    reshaped_container = colors_container.reshape(-1,len(colors),3)

    color_view = reshaped_container[natural_index,min_index].reshape(shape[0],shape[1],3)
    return color_view

# NOTE: Dont pass uint8 due to overflow during subtract
result_image = closest(image,colors_container)

Image.fromarray(result_image.astype(np.uint8)).save("out.png")

input("Finished coloring! Press enter to convert to string!")

i = Image.fromarray(result_image.astype(np.uint8))
pixels = i.load()
width, height = i.size

all_pixels = []
pixels_x = []
pixels_y = []
for y in range(height):
    for x in range(width):
        cpixel = pixels[x, y]
        all_pixels.append(cpixel)
        pixels_x.append(x)
        pixels_y.append(y)

lasty = 1

all_pixels = list(all_pixels)
for idx, px in enumerate(all_pixels):
    
    colorcode = totalcolors[px]

    currenty = pixels_y[idx]
    if currenty > lasty:
        outputlist.append(":")
        lasty = currenty
    else:
        outputlist.append(colorcode)


for _,j in itertools.groupby(outputlist):
    j = list(j)
    outstring = outstring + (str(len(j)) + _ + "|")

outputlist = []
while len(outstring) > 1:
    outputlist.append(outstring[:280])
    outstring = outstring[280:]

print("Press CTRL + K to set mouse position for textbox\nPress CTRL + L to set mouse position for done button\nPress CTRL + P to start (must be on rec room screen)")
input("Press enter to CANCEL")