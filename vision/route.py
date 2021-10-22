ABLE = '''
Example:
You want to summarize your around-the-world-in-80-days in a couple of frames.
Background image is the 1872 world map.
Front image is your profile picture.
Your picture will walk on the map representing your adventure.

Steps to do:
1. You generate a route.
2. This script runs and saves the result.

Expected commands:
$ python route.py back.jpg front.png route.json movie.mp4
will generate, run, and save
# $ python route.py gen back.png route.json
# will generate route.json
# $ python route.py run back.jpg front.jpg route.json movie.mp4
# will run and save movie.mp4 frame by frame
'''

UNABLE = '''
This script can't do it beautifully.
This script creates route based on one side flat map, not spherical world.
'''

import cv2
import json
import numpy as np
from sys import argv

# treat file path accordingly
path_back = argv[1]
path_front = argv[2]
path_route = argv[3]
path_movie = argv[4]
im_back = cv2.imread(path_back)
im_front = cv2.imread(path_front, cv2.IMREAD_UNCHANGED)

## Generating
judul = 'Generating route'
# function to capture nodes from mouse event
daftar_garis = []
def menggaris(event, x, y, flags, param):
  if event == cv2.EVENT_LBUTTONDOWN:
    daftar_garis.append([y,x])
    print(f'[I] Start point {[y,x]} saved.')
  elif event == cv2.EVENT_LBUTTONUP:
    daftar_garis[-1] += [y,x]
    print(f'[I] End point {[y,x]} saved.')
  elif event == cv2.EVENT_RBUTTONDOWN:
    print(f'[I] Line {daftar_garis.pop()} erased.')
# creates window and callback
cv2.namedWindow(judul)
cv2.setMouseCallback(judul, menggaris)
cv2.imshow(judul, im_back)
cv2.displayStatusBar(judul, 'Every node is a line. Create line by drag from one point to another.')
cv2.waitKey()
cv2.destroyAllWindows()
# calculations
peta = {
  'titik': [],
  'jalur': [[]]
}
for i,garis in enumerate(daftar_garis):
  ya,xa,yb,xb = garis
  yc = (ya + yb) // 2
  xc = (xa + xb) // 2
  s = np.sqrt( (ya - yb)**2 + (xa - xb)**2 )
  s = int(s)
  peta['titik'].append([yc,xc,s])
  peta['jalur'][0].append(i) # you can add route manually
# writes route.json file
with open(path_route, 'w') as f:
  json.dump(peta, f)

# Running
judul = 'Running and saving movie'
# function to combine two images, import another script for modularity
# code to support features
# generates in-between nodes
# save each frame for each node into movie file
