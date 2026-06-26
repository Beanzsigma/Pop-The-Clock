import customtkinter as ctk
from tkinter import Canvas
from PIL import Image, ImageSequence, ImageTk
import sys
import os
afterid = None
app = ctk.CTk()
app.title("Pop The Clock!")
app.geometry("700x700")
app.update()
def loadfont(font_path):
    if sys.platform != 'win32':
        return 
    from ctypes import windll
    FR_PRIVATE = 0x10
    windll.gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)
def getpath(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
def gifbg():
    global afterid
    if afterid:
        app.after_cancel(afterid)
    app.update()
    children = list(app.children.values())
    parent = children[0] if children else app
    frames = []
    gif = Image.open(getpath("Assets/outlinebg.gif"))
    for frame in ImageSequence.Iterator(gif):
        frame = frame.copy().convert("RGBA")
        r, g, b, a = frame.split()
        a = a.point(lambda x: x * 0.4)
        frame.putalpha(a)
        frames.append(ImageTk.PhotoImage(frame.resize((700, 700))))
    canvas = Canvas(parent, width=700, height=700,
                    highlightthickness=0, bd=0, bg='black')
    canvas.place(x=0, y=0)
    canvasbg = canvas.create_image(0, 0, anchor='nw')
    canvas._frames = frames
    def animate(frame_index=0):
        global afterid
        canvas.itemconfig(canvasbg, image=frames[frame_index])
        afterid = app.after(50, animate, (frame_index + 1) % len(frames))  #speed change latr
    animate()
    return canvas, canvasbg
canvas, canvasbg = gifbg()
def clear(canvas, canvas_img):
    for item in canvas.find_all():
        if item != canvas_img:
            canvas.delete(item)
needle_img = Image.open(getpath("Assets/needle.png")).convert('RGBA')
needle_img = needle_img.resize((430, 430), Image.NEAREST)
needle_photo = ImageTk.PhotoImage(needle_img)
def maingame(canvas, canvas_img):
    clear(canvas, canvas_img)
    canvas.create_text(353, 23, text='POP THE CLOCK!', font=("Press Start 2P", 22), fill="#968d8d", anchor='center')
    canvas.create_text(350, 20, text="POP THE CLOCK!", font=("Press Start 2P", 22), fill="#ffffff", anchor='center')
    needle = canvas.create_image(250, 365, anchor='w', image=needle_photo)
    canvas._needle = needle_photo
    canvas.lift(needle)

maingame(canvas, canvasbg)
app.mainloop()