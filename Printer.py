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
filename = askopenfilename(title="Open Image", filetypes=[("Image Files",".png .jpg .jpeg")])

bind = Controller()

#SETUP
actiondelay = 0.1
textboxpos = (0, 0)
donebuttonpos = (0, 0)
debugmode = True #Debug mode doesn't have the automatic printing
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
im = im.convert("RGB")
im.save(filename)

im = np.asarray(im)

print("Processing image... (This might take a while)")

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

try:
    # for all colors (256*256*256) assign color from palette
    precalculated = np.load('view.npz')['color_cube']
except:
    print("view.npz not found. Building a new one...")
    precalculated = np.zeros(shape=[256,256,256,3])
    for i in range(256):
        print('processing',100*i/256)
        for j in range(256):
            for k in range(256):
                index = np.argmin(np.sqrt(np.sum(((colors)-np.array([i,j,k]))**2,axis=1)))
                precalculated[i,j,k] = colors[index]
    np.savez_compressed('view', color_cube = precalculated)
        

# Processing part
#### Step 1: Take precalculated color cube for defined palette and 

def get_view(color_cube,image):
    shape = image.shape[0:2]
    indices = image.reshape(-1,3)
    # pass image colors and retrieve corresponding palette color
    new_image = color_cube[indices[:,0],indices[:,1],indices[:,2]]
   
    return new_image.reshape(shape[0],shape[1],3).astype(np.uint8)


start = time.time()
result = get_view(precalculated,im)
print('Image processed! Generating strings...')
product = Image.fromarray(result)

product.save("out.jpg")

pixels = product.load()
width, height = product.size

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
input("Press enter to CANCEL (If debug mode is on, it will output all strings)")
if debugmode:
    print(outputlist)