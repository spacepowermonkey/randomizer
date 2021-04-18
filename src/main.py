import secrets

import numpy as np



import render



def make_random_layer(shape, scaling):
    X,Y = shape

    new_layer = np.zeros((X * scaling, Y * scaling), dtype=np.uint8)

    for x in range(X):
        for y in range(Y):
            sx = slice(x*scaling, (x+1)*scaling)
            sy = slice(y*scaling, (y+1)*scaling)

            value = secrets.choice([0,255])
            new_layer[sx, sy] = value

    return new_layer

def insert_tracker(layer, shape, offset, value):
    dx,dy = shape
    x,y = offset

    sx = slice(x, x+dx)
    sy = slice(y, y+dy)

    layer[sx, sy] = value
    return

def make_tracker_seq(base_shape, base_scale, tracker_shape, tracker_offset, tracker_step, reverse=False):
    bs = base_scale
    bx,by = base_shape
    ts = tracker_step
    tx,ty = tracker_shape
    tox,toy = tracker_offset

    frames = []
    base_layer = make_random_layer(base_shape, base_scale)
    print(base_layer.shape)
    for i in range((bs*by - ty) // ts): # This won't hit the far edge on a scan!
        frame = np.copy(base_layer)
        if not reverse:
            insert_tracker(frame, tracker_shape, (tox,toy+i*ts), 127)
        if reverse:
            insert_tracker(frame, tracker_shape, (tox,toy+(by*bs-i*ts-ty)), 127)
        frames.append(frame)
    
    return frames



if __name__=="__main__":
    # x is vertical; y is horizontal
    x = 100
    y = 2*x
    s = 4

    frames = []
    for val in [False, True]*6:
        frames += make_tracker_seq((x,y), s, (x,x), ((x*s-x)//2,0), 10, reverse=val)
    for i in range(len(frames)):
        render.layer2bmp(frames[i], i)
    render.bmp2mp4((x*s,y*s))
