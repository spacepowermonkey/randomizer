
import subprocess

import skimage.io as io
import numpy as np

def layer2bmp(layer, index):
    io.imsave("renders/stills/frame_{:0>5d}.bmp".format(index), layer)
    return

    
# WARING:
#   This runs into memory issues when called on large automata via Python.
#   However, the shell command works fine even on large automata when called directly from the terminal.    
def bmp2mp4(shape):
    subprocess.run(
        "ffmpeg -pattern_type glob -r 24 -i 'renders/stills/*.bmp' -vf scale={vwidth}:{vheight} -c:v libx264 -preset slow -crf 21 renders/clips/random.mp4".format(**{
            "vwidth":   shape[1],
            "vheight":  shape[0]
        }),
        shell=True, check=True
    )
    
    subprocess.run(
        "rm renders/stills/*.bmp",
        shell=True, check=True
    )
    
    return
    