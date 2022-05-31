import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import Menu
from tkinter.messagebox import askyesno

import os
import csv
from datetime import datetime

import numpy as np
import pandas as pd

from scipy.io import wavfile
import sounddevice as sd


root = tk.Tk()
root.title("Speech Task Controller")
root.withdraw()


#######################################
#### FOLDER AND STARTUP MANAGEMENT ####
#######################################

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Check for existing data folder
if os.path.isdir(_thisDir + os.sep + 'data' + os.sep):
    print("Found data folder.")
else:
    print("No data folder found; creating one.")
    os.mkdir(_thisDir + os.sep + 'data' + os.sep)
    isdir = os.path.isdir(_thisDir + os.sep + 'data' + os.sep)
    if isdir:
        print("Data folder created successfully.")
    else:
        print("Problem creating data folder.")


def params_manager():
    global expInfo
    # Look for previous parameters file
    try:
        df = pd.read_csv('lastParams.csv',
            header=None, index_col=0)
        expInfo = df.to_dict()
        expInfo = expInfo[1] # to_dict returns a list
    except:
        print('Using default dictionary')
        expInfo = {'subject':'999', 'condition':'SPIN', 'speaker':3, 'level':65.0}

    # Get current date/time
    now = datetime.now()
    expInfo['stamp'] = now.strftime("%Y_%b_%d_%H%M")

params_manager()



def startup_win():
    ###########################
    #### BEGIN TKINTER GUI ####
    ###########################
    global expInfo
    # Make root window
    winStartParams = tk.Tk()
    winStartParams.title('Session Parameters')
    winStartParams.withdraw()

    # Create startup parameters frames
    frmStartup = ttk.Frame(winStartParams)
    frmStartup.grid(column=0,row=0,sticky='NSEW', padx=10, pady=10)
    frmStartup.columnconfigure(0, weight=1)
    frmStartup.rowconfigure(0, weight=1)

    frmStartup2 = ttk.Frame(winStartParams)
    frmStartup2.grid(column=0,row=1,sticky='NSEW', padx=10, pady=10)
    frmStartup2.columnconfigure(0, weight=1)
    frmStartup2.rowconfigure(0, weight=1)

    params_manager()

    # Create labels and entries for startup params
    # Values filled from params file or default dict
    entries = []
    text = tk.StringVar()
    for idx, key in enumerate(expInfo):
        # Labels
        ttk.Label(frmStartup,text=str(key).capitalize() + ': ').grid(column=0,row=idx,sticky='E')
        # Entry boxes
        text = str(expInfo[key])
        myEntry = ttk.Entry(frmStartup,textvariable=text)
        myEntry.insert(0,text)
        if key == 'stamp':
            myEntry.config(state = 'disabled')
        myEntry.grid(column=1,row=idx,sticky='W')
        entries.append(myEntry)

    # Write startup params to lastParams.csv
    def startup_params():
        """ Collect param values and write to file.
        """
        keys = list(expInfo.keys())
        with open('lastParams.csv', 'w', newline='') as f:
            for idx, entry in enumerate(entries):
                print(entry.get())
                writer = csv.writer(f)
                writer.writerow([keys[idx], entry.get()])
        params_manager()
        winStartParams.destroy()

    # Save button
    btnSave = ttk.Button(frmStartup2,text="Save",command=startup_params)
    #btnSave.bind('<Return>', startup_params)
    btnSave.focus()
    btnSave.grid(column=0,row=len(expInfo)+1)

    # Cancel without saving button
    ttk.Button(frmStartup2,text="Cancel",command=lambda: winStartParams.destroy()).grid(column=1,
        row=len(expInfo)+1)

    # Center root based on new size
    winStartParams.update_idletasks()
    #root.attributes('-topmost',1)
    window_width = winStartParams.winfo_width()
    window_height = winStartParams.winfo_height()
    # get the screen dimension
    screen_width = winStartParams.winfo_screenwidth()
    screen_height = winStartParams.winfo_screenheight()
    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    # set the position of the window to the center of the screen
    winStartParams.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    winStartParams.resizable(False, False)
    winStartParams.deiconify()

    winStartParams.mainloop()

