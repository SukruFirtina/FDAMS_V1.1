import threading
from tkinter import Tk, DoubleVar
from tkinter.ttk import Progressbar, Label, Style

import pandas as pd

window = Tk()
label_information = Label()

process_progress_bar = Progressbar()
read_progress_bar = Progressbar()

pb_style = Style()
s = Style()
fps_variable = DoubleVar()


image_frames = 'image_frames'
is_high_FPS = False

thread_map = {}
t_m = 0
flag = False
map_ready=False
select_coords = []
selecting = False

def init():
    global window
    global label_information
    global process_progress_bar
    global read_progress_bar
    global pb_style
    global s
    global fps_variable
    global image_frames
    global is_high_FPS
    global thread_map
    global t_m
    global flag
    global map_ready
    global select_coords, selecting, image, clone



