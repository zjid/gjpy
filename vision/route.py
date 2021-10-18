ABLE = '''
Example:
You want to summarize your around-the-world-in-80-days in a couple of frames.
Background image is the 1872 world map.
Front image is your profile picture.

Steps to do:
1. Generate a route.
2. Run and save.

Expected commands:
$ python route.py to/back.jpg to/front.png to/route.json to/route.mp4
will generate, run, and save
$ python route.py gen back.png route.json
will generate route.json
$ python route.py run back.jpg front.jpg route.json route.mp4
will run and save route.mp4 frame by frame
'''

import cv2
import json
import numpy as np
from sys import argv

