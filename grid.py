import tkinter as tk
from tkinter import StringVar, ttk
import pandas as pd
import numpy as np

root = tk.Tk()
root.title("Presentation Controller")
window_width = 800
window_height = 600
# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
#root.resizable(False, False)


root.columnconfigure([0,1], weight=1)
root.rowconfigure([0,1], weight=1)

frm1 = ttk.Frame(root, padding=10)
frm1.grid(column=0, row=0, ipadx=10, ipady=10)

frm2 = ttk.Frame(root, padding=10)
frm2.grid(column=1, row=0, ipadx=10, ipady=10)

frm5 = ttk.Frame(root, padding=10)
frm5.grid(column=0, row=1, ipadx=10, ipady=10)

lbl1 = ttk.Label(frm1, text="C")
lbl1.grid(column=1, row=1)

lbl2 = ttk.Label(frm1, text="N")
lbl2.grid(column=1, row=0)

lbl3 = ttk.Label(frm1, text="S")
lbl3.grid(column=1, row=2)

lbl4 = ttk.Label(frm1, text="W")
lbl4.grid(column=0, row=1)

lbl5 = ttk.Label(frm1, text="E")
lbl5.grid(column=2, row=1)

lbl6 = ttk.Label(frm1, text="SE")
lbl6.grid(column=2, row=2)

lbl7 = ttk.Label(frm2, text="C")
lbl7.grid(column=0, row=0)

lbl = ttk.Label(frm5, text="C")
lbl.grid(column=0, row=0)

# root row/colum configure carves up the root window into grids spaces (coordinates)
# THEN, a frame can be assigned to any coordinate (cell) on the root
# THEN, a widget can be placed NSEW in the frame, which will be contained in the root cell


root.mainloop()
