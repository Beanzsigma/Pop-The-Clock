import customtkinter as ctk
from tkinter import Canvas, filedialog
afterid = None
from PIL import Image, ImageSequence, ImageTk
app = ctk.CTk()
app.title("Pop The Clock!")
app.geometry("700x700")  
# def getpath(relative_path):
#     try:
#         base_path = sys._MEIPASS
#     except AttributeError:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)
# FR_PRIVATE = 0x10
# def load_font(font_path):
#     windll.gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)
import sys
import os
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
    for widget in app.winfo_children():
        widget.destroy()
    frames = []
    gif = Image.open(getpath("Assets/outlinebg.gif"))
    for frame in ImageSequence.Iterator(gif):
        frame= frame.copy().convert("RGBA")
        r, g, b, a = frame.split()
        a= a.point(lambda x:x*0.4)
        frame.putalpha(a)
        frames.append(ImageTk.PhotoImage(frame.resize((700, 700))))
    canvas = Canvas(app, width=700, height=700, highlightthickness=0, bd=0, bg='black')
    canvas.place(x=0, y=0)
    app.update()
    canvasbg = canvas.create_image(0, 0, anchor='nw')
    canvas._frames = frames
    def animate(frame_index=0):
        global afterid
        canvas.itemconfig(canvasbg, image=frames[frame_index])

        afterid = app.after(20, animate, (frame_index+1) % len(frames))
    animate()
    return canvas, canvasbg
app.update()
canvas, canvasbg = gifbg()
app.mainloop()