###############
#### BEGIN ####
###############
# Menu
def confirm_exit():
    answer = askyesno(title='Really?',
        message='Are you sure you want to quit?')
    if answer:
        root.destroy()

# create a menubar
menubar = Menu(root)
root.config(menu=menubar)

# create the File menu
file_menu = Menu(menubar, tearoff=False)

# add menu items to the File menu
file_menu.add_command(
    label='New Session',
    command=startup_win
)

file_menu.add_separator()

file_menu.add_command(
    label='Exit',
    command=confirm_exit
)

# add the File menu to the menubar
menubar.add_cascade(
    label="File",
    menu=file_menu
)

# create the help menu
help_menu = Menu(
    menubar,
    tearoff=0
)

# add items to the Help menu
help_menu.add_command(label='Welcome')
help_menu.add_command(label='About...')

# add the Help menu to the menubar
menubar.add_cascade(
    label="Help",
    menu=help_menu
)

#root.columnconfigure([0,1], weight=1)
#root.rowconfigure([0,1,2], weight=1)

myFont = font.nametofont('TkDefaultFont').configure(size=16)

options = {'padx':15, 'pady':15}
options_word = {'padx':5, 'pady':5}

def next():
    #status.set("Presenting...")
    status.set(str(expInfo['subject']))

frmStatus = ttk.Frame(root) # padding=10
frmStatus.grid(column=0, columnspan=2, row=0, **options)

frmSentence = ttk.LabelFrame(root, text='Sentence:') # padding=10
frmSentence.grid(column=0, row=1, **options)

frmScore = ttk.Frame(root)
frmScore.grid(column=0, columnspan=2, row=2, sticky="W")

frmBtn = ttk.Frame(root) # padding=10
frmBtn.grid(column=1, row=1, sticky="S", **options)


status = tk.StringVar()
status.set("Ready")
lblStatus = ttk.Label(frmStatus, textvariable=status, anchor="center", width=10, borderwidth=2, relief="groove")
lblStatus.config(font=('TkDefaultFont', 30))
lblStatus.grid(column=0, row=0, sticky="N", ipadx=10, ipady=10, **options)

# Words
lblWord1 = ttk.Label(frmSentence, text="word1")
lblWord1.grid(column=0, row=1, sticky="N", **options_word)

lblWord2 = ttk.Label(frmSentence, text="word2")
lblWord2.grid(column=1, row=1, sticky="N", **options_word)

lblWord3 = ttk.Label(frmSentence, text="word3")
lblWord3.grid(column=2, row=1, sticky="N", **options_word)


# Checkbutton
chk1 = tk.StringVar(value=0)
chkWord1 = ttk.Checkbutton(frmSentence, text='', takefocus=0, variable=chk1)
chkWord1.grid(column=0, row=2, **options_word)

chk3 = tk.StringVar(value=0)
chkWord3 = ttk.Checkbutton(frmSentence, text='', takefocus=0, variable=chk3)
chkWord3.grid(column=2, row=2, **options_word)


# Score label
correct = 0
total= 0
try:
    percent_cor = correct/total*100
except:
    percent_cor = 0
score = tk.StringVar()
score.set(f'{correct} of {total} = {percent_cor}% correct')
lblScore = ttk.Label(frmScore, textvariable=score) # padding=10
lblScore.grid(column=0, row=0, sticky="W", **options)


# Button
btnNext = ttk.Button(frmBtn, text="Next", command=next)
btnNext.grid(column=0, row=0, sticky="N")




# Center root based on new size
root.update_idletasks()
#root.attributes('-topmost',1)
window_width = root.winfo_width()
window_height = root.winfo_height()
# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)
root.deiconify()




root.mainloop()
