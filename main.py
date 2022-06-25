import subprocess
import threading
import tkinter as tk
import PIL.Image
from PIL import ImageTk
import gui_tools
import ocr
import tools
from gui_tools import *
from ocr import get_text, process
import webview
import time
import sys
import time
#from screeninfo import get_monitors
#import pyautogui
# import psutil


def start_process():
    #vid = tools.files(env.image_frames)
    #process(vid)
    if not env.is_high_FPS:
        get_text()


def thread_handling():
    t = threading.Thread(target=start_process)
    if not t.is_alive():
        t.daemon = True
        t.start()
    else:
        t.join()
        t = threading.Thread(target=start_process)
        t.daemon = True
        t.start()



def fun():
    print(threading.active_count())


env.thread_map[env.t_m] = threading.Thread(target=tools.create_kml)
env.t_m = 0



def thread_handling_for_map():
    print('t_m', env.t_m)
    print('len', env.thread_map.__len__())
    print('act thre', threading.active_count())



    tools.create_kml()



    if env.map_ready==True:
        webwindow=webview.create_window('FDAMS', "map.html", width=1920,height=1080)
        webwindow.events.closed+=env.window.deiconify
        webview.start(env.window.withdraw())


def show_fps(self):
    env.text_FPS.configure(text=str(env.fps_variable.get()))

