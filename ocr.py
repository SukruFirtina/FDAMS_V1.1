import os
from tkinter import BOTTOM, S

import PIL
import cv2
import numpy as np
import pandas as pd
import easyocr
from PIL import ImageTk

import environment as env
import gui_tools
from data_correction import fix_df
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import ttk
import threading
from tkinter import messagebox
import random



def process(src_vid):
    env.flag = True

    env.process_progress_bar.pack(pady=10, side=BOTTOM, anchor=S)

    video_len = int(src_vid.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = src_vid.get(cv2.CAP_PROP_FPS)
    frame_range = int(fps / env.fps_variable.get())

    index = 1
    if env.fps_variable.get() <= int(fps):
        env.is_high_FPS = False
        while src_vid.isOpened():

            prog = int(100 * index / video_len)
            env.process_progress_bar['value'] = prog
            env.window.update_idletasks()

            ret, frame = src_vid.read()
            if not ret:
                break

            # name each frame and save as png
            if index < 10:
                name = './image_frames/frame000' + str(index) + '.png'
            elif index < 100:
                name = './image_frames/frame00' + str(index) + '.png'
            elif index < 1000:
                name = './image_frames/frame0' + str(index) + '.png'
            else:
                name = './image_frames/frame' + str(index) + '.png'

            if index % frame_range == 0:
                print('Extracting frames ...' + name)

                # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                # lower = np.array([39, 50, 125])
                # upper = np.array([178, 255, 255])
                # mask = cv2.inRange(hsv, lower, upper)
                #
                # mask = fix_image(mask)

                cv2.imwrite(name, frame)

            index = index + 1

            # if cv2.waitKey(10) & 0xFF == ord('q'):
            #    break

        env.label_information.configure(text='Video frames are extracted')
        src_vid.release()
        # cv2.destroyAllWindows()
    else:
        env.label_information.configure(text="The FPS value you selected is higher than the FPS value of the video.\n"
                                             "FPS of video is:" + str(fps))
        env.is_high_FPS = True



def get_text():
    env.read_progress_bar.pack(pady=10, side=BOTTOM, anchor=S)

    if env.flag == True:

        try:
            os.remove("cropped_images")
        except OSError:
            pass

        if not os.path.exists("cropped_images"):
            os.makedirs("cropped_images")

        # progress['value'] = 0

        data = {
            'day': [],
            'month': [],
            'year': [],
            'hour': [],
            'min': [],
            'sec': [],
            'degree_lat': [],
            'minute_lat': [],
            'second_lat': [],
            'direction_lat': [],
            'degree_lon': [],
            'minute_lon': [],
            'second_lon': [],
            'direction_lon': [],
            'heading_angle': [],
            'target_degree_lat': [],
            'target_minute_lat': [],
            'target_second_lat': [],
            'target_direction_lat': [],
            'target_degree_lon': [],
            'target_minute_lon': [],
            'target_second_lon': [],
            'target_direction_lon': [],
        }

        reader = easyocr.Reader(['en'])
        df = pd.DataFrame(data)
        crops_pixels_df = pd.read_csv(env.crop_pixels_file_path)
        crop = {}



        j = 0
        for i in os.listdir(env.image_frames): # Dosyadaki tüm frameleri okuyor !!! HATA
            print(str(i))
            frame = cv2.imread(env.image_frames + "/" + i)

            for col_name in crops_pixels_df.columns:
                crop[col_name] = frame[crops_pixels_df[col_name][0]:     crops_pixels_df[col_name][1] ,   crops_pixels_df[col_name][2] :   crops_pixels_df[col_name][3]]



            k = 0

            text = {'frame': i}

            for c in crop.keys():

                if c == 'month':
                    text[c] = reader.readtext(crop[c], allowlist='ABCDEFGHIJKLMNOPRSTUVWXYZ')
                elif c == 'direction_lat' or c == 'target_direction_lat':
                    text[c] = reader.readtext(crop[c], allowlist='SN')
                elif c == 'direction_lon' or c == 'target_direction_lon':
                    text[c] = reader.readtext(crop[c], allowlist='EW')
                else:
                    text[c] = reader.readtext(crop[c], allowlist='0123456789')

                cv2.imwrite("cropped_images/" + i + "_" + str(k) + '.' + c + ".png", crop[c])

                # image = cv2.imread("cropped_images/" + i + "_" + str(k) + '.' + c + ".png")
                # print(image)

                k += 1
                if text[c] != []:
                    text[c] = (text[c][0][1].replace(" ", ""))
                    print(text[c])

                j += 1
                prog = int(100 * j / (os.listdir(env.image_frames).__len__() * crop.__len__()))
                env.read_progress_bar['value'] = prog
                env.window.update_idletasks()

            df = df.append(text, ignore_index=True)
        df.to_csv('files/unfixed_output.csv', index=False)

    else:
        df = pd.read_csv('files/unfixed_output.csv')

        df['month'] = (df['month']).astype(str)
        df['direction_lat'] = (df['direction_lat']).astype(str)
        df['direction_lon'] = (df['direction_lon']).astype(str)
        df['year'] = (df['year']).astype(str)

    df = fix_df(df)

    df.to_csv('files/fixed_output.csv', index=False)

    env.label_information.configure(text='CSV file is complete')

    env.read_progress_bar['value'] = 100
    env.window.update_idletasks()


def region_selection(event, x, y, flags, param):


    if event == cv2.EVENT_LBUTTONDOWN:
        # Left mouse button down: begin the selection.
        # The first coordinate pair is the centre of the square.
        env.select_coords = [(x, y)]
        env.selecting = True

    elif event == cv2.EVENT_MOUSEMOVE and env.selecting:
        # If we're dragging the selection square, update it.
        env.image = env.clone.copy()
        x0, y0, x1, y1 = (x, y, *env.select_coords[0])
        cv2.rectangle(env.image, (x0, y0), (x1, y1), (0, 255, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        # Left mouse button up: the selection has been made.
        env.select_coords.append((x, y))
        env.selecting = False

def thread_handling_cropping():
    t = threading.Thread(target=set_cropping_selection)
    if not t.is_alive():
        t.daemon = True
        t.start()
    else:
        t.join()
        t = threading.Thread(target=set_cropping_selection)
        t.daemon = True
        t.start()


def thread_handling_region_selection(event, x, y, flags, param):
    t = threading.Thread(target=region_selection(event, x, y, flags, param))
    if not t.is_alive():
        t.daemon = True
        t.start()
    else:
        t.join()
        t = threading.Thread(target=region_selection(event, x, y, flags, param))
        t.daemon = True
        t.start()

def selected_rectangle(crops_pixels_df, img):
    if (env.data_place.get() != "Not Selected"):
        cv2.rectangle(img, (crops_pixels_df[env.data_place.get()][3], crops_pixels_df[env.data_place.get()][1]),
                      (crops_pixels_df[env.data_place.get()][2], crops_pixels_df[env.data_place.get()][0]), color=(0,0,255), thickness=2)

    return img

def draw_rectangles(crops_pixels_df, img):
    #cv2.rectangle(img1, pt1=(400,200), pt2=(100,50), color=(255,0,0), thickness=10))

    for col_name in crops_pixels_df.columns:
        #env.colors[i] = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
        cv2.rectangle(img, (crops_pixels_df[col_name][3],crops_pixels_df[col_name][1] ),(crops_pixels_df[col_name][2],crops_pixels_df[col_name][0]), color = (0,0,255),thickness=2)

    return img,

def check_ocr():
    #env.window.withdraw()
    crops_pixels_df = pd.read_csv(env.crop_pixels_file_path)

    cam = cv2.VideoCapture(env.video_file_path)

    try:
        if not os.path.exists('data'):
            os.makedirs('data')

    except OSError:
        print('Error')

    ret, frame = cam.read()
    if ret:
        name = 'frame_for_settings.png'
        print('Created...' + name)
        cv2.imwrite(name, frame)

    basename = os.path.basename('frame_for_settings.png')
    env.image = cv2.imread(basename)
    env.clone = env.image.copy()
    cv2.namedWindow(basename, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(basename, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)
    draw_rectangles(crops_pixels_df, env.image)

    while True:
        cv2.imshow(basename, env.image)


        key = cv2.waitKey(1) & 0xFF
        if key == ord("s") or key == 27 or cv2.getWindowProperty(basename, cv2.WND_PROP_VISIBLE) < 1:
            cv2.destroyAllWindows()
            break
    #env.window.deiconify()


def ShowChoice():
    print(env.data_place.get())


def set_crops_pixels_df():
    env.crops_pixels_df[env.data_place.get()][0] = y1
    env.crops_pixels_df[env.data_place.get()][1] = y0
    env.crops_pixels_df[env.data_place.get()][2] = x1
    env.crops_pixels_df[env.data_place.get()][3] = x0
    env.data_place.set("Not Selected")



open_save=False
def save_button():
    global open_save
    open_save = True
#    save_btn = Button(setCropsWindow, text='back to settings',
#                      command=lambda: [setCropsWindow.destroy(), exit_from_crop_screen()])
#    save_btn.grid(row=1, column=4)


y1 = 0
y0 = 0
x1 = 0
x0 = 0

def set_cropping_selection():
    env.window.withdraw()
    setCropsWindow = Toplevel(env.window)
    global y1, y0, x1, x0
    global save_btn
    env.crops_pixels_df = pd.read_csv(env.crop_pixels_file_path)



    setCropsWindow.attributes('-topmost', True)
    setCropsWindow.geometry("900x600")
    gui_tools.center(setCropsWindow)
    setCropsWindow.overrideredirect(True)

    #btn = Button(setCropsWindow, text='Set pixels for selected value', command=thread_handling_cropping)
    back_btn = Button(setCropsWindow, text='back to settings', command=lambda:[setCropsWindow.destroy(),exit_from_crop_screen()])



    #env.data_place.set(1)
    data_types = [('day'                 , 'day'                 ),
                 ('month'               , 'month'               ),
                 ('year'                , 'year'                ),
                 ('hour'                , 'hour'                ),
                 ('min'                 , 'min'                 ),
                 ('sec'                 , 'sec'                 ),
                 ]
    data_types2 = [
                  ('degree_lat', 'degree_lat'),
                  ('minute_lat', 'minute_lat'),
                  ('second_lat', 'second_lat'),
                  ('direction_lat', 'direction_lat'),
                  ('degree_lon', 'degree_lon'),
                  ('minute_lon', 'minute_lon'),
                  ('second_lon', 'second_lon'),
                  ('direction_lon', 'direction_lon'),
                  ('heading_angle', 'heading_angle'),
                  ('altitude', 'altitude')


                  ]

    data_types3 = [
        ('target_degree_lat', 'target_degree_lat'),
        ('target_minute_lat', 'target_minute_lat'),
        ('target_second_lat', 'target_second_lat'),
        ('target_direction_lat', 'target_direction_lat'),
        ('target_degree_lon', 'target_degree_lon'),
        ('target_minute_lon', 'target_minute_lon'),
        ('target_second_lon', 'target_second_lon'),
        ('target_direction_lon', 'target_direction_lon'),

    ]

    frame1 = LabelFrame(setCropsWindow)
    frame1.grid(row=1, column=1, padx=10)

    frame2 = LabelFrame(setCropsWindow)
    frame2.grid(row=1, column=2)

    frame3 = LabelFrame(setCropsWindow)
    frame3.grid(row=1, column=3)


    #Label(setCropsWindow,
    #         text="""Select the data type you want to set""",
    #         justify=LEFT).pack()

    for data_type, val in data_types:
                tk.Radiobutton(frame1,
                    text=data_type,
                    font=("arial", 10, "bold"),
                    indicator=0,
                    background="light green",
                    #padx=10,
                    #padx=20,
                    variable=env.data_place,
                    command=ShowChoice,
                    value=val).pack()

    for data_type, val in data_types2:
                tk.Radiobutton(frame2,
                    text=data_type,
                    font=("arial", 10, "bold"),
                    indicator=0,
                    background="light green",
                    #padx=40,


                    #padx=20,
                    variable=env.data_place,
                    command=ShowChoice,
                    value=val).pack()

    for data_type, val in data_types3:
                tk.Radiobutton(frame3,
                    text=data_type,
                    font=("arial", 10, "bold"),
                    indicator=0,
                    background="light green",
                    #padx=40,


                    #padx=20,
                    variable=env.data_place,
                    command=ShowChoice,
                    value=val).pack()



    #btn.pack()
    back_btn.grid(row=1, column=4)

    #env.window.attributes('-topmost', True)
    save_btn = Button(setCropsWindow, text='back to settings',
                      command=lambda: [set_crops_pixels_df()])
    save_btn.grid(row=1, column=5)


    cam = cv2.VideoCapture(env.video_file_path)
    try:
        if not os.path.exists('data'):
            os.makedirs('data')

    except OSError:
        print('Error')

    ret, frame = cam.read()
    if ret:
        name = 'frame_for_settings.png'
        print('Created...' + name)
        cv2.imwrite(name, frame)

    basename = os.path.basename('frame_for_settings.png')
    env.image = cv2.imread(basename)
    env.clone = env.image.copy()
    cv2.namedWindow(basename, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(basename, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)
    #cv2.setMouseCallback(basename, region_selection)

    while True:
        cv2.setMouseCallback(basename, thread_handling_region_selection)
        draw_rectangles(env.crops_pixels_df,env.image)
        cv2.imshow(basename, env.image)


        key = cv2.waitKey(1) & 0xFF
        #if key == ord("s") or key == 27 or cv2.getWindowProperty(basename, cv2.WND_PROP_VISIBLE) < 1 or env.exit == True:
        if env.exit_check == True:
            #HEPSİNİN KAYDI BURADA YAPILACAK
            env.data_place.set("Not Selected")
            env.crops_pixels_df.to_csv(env.crop_pixels_file_path)
            cv2.destroyAllWindows()
            #env.window.attributes('-topmost', False)
            break

        if len(env.select_coords) == 2:
            x1, y1 = env.select_coords[0]
            x0, y0 = env.select_coords[1]
            crop_values_dict = {}

            print(y1, y0, x1, x0)
            if (env.data_place.get() != "Not Selected"):
                env.image = selected_rectangle(env.crops_pixels_df,env.image)
                print('sfdg')



            else:
               warninglabel = tk.Label(setCropsWindow,
                                       text="Please Select DataType to set",
                                       fg="red", background='white', font=("arial", 10, "bold"))
               warninglabel.grid(row=2, column=4)
               warninglabel.after(10, warninglabel.destroy)
            #cv2.waitKey(0)
    env.exit_check = False
    env.window.deiconify()
    #cv2.rectangle(env.image, (x1, y1), (x2, y2), (255, 0, 0), 2) !!!! Gsötermk için kullanılacak

def select_option_cropping(self):
    selection = env.cropping_selection.get()

    if selection == "INDIVIDUAL":
        env.crop_pixels_file_path = "res/crop_pixels_individual.csv"
        thread_handling_cropping()

    elif selection == "DEFAULT":
        env.crop_pixels_file_path = "res/crop_pixels.csv"

    elif selection == "DEFAULT2":
        env.crop_pixels_file_path = "res/crop_pixels_default2.csv"

    elif selection == "BROWSE FILE":
        path = gui_tools.browse_csv()
        env.crop_pixels_file_path = path


def raise_frame(frame):
    frame.tkraise()

def exit_from_crop_screen():
    env.exit_check = True