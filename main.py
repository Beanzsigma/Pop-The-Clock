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
        afterid = app.after(20, animate, (frame_index + 1) % len(frames))  #speed change latr
    animate()
    return canvas, canvasbg
canvas, canvasbg = gifbg()
def clear(canvas, canvas_img):
    for item in canvas.find_all():
        if item != canvas_img:
            canvas.delete(item)
needle_raw = Image.open(getpath("Assets/needle.png")).convert('RGBA')
padded = Image.new('RGBA', (310, 260), (0, 0, 0, 0))
padded.paste(needle_raw, (97, 0))
scale = 1.6
needle_img = padded.resize((int(292 * scale), int(260 * scale)), Image.NEAREST)
needle_frames = []
for i in range(1080):
    angle = i * (360 / 1080)
    rotated = needle_img.rotate(-angle, resample=Image.BICUBIC, expand=False)
    needle_frames.append(ImageTk.PhotoImage(rotated))
needle_angle = 0
def rotate_needle():
    global needle_angle
    needle_angle = (needle_angle + 8) % 1080
    canvas.itemconfig(needle, image=needle_frames[needle_angle])
    canvas._needle = needle_frames[needle_angle]
    app.after(20, rotate_needle)
def maingame(canvas, canvas_img):
    global needle
    clear(canvas, canvas_img)
    canvas.create_text(353, 23, text='POP THE CLOCK!', font=("Press Start 2P", 22), fill="#968d8d", anchor='center')
    canvas.create_text(350, 20, text="POP THE CLOCK!", font=("Press Start 2P", 22), fill="#ffffff", anchor='center')
    canvas._needle = needle_frames[0]
    needle = canvas.create_image(350, 350, anchor='center', image=needle_frames[0])
    canvas.lift(needle)
maingame(canvas, canvasbg)
rotate_needle()
app.mainloop()