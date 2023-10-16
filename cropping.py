import cv2
import random
import os

# define coordinates and filenames
coordinates = []
filenames = []

# open files and read the coordinates and the filenames in the lists
with open('D:/projects/blender/setup-production-01/coords005.txt', 'r') as filehandle:
    coordinates = [current_place.rstrip() for current_place in filehandle.readlines()]
with open('D:/projects/blender/setup-production-01/names005.txt', 'r') as filehandle:
    filenames = [current_place.rstrip() for current_place in filehandle.readlines()]
    
# print(coordinates[0])
# print(filenames)

i = 0
for render in filenames:
    # organize coordinates
    rendercoord = coordinates[i]
    rendercoord = rendercoord[1:-1]
    rendercoord = rendercoord.split(", ")
    i += 1
    # print(rendercoord)
    render = render + ".png"
    image = cv2.imread(render)
    x = int(rendercoord[0])
    y = int(rendercoord[1])
    endx = x + int(rendercoord[2])
    endy = y + int(rendercoord[3])
    #randomize coordinates
    #identify lengths
    xl = int(rendercoord[2]) * random.random() * 0.1
    yl = int(rendercoord[3]) * random.random() * 0.1
    x = round(x + xl * random.choice([-1,1]))
    endx = round(endx + xl * random.choice([-1,1]))
    y = round(y + yl * random.choice([-1,1]))
    endy = round(endy + yl * random.choice([-1,1]))
    print(x, endx, y, endy)
    crop_image = image[y:endy, x:endx]
    # filename = render[0:-4] + '-cropped.png'
    # below parameters can change
    filename = ""
    wholename = render.split("/")
    for k in range(4):
        filename = filename + wholename[k] + "/"
    filename = filename + wholename[4] + "-cropped/cropped-" + wholename[5]
    print(filename)
    cv2.imwrite(filename, crop_image)
