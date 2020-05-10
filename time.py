import tkinter as tk

root = tk.Tk()

def quit():
    None

def snooz():
    None

canvas = tk.Canvas(root, height = 300, width = 300)

close_button = tk.Button(canvas, text='Close Alarm', font=('verdana', 10), command=lambda: quit())
snooz_button = tk.Button(canvas, text='Snooz', font=('verdana', 10), command=lambda: snooz())


canvas.pack()
root.mainloop()


