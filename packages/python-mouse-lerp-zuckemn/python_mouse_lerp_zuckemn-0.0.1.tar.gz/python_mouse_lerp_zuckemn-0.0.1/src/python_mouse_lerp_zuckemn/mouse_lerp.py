import noise
import argparse
import numpy as np
import random
import ctypes

def __mouse_pos():
    user32 = ctypes.windll.user32
    point = ctypes.wintypes.POINT()
    user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y

def __linear_interpolation(p0, p1, t):
    return (1 - t) * p0 + t * p1

def __quadratic_bezier(p0, p1, p2, num_points=65000):
    t_values = np.linspace(0, 1, num_points)
    curve_points = []
    for t in t_values:
        alpha_x = noise.pnoise1(5.46)
        alpha_y = noise.pnoise1(5.46)
        p01 = __linear_interpolation(p0, p1, t)
        p12 = __linear_interpolation(p1, p2, t)
        curve_points.append(__linear_interpolation(p01 + alpha_x, p12 + alpha_y, t))
    return np.array(curve_points)

def lerp(x, y):
    mouse_x, mouse_y = __mouse_pos()
    mouse_x = round(mouse_x)
    mouse_y = round(mouse_y)
    p0 = np.array([mouse_x, mouse_y])
    p1 = np.array([abs(mouse_x - x)/(random.random() + random.randrange(1, 2)), abs(mouse_y - y)/(random.random() + random.randrange(1, 2))])
    p2 = np.array([x, y])
    
    path = __quadratic_bezier(p0, p1, p2)
    
    for x, y in path:
        ctypes.windll.user32.SetCursorPos(int(x), int(y))
    #make sure cursor's precisely at the right position
    ctypes.windll.user32.SetCursorPos(int(x), int(y))

    