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
$ python route.py gen back.png route.json
will generate route.json
$ python route.py run back.jpg front.jpg route.json movie.mp4
will run and save movie.mp4 frame by frame
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

# Generating
# function to capture nodes from mouse event
# creates window and callback
# calculations
# writes route.json file

# Running
# function to combine two images, import another script for modularity
# code to support features
# generates in-between nodes
# save each frame for each node into movie file
