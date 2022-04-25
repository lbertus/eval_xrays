# from pathlib import Path, PureWindowsPath
from tkinter import filedialog
from PIL import Image, ImageTk
from pathlib import Path
from tkinter import ttk
import tkinter as tk
import configparser
# import shutil
# import time
# import glob
import os
# from tkinter import *


class APP:

    def __init__(self, root):
        # create renamed X-ray folder strings
        self.image1 = None
        self.tk_image = None
        self.rename_folder_pystr = ""
        self.pass_folder_pystr = ""
        self.fail_folder_pystr = ""

        # get previous rename X-ray folders from ini file
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')  # path of .ini file
        self.rename_folder_pystr = self.config.get("Settings", "xray_rename_folder")
        self.pass_folder_pystr = self.config.get("Settings", "xray_pass_folder")
        self.fail_folder_pystr = self.config.get("Settings", "xray_fail_folder")

        # setup tk
        root.title('Login')
        # self.resizable(0, 0)
        root.title("Evaluate X-Ray renamed images")
        root.geometry('1000x500+50+50')  # set tk window size

        # UI options
        paddings = {'padx': 5, 'pady': 5}
        # entry_font = {'font': ('Helvetica', 11)}

        # configure the grid
        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=3)
        # self.rowconfigure(0, weight=10)

        # set the label and text variables
        self.rename_folder_tk = tk.StringVar()
        self.pass_folder_tk = tk.StringVar()
        self.fail_folder_tk = tk.StringVar()

        # configure label and button styles
        self.style = ttk.Style(root)
        self.style.configure('Heading.TLabel', font=('Helvetica', 12))
        self.style.configure('TLabel', font=('Helvetica', 11))  # , foreground="black", background="white")
        self.style.configure('TButton', font=('Helvetica', 11))  # relief styles: flat, sunken, raised, groove, ridge

        mainframe = tk.Frame(root)
        mainframe.grid(column=0, row=0)

        # Window heading
        heading = ttk.Label(mainframe, text='X-ray renamed, pass and fail folders', style='Heading.TLabel')
        # heading.grid(column=0, row=0, columnspan=2, pady=5, sticky=tk.N)
        heading.grid(column=0, row=0, sticky=tk.W, **paddings)

        # x-ray renamed folder button
        rename_folder_button = ttk.Button(mainframe, text="Select X-ray renamed folder",
                                          command=self.select_rename_folder, style='TButton')
        rename_folder_button.grid(column=0, row=1, sticky=tk.W, **paddings)

        # X-ray x-ray renamed folder label
        rename_folder_heading = ttk.Label(mainframe, text="You selected this X-ray renamed folder:", style='TLabel')
        rename_folder_heading.grid(column=0, row=2, sticky=tk.W, **paddings)

        # X-ray source selected location label
        rename_folder_entry = ttk.Label(mainframe, textvariable=self.rename_folder_tk, style='TLabel')
        rename_folder_entry.grid(column=0, row=3, sticky=tk.W, **paddings)
        self.rename_folder_tk.set(self.rename_folder_pystr)  # from init file

        # x-ray pass folder button
        pass_folder_button = ttk.Button(mainframe, text="Select passed X-ray folder", command=self.select_pass_folder,
                                        style='TButton')
        pass_folder_button.grid(column=0, row=4, sticky=tk.W, **paddings)

        # X-ray pass folder label
        pass_folder_heading = ttk.Label(mainframe, text="You selected this pass folder:", style='TLabel')
        pass_folder_heading.grid(column=0, row=5, sticky=tk.W, **paddings)

        # X-ray selected pass location label/entry
        pass_folder_entry = ttk.Label(mainframe, textvariable=self.pass_folder_tk, style='TLabel')
        pass_folder_entry.grid(column=0, row=6, sticky=tk.W, **paddings)
        self.pass_folder_tk.set(self.pass_folder_pystr)

        # x-ray fail folder button
        fail_folder_button = ttk.Button(mainframe, text="Select fail X-ray folder", command=self.select_fail_folder,
                                        style='TButton')
        fail_folder_button.grid(column=0, row=7, sticky=tk.W, **paddings)

        # X-ray fail folder label
        fail_folder_heading = ttk.Label(mainframe, text="You selected this fail folder:", style='TLabel')
        fail_folder_heading.grid(column=0, row=8, sticky=tk.W, **paddings)

        # X-ray selected fail location label/entry
        fail_folder_entry = ttk.Label(mainframe, textvariable=self.fail_folder_tk, style='TLabel')
        fail_folder_entry.grid(column=0, row=9, sticky=tk.W, **paddings)
        self.fail_folder_tk.set(self.fail_folder_pystr)

        # process X-rays
        evaluate_folder_button = ttk.Button(mainframe, text="Evaluate rename X-rays ", command=self.evaluate_xrays)
        evaluate_folder_button.grid(column=0, row=10, sticky=tk.W, **paddings)

    # select rename folder button pressed
    def select_rename_folder(self):
        self.rename_folder_pystr = tk.filedialog.askdirectory(title='Select X-Ray Rename folder')
        self.rename_folder_tk.set(self.rename_folder_pystr)
        config_file = Path('config.ini')  # Path of .ini file
        self.config.read(config_file)
        self.config.set('Settings', 'xray_rename_folder', self.rename_folder_pystr)  # Updating existing entry
        self.config.write(config_file.open("w"))

    # select pass folder button pressed
    def select_pass_folder(self):
        self.pass_folder_pystr = tk.filedialog.askdirectory(title='Select X-Ray pass folder')
        self.pass_folder_tk.set(self.pass_folder_pystr)
        config_file = Path('config.ini')  # Path of .ini file
        self.config.read(config_file)
        self.config.set('Settings', 'xray_pass_folder', self.pass_folder_pystr)  # Writing new entry
        self.config.write(config_file.open("w"))

    # select fail folder button pressed
    def select_fail_folder(self):
        self.fail_folder_pystr = tk.filedialog.askdirectory(title='Select X-Ray fail folder')
        self.fail_folder_tk.set(self.fail_folder_pystr)
        config_file = Path('config.ini')  # Path of .ini file
        self.config.read(config_file)
        self.config.set('Settings', 'xray_fail_folder', self.fail_folder_pystr)  # Writing new entry
        self.config.write(config_file.open("w"))

    # button pressed
    def evaluate_xrays(self):
        # print('\n-------------------- Start of app -------------------------------')
        print('\nrename_folder path:', self.rename_folder_pystr)
        print('\nrename_folder contents:', os.listdir(self.rename_folder_pystr))
        print('\npass_folder path:', self.pass_folder_pystr)
        print('\npass_folder contents:', os.listdir(self.pass_folder_pystr))
        print('\nfail_folder path:', self.fail_folder_pystr)
        print('\nfail_folder contents:', os.listdir(self.fail_folder_pystr))

        rename_images = os.listdir(self.rename_folder_pystr)
        print(rename_images)
        print(rename_images[0])

        # for img in rename_images:
        #     self.image1 = Image.open(os.path.join(self.rename_folder_pystr, img))
        #     self.tk_image = ImageTk.PhotoImage(self.image1)
        #     label1 = ttk.Label(image=self.tk_image)
        #     label1.grid(column=1, row=0, sticky=tk.W)
        #     break

        r = tk.Toplevel()
        r.title("My image")

        self.image1 = Image.open(os.path.join(self.rename_folder_pystr, rename_images[0]))
        self.tk_image = ImageTk.PhotoImage(self.image1)
        label1 = ttk.Label(r, image=self.tk_image)
        # label1.grid(column=1, row=0, sticky=tk.W)

        label1.image = self.tk_image
        label1.place(x=0, y=0)

        r.mainloop()    # work without???


def main():
    root = tk.Tk()
    APP(root)  # instantiate APP object, Tk root window
    root.mainloop()  # enter Tk root window event loop


if __name__ == '__main__':
    main()