def start_window():
    process_frame = tk.Frame(env.window, bg="black")
    process_frame.place(x=0, y=0, width=130, height=1000)

    back_icon = PIL.Image.open("res/back.png")
    back_icon = back_icon.resize((65, 65))
    back_icon = ImageTk.PhotoImage(back_icon)
    back_btn = tk.Button(process_frame, image=back_icon, command=lambda:[process_frame.destroy(),  env.text_FPS.destroy()], background='black',
                         activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    back_btn.image = back_icon
    back_btn.place(x=30, y=30)

    env.text_FPS = tk.Label(env.window, text=str(env.fps_variable.get()), fg="white", background='black')
    env.text_FPS.place(x=98, y=147)


    fps_icon = PIL.Image.open("res/fps_icon.png")
    fps_icon = fps_icon.resize((70, 70))
    fps_icon = ImageTk.PhotoImage(fps_icon)
    fps_values = ("0.15", "0.2", "0.5", "1", "2", "3", "4", "5")
    select_fps = tk.OptionMenu(process_frame, env.fps_variable, *fps_values, command=show_fps)
    select_fps.config(image=fps_icon, background='black', borderwidth=0, highlightthickness=0, activebackground="black")
    CreateToolTip(select_fps, text='Select FPS')
    select_fps.image = fps_icon
    select_fps.place(x=30, y=150)

    show_ocr_places_icon = PIL.Image.open("res/show_ocr_places.png")
    show_ocr_places_icon = show_ocr_places_icon.resize((70, 70))
    show_ocr_places_icon = ImageTk.PhotoImage(show_ocr_places_icon)
    check_ocr_btn = tk.Button(process_frame, image=show_ocr_places_icon, command=ocr.check_ocr, background='black',
                         activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    check_ocr_btn.image = show_ocr_places_icon
    check_ocr_btn.place(x=30, y=240)

    browse_file_icon = PIL.Image.open("res/browse_folder.png")
    browse_file_icon = browse_file_icon.resize((70, 70))
    browse_file_icon = ImageTk.PhotoImage(browse_file_icon)
    browse_file_btn = tk.Button(process_frame, image=browse_file_icon, command=gui_tools.browse_files, background='black',
                         activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    browse_file_btn.image = browse_file_icon
    browse_file_btn.place(x=30, y=420)

    start_ocr_icon = PIL.Image.open("res/start_ocr.png")
    start_ocr_icon = start_ocr_icon.resize((110, 110))
    start_ocr_icon = ImageTk.PhotoImage(start_ocr_icon)
    start_ocr_btn = tk.Button(process_frame, image=start_ocr_icon, command=thread_handling, background='black',
                         activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    start_ocr_btn.image = start_ocr_icon
    start_ocr_btn.place(x=10, y=600)

    set_pixels_icon = PIL.Image.open("res/set_pixels.png")
    set_pixels_icon = set_pixels_icon.resize((70, 70))
    set_pixels_icon = ImageTk.PhotoImage(set_pixels_icon)

    env.cropping_selection.set(list(env.crop_options.keys())[0])
    dropdown = tk.OptionMenu(
        process_frame,
        env.cropping_selection,
        #list(env.crop_options.keys())[0],
        *list(env.crop_options.keys()),
        command=ocr.select_option_cropping
    )
    dropdown.config(image=set_pixels_icon, background='black', borderwidth=0, highlightthickness=0, activebackground="black")
    dropdown.image = set_pixels_icon
    dropdown.place(x=30, y=330)

    show_csv_icon = PIL.Image.open("res/show_csv_icon.png")
    show_csv_icon = show_csv_icon.resize((70, 70))
    show_csv_icon = ImageTk.PhotoImage(show_csv_icon)
    show_csv_btn = tk.Button(process_frame, image=show_csv_icon, command=show_csv, background='black',
                              activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    show_csv_btn.image = show_csv_icon
    show_csv_btn.place(x=30, y=510)

def earth_on_web():
    webwindow = webview.create_window('Google Earth', "https://earth.google.com/", width=1920, height=1080)
    webwindow.events.closed += env.window.deiconify
    webview.start(env.window.withdraw())

def open_kml_file():
    filename = "files/flight.kml"
    os.system("start " + filename)


def show_kml():
    show_kml_frame = tk.Frame(env.window, bg="black")
    show_kml_frame.place(x=0, y=0, width=130, height=1000)

    back_icon = PIL.Image.open("res/back.png")
    back_icon = back_icon.resize((65, 65))
    back_icon = ImageTk.PhotoImage(back_icon)
    back_btn = tk.Button(show_kml_frame, image=back_icon, command=show_kml_frame.destroy, background='black',
                         activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    back_btn.image = back_icon
    back_btn.place(x=30, y=30)


    simulate_icon = PIL.Image.open("res/earth_pc.png")
    earth_pc_icon = simulate_icon.resize((80, 80))
    earth_pc_icon = ImageTk.PhotoImage(earth_pc_icon)
    back_btn = tk.Button(show_kml_frame, image=earth_pc_icon, command=open_kml_file, background='black',
                         activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    back_btn.image = earth_pc_icon
    back_btn.place(x=25, y=180)

    show_kml_icon = PIL.Image.open("res/earth_web.png")
    show_kml_icon = show_kml_icon.resize((80, 80))
    show_kml_icon = ImageTk.PhotoImage(show_kml_icon)
    show_kml_btn = tk.Button(show_kml_frame, image=show_kml_icon, command=earth_on_web, background='black',
                         activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    show_kml_btn.image = show_kml_icon
    show_kml_btn.place(x=25, y=270)





def mapping_window():
    mapping_frame = tk.Frame(env.window, bg="black")
    mapping_frame.place(x=0, y=0, width=130, height=1000)

    back_icon = PIL.Image.open("res/back.png")
    back_icon = back_icon.resize((70, 70))
    back_icon = ImageTk.PhotoImage(back_icon)
    back_btn = tk.Button(mapping_frame, image=back_icon, command=mapping_frame.destroy, background='black',
                           activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    back_btn.image = back_icon
    back_btn.place(x=30, y=30)

    simulate_icon = PIL.Image.open("res/simulating_icon.png")
    simulate_icon = simulate_icon.resize((70, 70))
    simulate_icon = ImageTk.PhotoImage(simulate_icon)
    simulate_btn = tk.Button(mapping_frame, image=simulate_icon, command=thread_handling_for_map, background='black',
                         activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    simulate_btn.image = simulate_icon
    simulate_btn.place(x=25, y=180)

    show_kml_icon = PIL.Image.open("res/3d_kml_icon.png")
    show_kml_icon = show_kml_icon.resize((80, 80))
    show_kml_icon = ImageTk.PhotoImage(show_kml_icon)
    show_kml_btn = tk.Button(mapping_frame, image=show_kml_icon, command=show_kml, background='black',
                         activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    show_kml_btn.image = show_kml_icon
    show_kml_btn.place(x=25, y=268)

    show_csv_icon = PIL.Image.open("res/show_csv_icon.png")
    show_csv_icon = show_csv_icon.resize((70, 70))
    show_csv_icon = ImageTk.PhotoImage(show_csv_icon)
    show_csv_btn = tk.Button(mapping_frame, image=show_csv_icon, command=show_csv, background='black',
                             activebackground="#ff73c8", relief=FLAT, borderwidth=0)
    show_csv_btn.image = show_csv_icon
    show_csv_btn.place(x=30, y=365)

env.init()
env.window.title('FLIGHT DATA ANALYSER AND FLIGHT SIMULATER')
env.window.geometry("1280x720")
env.window.overrideredirect(True)
env.window.resizable(False, False)

background_img = PIL.Image.open("res/background_img.png")
background_img = background_img.resize((1280,800))
background_img = ImageTk.PhotoImage(background_img)
background_label = Label(env.window, image=background_img)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

exit_icon = PIL.Image.open("res/exit_icon.png")
exit_icon = exit_icon.resize((35, 35))
exit_icon = ImageTk.PhotoImage(exit_icon)

minimize_icon = PIL.Image.open("res/minimize_icon.png")
minimize_icon = minimize_icon.resize((17, 17))
minimize_icon = ImageTk.PhotoImage(minimize_icon)

start_icon = PIL.Image.open("res/start_icon.png")
start_icon = start_icon.resize((100, 100))
start_icon = ImageTk.PhotoImage(start_icon)

mapping_icon = PIL.Image.open("res/mapping.png")
mapping_icon = mapping_icon.resize((85, 85))
mapping_icon = ImageTk.PhotoImage(mapping_icon)


# Create a File Explorer label
label_window = tk.Label(env.window,
                        text="FLIGHT DATA ANALYSER AND SIMULATER",
                        fg="white", background='black')

label_window.config(font=("Verdana", 14))
env.label_information = tk.Label(env.window,
                                 text="",
                                 fg="red", background='black')

env.label_information.config(font=("Verdana", 15))

env.label_information2 = tk.Label(env.window,
                                  text="WELCOME",
                                  fg="gray", background='black', font=("Verdana", 18))

label_window.after(3000, env.label_information2.destroy)

label_buttons = tk.Label(env.window, background='black')


logo = PIL.Image.open("res/logo.png")
logo = logo.resize((50, 50))
logo = ImageTk.PhotoImage(logo)
logo_btn = tk.Button(label_window, image=logo, background='black',
                        activebackground="#ff73c8", relief=FLAT, borderwidth=0)
logo_btn.image = logo
logo_btn.place(x=335, y=6)

button_start_process = tk.Button(env.window, image=start_icon, command=start_window, relief=FLAT, borderwidth=0)
button_start_process.config(bg="black")

button_exit = tk.Button(env.window, command=exit, width=35, height=35, background='black', image=exit_icon)
button_simulate = tk.Button(env.window, image=mapping_icon, command=mapping_window, background='black',
                            relief=FLAT,
                            borderwidth=0)
button_simulate.config(font=("Verdana", 9))


button_minimize = tk.Button(env.window, width=35, height=35, command=minimize_window,
                            background='black', image=minimize_icon)

CreateToolTip(button_simulate, text='Simulate On Map\nShow KML File')
CreateToolTip(button_start_process, text='Start to process')

label1 = tk.Label(env.window, background='black')
label1.place(x=0, y=700, width=1280, height=60)
label2 = tk.Label(env.window, background='black')
label2.place(x=1278, y=0, width=20, height=1000)

label_window.place(x=0, y=0, width=1280, height=60)
env.label_information2.place(x=127, y=525, width=1000, height=50)
env.label_information.place(x=127, y=525, width=1000, height=50)
label_buttons.place(x=0, y=0, width=130, height=1000)


button_simulate.place(x=18, y=400)
button_start_process.place(x=11, y=270)
button_exit.place(x=1230, y=10)
button_minimize.place(x=1175, y=10)

env.s.theme_use("alt")
env.s.configure("TProgressbar", thickness=5, background='yellow', troughcolor='black')

env.read_progress_bar = Progressbar(env.window, orient=HORIZONTAL,
                                    length=500, mode='determinate', style="TProgressbar")

env.process_progress_bar = Progressbar(env.window, orient=HORIZONTAL,
                                       length=500, mode='determinate', style="TProgressbar")


center(env.window)
env.window.mainloop()

