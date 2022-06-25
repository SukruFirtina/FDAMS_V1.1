import threading
from tkinter import Tk, DoubleVar, IntVar, StringVar
from tkinter.ttk import Progressbar, Label, Style
import tkinter as tk
import pandas as pd
import numpy as np

window = Tk()
label_information = Label()

process_progress_bar = Progressbar()
read_progress_bar = Progressbar()

pb_style = Style()
s = Style()
fps_variable = DoubleVar()
fps_variable.set("1")  #default
exit_check = False
crop_pixels_file_path = "res/crop_pixels.csv"
video_file_path = "yeni.mp4" #şimdilik
data_place = StringVar(value='Not Selected')
cropping_selection = StringVar()
crop_options = {"DEFAULT": "res/crop_pixels.csv",
                "DEFAULT2": "res/crop_pixels_default2.csv",
                "INDIVIDUAL": "res/crop_pixels_individual.csv",
                "BROWSE FILE": ""}

#crop_pixels_file_path = "res/crop_pixels.csv"
image_frames = 'image_frames'
is_high_FPS = False


thread_map = {}
t_m = 0
flag = False
map_ready=False
select_coords = []
selecting = False
cropping_selection.set("DEFAULT")

text_FPS = tk.Label(window)

colors = {}
crops_pixels_df = pd.read_csv(crop_pixels_file_path)

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
    global exit_check
    global cropping_selection
    global crop_options
    global crop_pixels_file_path
    global data_place
    global video_file_path
    global text_FPS
    global colors
    global crops_pixels_df



