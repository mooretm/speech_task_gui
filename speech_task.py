# tk inter imports
from textwrap import fill
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import Menu
from tkinter.messagebox import askyesno
# system type imports
import os
import csv
from datetime import datetime
# data science imports
import numpy as np
import pandas as pd
# audio imports
from scipy.io import wavfile
import sounddevice as sd

# Initialize root window
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
        expInfo = {'subject':'999', 'condition':'SPIN', 'speaker':3, 'level':65.0, 'lists':'1 2'}

    # Get current date/time
    now = datetime.now()
    expInfo['stamp'] = now.strftime("%Y_%b_%d_%H%M")

# Create expInfo dictionary
params_manager()

global list_counter
list_counter = 0

# Pull in text sentences
global sentences
global sentences_list
def get_sentences():
    global sentences
    global sentences_list
    df = pd.read_csv('.\\sentences\\IEEE-DF.csv')
    lists = expInfo['lists'].split()
    lists = [int(x) for x in lists]
    print(lists)
    sentences = df.loc[df['list_num'].isin(lists), 'ieee_text']
    sentences_list = list(sentences)

get_sentences()


myFont = font.nametofont('TkDefaultFont').configure(size=10)

options = {'padx':10, 'pady':10}
options_word = {'padx':0, 'pady':0}

# Frames for widget positioning
frmStatus = ttk.Frame(root)
frmStatus.grid(column=0, columnspan=2, row=0, **options)

frmSentence = ttk.LabelFrame(root, text='Sentence:')
frmSentence.grid(column=0, row=1, sticky='w', **options)

frmBtn = ttk.Frame(root)
frmBtn.grid(column=1, row=1, sticky="S", **options)

frmScore = ttk.Frame(root)
frmScore.grid(column=0, columnspan=2, row=2, sticky="W")

sep = ttk.Separator(root, orient='vertical')
sep.grid(column=2, row=0, rowspan=12, sticky='ns')

frmParams = ttk.LabelFrame(root, text="Parameters")
frmParams.grid(column=3, row=0, rowspan=2, sticky='nw',**options)

frmTrials = ttk.Frame(root)
frmTrials.grid(column=3, row=2, sticky='w',  **options)

def params_list():
    keys = list(expInfo.keys())
    print(keys)
    for idx, param in enumerate(expInfo):
        if param == 'stamp':
            pass
        else:
            lblLabel = ttk.Label(frmParams, text=keys[idx].capitalize() + ': ' + str(expInfo[param]))
            lblLabel.grid(column=0, row=idx, sticky='w')


def startup_win():
    ###########################
    #### BEGIN TKINTER GUI ####
    ###########################
    global expInfo
    global sentences
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
        global sentences
        """ Collect param values and write to file.
        """
        keys = list(expInfo.keys())
        with open('lastParams.csv', 'w', newline='') as f:
            for idx, entry in enumerate(entries):
                print(entry.get())
                writer = csv.writer(f)
                writer.writerow([keys[idx], entry.get()])
        params_manager()
        params_list()

        # Pull in text sentences
        get_sentences()
        winStartParams.destroy()

    # Save button
    btnSave = ttk.Button(frmStartup2,text="Save",command=startup_params)
    #btnSave.bind('<Return>', startup_params)
    btnSave.focus()
    btnSave.grid(column=0,row=len(expInfo)+1)

    # Cancel without saving button
    ttk.Button(frmStartup2,text="Cancel",command=lambda: winStartParams.destroy()).grid(column=1,
        row=len(expInfo)+1)

    # Center winStartParams  based on new size
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

params_list()

lblTrial = ttk.Label(frmTrials, text='Trial 0 of 0')
lblTrial.grid(column=0, row=0)

status = tk.StringVar()
status.set("Ready")
lblStatus = ttk.Label(frmStatus, textvariable=status, anchor="center", width=10, borderwidth=1, relief="groove")
lblStatus.config(font=('TkDefaultFont', 14))
lblStatus.grid(column=0, row=0, sticky="N", ipadx=5, ipady=5)

# Words
# Process current sentence for presentation
# and scoring.
theText = ''.join(sentences_list[list_counter]) # ['the dog is fast']
words = theText.split() # ['the' 'dog' 'is' 'fast']
nums = np.arange(0,len(words)) # index to ensure each word is a unique key
nums = [str(x) for x in nums] # turn into strings
# Append nums to words to ensure each word is a unique dict key
newWords = []
for i, word in enumerate(words):
    word = word + str(i)
    newWords.append(word)
# Prepopulate checkboxes to "off"
vals = np.zeros(len(words),dtype=int)
chkbox_dict = dict(zip(newWords,vals))
# Instantiate and display words and checkboxes
for counter, key in enumerate(chkbox_dict,start=0):
    chkbox_dict[key] = tk.IntVar()
    if key.isupper() and key != 'A':
        theWords = ttk.Label(frmSentence,text=newWords[counter][:-1])
        theWords.config(font=('TkDefaultFont 10 underline'))
        theWords.grid(column=counter,row=0)
        aCheckButton = ttk.Checkbutton(frmSentence,text='',takefocus=0,variable=chkbox_dict[key])
        aCheckButton.grid(column=counter,row=1)
    else:
        aCheckButton = ttk.Checkbutton(frmSentence,text='',takefocus=0,variable=chkbox_dict[key])
        #aCheckButton.grid(column=counter,row=4) # Do not display these checkboxes
        theWords = ttk.Label(frmSentence,text=newWords[counter][:-1]).grid(column=counter,row=0)


global cor_count
cor_count = 0

global incor_count
incor_count = 0

theScores = []
def score():
    global cor_count
    global incor_count
    global list_counter
    theScores = []
    for key, value in chkbox_dict.items():
        state = value.get()
        if state != 0:
            print('Correct! ' + key[:-1])
            theScores.append(1)
            chkbox_dict[key].set(0)
        else:
            if key.isupper() and key != 'A':
                print('Wrong! ' + key[:-1])
                theScores.append(0)
                chkbox_dict[key].set(0)
    # Mark correct or incorrect
    # Criterion: all keywords must have been correctly identified
    if all(ele > 0 for ele in theScores):
        cor_count += 1
    else:
        incor_count += 1

    total_count = cor_count + incor_count
    try:
        percent_cor = cor_count/total_count*100
    except:
        percent_cor = 0
    score_text.set(f'{cor_count} of {total_count} = {round(percent_cor,1)}% correct')
    lblTrial.config(text=f'Trial {total_count} of 20')
    print(theScores)
    list_counter += 1


score_text = tk.StringVar()
lblScore = ttk.Label(frmScore, textvariable=score_text, font=myFont) # padding=10
lblScore.grid(column=0, row=0, sticky="W", **options)
score_text.set('No data!')

# Button
btnNext = ttk.Button(frmBtn, text="Next", command=score)
btnNext.grid(column=0, row=0, sticky="N")



# Center root based on new size
root.update_idletasks()
#root.attributes('-topmost',1)
window_width = root.winfo_width()
window_height = root.winfo_height()
#window_width = 700
#window_height=300
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
