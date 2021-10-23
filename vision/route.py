ABLE = '''
Example:
You want to summarize your around-the-world-in-80-days in a couple of frames.
Background image is the 1872 world map.
Front image is your profile picture.
Your picture will walk on the map representing your adventure.

Steps to do:
1. You generate a route.
2. This script runs and saves the movie.

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

## Generating
if argv[1] == 'gen':

  # treat file path accordingly
  path_back = argv[2]
  path_route = argv[3]
  im_back = cv2.imread(path_back)

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
elif argv[1] == 'run':

  # treat file path accordingly
  path_back = argv[2]
  path_front = argv[3]
  path_route = argv[4]
  path_movie = argv[5]
  im_back = cv2.imread(path_back)
  im_front = cv2.imread(path_front, cv2.IMREAD_UNCHANGED)
  with open(path_route, 'r') as f:
    p = json.load(f)

  judul = 'Running movie'
 
  # function to combine two images, import another script for modularity
  # from vision.timpa import timpa
  from timpa import timpa

  # code to support features
  # reverse route
  # out of frame
  # branch route
  # merge route
  piksel = 5 # distance between nodes
  fps = 20

  # generates in-between nodes
  halus = []
  for jalur in p['jalur']:
    alus = []
    for i in range(len(jalur) - 1):
      t0 = jalur[i]
      t1 = jalur[i+1]
      p0 = [y0, x0, s0] = p['titik'][t0]
      p1 = [y1, x1, s1] = p['titik'][t1]
      d = ( (y0 - y1) ** 2 + (x0 - x1) ** 2 ) ** 0.5
      langkah = int( d / piksel )
      pp = list(np.linspace(p0, p1, langkah).astype(int)) # semua titik dari t0 hingga sebelum t1
      alus += pp
    alus.append(p1)
    halus.append(alus)

  # save each frame for each node into movie file
  height, width = im_back.shape[:2]
  movie = cv2.VideoWriter(path_movie, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
  rute = halus[0]
  banyak = len(rute)
  for i,node in enumerate(rute):
    gambar = timpa( im_front, im_back.copy(), node )
    cv2.imshow(judul, gambar)
    cv2.displayStatusBar(judul, f'frame {i+1}/{banyak} posisi {str(p)}')
    movie.write(gambar)
    cv2.waitKey(1)

  movie.release()
  print('[I] Movie saved.')
  cv2.waitKey()
  cv2.destroyAllWindows()
