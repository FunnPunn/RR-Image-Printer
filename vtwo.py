import numpy as np
from pynput.keyboard import Key, Controller, Listener
from pynput.mouse import Button, Controller
import pyperclip
import math
from PIL import Image
import itertools
import time

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
    if key == key.ctrl:
        holdingctrl = True
    elif key == key.k:
        if holdingctrl:
            textboxpos = bind.position
            print("Set textbox position!")
    elif key == key.l:
        if holdingctrl:
            donebuttonpos = bind.position
            print("Set done button position!")
    elif key == key.p:
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
                
            

def on_release(key):
    if key == key.ctrl:
        holdingctrl = False
        
# Collect events until released
listener = Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

im = Image.open("test.png")
newsize = (1000, 1000)
im = im.resize(newsize)

im = np.asarray(im)
new_shape = (im.shape[0],im.shape[1],1,3)

image = im.reshape(im.shape[0],im.shape[1],1,3)


totalcolors ={
    (224, 83, 80)  :"$",
    (210, 30, 45)  :"₼",
    (127, 24, 42)  :"¥",
    (133, 52, 57)  :"₱",
    (235, 128, 80) :"=",
    (238, 95, 47)  :"≠",
    (194, 61, 42)  :"≈",
    (135, 71, 57)  :">",

    (240, 208, 100):"<",
    (239, 192, 46) :"≥",
    (184, 102, 38) :"≤",
    (139, 99, 63)  :"(",
    (147, 174, 81) :")",
    (116, 160, 44) :"[",
    (50, 81, 42)   :"]",
    (75, 86, 55)   :"+",

    (116, 184, 115):"-",
    (0, 103, 50)   :"±",
    (0, 64, 42)    :"*",
    (55, 79, 63)   :"×",
    (116, 210, 187):"÷",
    (1, 154, 128)  :"/",
    (1, 83, 76)    :"—",
    (59, 90, 83)   :".",

    (114, 194, 215):"^",
    (0, 168, 213)  :"√",
    (0, 90, 111)   :"%",
    (56, 94, 102)  :"‰",
    (113, 159, 221):"Δ",
    (8, 108, 201)  :"|",
    (0, 61, 120)   :"π",
    (55, 83, 114)  :"∞",

    (171, 134, 220):"{",
    (89, 31, 201)  :"}",
    (49, 31, 113)  :"!",
    (97, 77, 113)  :"∑",
    (223, 148, 220):"∏",
    (130, 71, 123) :"γ",
    (72, 31, 76)   :"φ",
    (98, 66, 91)   :"†",

    (232, 121, 164):"μ",
    (230, 52, 80)  :"σ",
    (139, 24, 69)  :"α",
    (114, 61, 79)  :"β",
    (134, 69, 45)  :"δ",
    (77, 45, 45)   :"ε",
    (69, 36, 42)   :"ζ",
    (37, 24, 39)   :"θ",

    (198, 133, 90) :"ι",
    (151, 102, 74) :"κ",
    (100, 69, 60)  :"λ",
    (37, 36, 45)   :"ξ",
    (240, 229, 211):"ς",
    (193, 183, 169):"τ",
    (161, 148, 135):"υ",
    (133, 121, 112):"ψ",

    (108, 102, 98) :"?",
    (83, 77, 79)   :"¤",
    (45, 52, 60)   :"¨",
    (31,32,36)     :"'",
    (24,24,24)     :"`",
    (255,255,255)  :"§" 
}

colors = list(totalcolors.keys())

# Create color container 
## It has same dimensions as image (1000,1000,number of colors,3)
colors_container = np.ones(shape=[image.shape[0],image.shape[1],len(colors),3])
for i,color in enumerate(colors):
    colors_container[:,:,i,:] = color



def closest(image,color_container):
    shape = image.shape[:2]
    total_shape = shape[0]*shape[1]

    # calculate distances
    ### shape =  (x,y,number of colors)
    distances = np.sqrt(np.sum((color_container-image)**2,axis=3))

    # get position of the smalles distance
    ## this means we look for color_container position ????-> (x,y,????,3)
    ### before min_index has shape (x,y), now shape = (x*y)
    #### reshaped_container shape = (x*y,number of colors,3)
    min_index = np.argmin(distances,axis=2).reshape(-1)
    # Natural index. Bind pixel position with color_position
    natural_index = np.arange(total_shape)

    # This is due to easy index access
    ## shape is (1000*1000,number of colors, 3)
    reshaped_container = colors_container.reshape(-1,len(colors),3)

    # Pass pixel position with corresponding position of smallest color
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