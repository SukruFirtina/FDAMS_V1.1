import csv
import os
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import tkinter as tk
import PySimpleGUI as sg
import environment as env
import sys
import PIL
from PIL import ImageTk
from tkinter import Tk, DoubleVar, IntVar, StringVar
from tkinter.ttk import Progressbar, Label, Style, Frame, Button




class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "9", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


def show_csv():

    csv_file = 'files/fixed_output.csv'
    with open(csv_file, "r") as infile:
        reader = csv.reader(infile)
        header_list = next(reader)
        data = list(reader)
    sg.SetOptions(element_padding=(0, 10),
                  background_color='black')
    #col_widths = list(map(lambda x: len(x)+4, data[3]))
    #col_widths = list(map(lambda x: len(x), header_list))


    layout = [
        [sg.Table(
            key='table1',
            values=data,
            headings=header_list,
            # max_col_width=10,
            auto_size_columns=False,
            justification='center',
            background_color='#444444',
            alternating_row_color='black',
            num_rows=40,
            #col_widths = col_widths,
            def_col_width=10,
            enable_events=True,
            vertical_scroll_only= False)],
    ]
    window = sg.Window(
        size=(1920, 800),
        title='CSV File',
        return_keyboard_events=True,
        grab_anywhere=False).Layout(layout)

    while True:
        event, values = window.Read()

        if event is None or event == 'Exit':
            window.close()
            break

        if event == 'Escape:27':  # Exit on ESC
            window.close()
            break
    env.s.theme_use("alt")
    return mainloop()


def browse_files():
    file_path = filedialog.askopenfilename(initialdir="/",
                                            title="Select a File",
                                            filetypes=(("Video",
                                                        "*.mp4*"),
                                                       ("csv file",
                                                        "*.csv")))
    if file_path == "":
        env.label_information.configure(text="File could not be opened !!! " + file_path)
    else:
        env.label_information.configure(text="File Opened: " + file_path)

    env.video_file_path = file_path

def browse_csv():
    file_path = filedialog.askopenfilename(initialdir="/",
                                            title="Select a CSV File",
                                           filetypes=(("csv file",
                                                       "*.csv*"),
                                                      ))
    return file_path

def minimize_window():
    env.window.wm_state('iconic')
    env.window.iconify()


def restart_program():
    os.execl(sys.executable, '"{}"'.format(sys.executable), *sys.argv)

    python = sys.executable
    os.execl(python, python, *sys.argv)


def change_label():
    env.label_information['text'] = "kjhkhk"


def center(win, pyqt=False):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()





