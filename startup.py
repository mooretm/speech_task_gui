import os
import csv
from datetime import datetime
import pandas as pd
import tkinter as tk
from tkinter import ttk


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

# Look for previous parameters file
try:
    df = pd.read_csv('lastParams.csv',
        header=None, index_col=0)
    expInfo = df.to_dict()
    expInfo = expInfo[1] # to_dict returns a list
except:
    print('Using default dictionary')
    expInfo = {'Subject':'999', 'Condition':'SPIN', 'Speaker':3, 'Level':65.0}

# Get current date/time
now = datetime.now()
expInfo['stamp'] = now.strftime("%Y_%b_%d_%H%M")


###########################
#### BEGIN TKINTER GUI ####
###########################
# Make root window
root = tk.Tk()
root.title('Session Parameters')
root.withdraw()

# Create startup parameters frames
frmStartup = ttk.Frame(root)
frmStartup.grid(column=0,row=0,sticky='NSEW', padx=10, pady=10)
frmStartup.columnconfigure(0, weight=1)
frmStartup.rowconfigure(0, weight=1)

frmStartup2 = ttk.Frame(root)
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
    """ Collect param values and write to file.
    """
    keys = list(expInfo.keys())
    with open('lastParams.csv', 'w', newline='') as f:
        for idx, entry in enumerate(entries):
            print(entry.get())
            writer = csv.writer(f)
            writer.writerow([keys[idx], entry.get()])
    root.destroy()

# Save button
btnSave = ttk.Button(frmStartup2,text="Save",command=startup_params)
#btnSave.bind('<Return>', startup_params)
btnSave.focus()
btnSave.grid(column=0,row=len(expInfo)+1)

# Cancel without saving button
ttk.Button(frmStartup2,text="Cancel",command=lambda: root.destroy()).grid(column=1,
    row=len(expInfo)+1)

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