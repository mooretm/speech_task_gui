import tkinter as tk
from tkinter import ttk
from tkinter import font

root = tk.Tk()
root.title("Presentation Controller")
root.withdraw()

#root.columnconfigure([0,1], weight=1)
#root.rowconfigure([0,1,2], weight=1)


myFont = font.nametofont('TkDefaultFont').configure(size=16)


options = {'padx':15, 'pady':15}
options_word = {'padx':5, 'pady':5}

def next():
    status.set("Ready")

frmStatus = ttk.Frame(root) # padding=10
frmStatus.grid(column=0, columnspan=2, row=0, **options)

frmSentence = ttk.LabelFrame(root, text='Sentence:') # padding=10
frmSentence.grid(column=0, row=1, **options)

frmScore = ttk.Frame(root)
frmScore.grid(column=0, columnspan=2, row=2, sticky="W")

frmBtn = ttk.Frame(root) # padding=10
frmBtn.grid(column=1, row=1, sticky="S", **options)


status = tk.StringVar()
status.set("Presenting...")
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
correct = 7
total= 20
percent_cor = correct/total*100
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
