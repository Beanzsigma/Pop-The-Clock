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
        afterid = app.after(35, animate, (frame_index + 1) % len(frames))  # change speed here when making menu thingy
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
shadow_frames = []
for i in range(500):
    angle = i * (360 / 500)
    rotated = needle_img.rotate(-angle, resample=Image.BICUBIC, expand=False)
    needle_frames.append(ImageTk.PhotoImage(rotated))
    r, g, b, a= rotated.split()
    a = a.point(lambda x: x*0.4)
    shadow= Image.merge('RGBA', [r.point(lambda x: 0), g.point(lambda x: 0), b.point(lambda x: 0), a])
    shadow_frames.append(ImageTk.PhotoImage(shadow))
needle_angle = 0
needledir = 1
def rotate_needle():
    global needle_angle
    needle_angle = (needle_angle + 8 * needledir) % 500    #here change speed
    canvas.itemconfig(shadow, image=shadow_frames[needle_angle])
    canvas._shadow = shadow_frames[needle_angle]
    canvas.itemconfig(needle, image=needle_frames[needle_angle])
    canvas._needle = needle_frames[needle_angle]
    app.after(10, rotate_needle)
def flipdirection(e=None):
    global needledir
    needledir *= -1
    degrees = (needle_angle / 500) * 360
    number = int((degrees / 30 +3.3)% 12) or 12
    numberclick(number)
canvas.bind("<Button-1>", flipdirection)
canvas.bind("<space>", flipdirection)
lasthigh = [None]
numhigh = {}
def highlightnumb():
    degrees = (needle_angle / 500) * 360
    number = int((degrees / 30+ 3.3) % 12) or 12
    if lasthigh[0] != number:
        if lasthigh[0] in numhigh:
            canvas.itemconfig(numhigh[lasthigh[0]], fill="white")
        if number in numhigh:
            canvas.itemconfig(numhigh[number], fill="#353232")
        lasthigh[0] = number
    app.after(10, highlightnumb)
fading = {}
def numberclick(number):
    if number not in numhigh:
        return
    fading[number] = 255 
    execfade(number)
def execfade(number):
    if number not in fading:
        return
    intensity = fading[number]
    if intensity <= 0:
        canvas.itemconfig(numhigh[number], fill='white')
        del fading[number]
        return
    r = int(255 * (1 - intensity / 255))
    g = 255
    b = int(255 * (1 - intensity / 255))
    color = f'#{r:02x}{g:02x}{b:02x}'
    canvas.itemconfig(numhigh[number], fill=color)
    fading[number] = intensity -4
    app.after(16, execfade, number)
def normal(canvas, canvas_img):
    global needle, shadow
    clear(canvas, canvas_img)
    canvas.create_text(353, 23, text='POP THE CLOCK!', font=("Press Start 2P", 22), fill="#968d8d", anchor='center')
    canvas.create_text(350, 20, text="POP THE CLOCK!", font=("Press Start 2P", 22), fill="#ffffff", anchor='center')
    numhigh[12] = canvas.create_text(351, 143, text='12', font=("Press Start 2P", 20), fill="#968d8d", anchor='center')
    numhigh[12] = canvas.create_text(348, 140, text="12", font=("Press Start 2P", 20), fill="white", anchor='center')
    numhigh[1] = canvas.create_text(453, 184, text='1', font=("Press Start 2P", 20), fill="#968d8d", anchor='center')
    numhigh[1] = canvas.create_text(450, 181, text='1', font=("Press Start 2P", 20), fill='white', anchor='center')
    numhigh[2] = canvas.create_text(517, 263, text='2', font=("Press Start 2P", 20), fill='#968d8d', anchor='center')
    numhigh[2] = canvas.create_text(514, 260, text='2', font=("Press Start 2P", 20), fill='white', anchor='center')
    numhigh[3] = canvas.create_text(541, 353, text='3', font=("Press Start 2P",20), fill="#967d8d", anchor='center')
    numhigh[3]= canvas.create_text(538, 350, text='3', font=("Press Start 2P", 20), fill="white", anchor='center')
    numhigh[4] = canvas.create_text(517, 443, text='4', font=("Press Start 2P", 20), fill="#967d8d", anchor='center')
    numhigh[4] = canvas.create_text(514, 440, text='4', font=("Press Start 2P", 20), fill="white", anchor='center')
    numhigh[5] = canvas.create_text(453, 516, text='5', font=("Press Start 2P", 20), fill="#967d8d", anchor='center')
    numhigh[5]= canvas.create_text(450, 513, text='5', font=("Press Start 2P", 20), fill='white', anchor='center') 
    numhigh[6] = canvas.create_text(353, 553, text='6', font=("Press Start 2P", 20), fill='#967d8d', anchor='center')
    numhigh[6] = canvas.create_text(350, 550, text="6", font=("Press Start 2P", 20), fill="white", anchor='center')
    numhigh[7] = canvas.create_text(253, 516, text='7', font=("Press Start 2P", 20), fill='#967d8d', anchor='center')
    numhigh[7]= canvas.create_text(250, 513, text='7', font=('Press Start 2P', 20), fill="white", anchor='center')
    numhigh[8] = canvas.create_text(167, 443, text='8', font=('Press Start 2P', 20), fill='#967d8d', anchor='center')
    numhigh[8] = canvas.create_text(164, 440, text='8', font=("Press Start 2P", 20), fill='white', anchor='center')
    numhigh[9] = canvas.create_text(155, 353, text='9', font=("Press Start 2P", 20), fill='#967d8d', anchor='center')
    numhigh[9] = canvas.create_text(152, 350, text='9', font=("Press Start 2P", 20), fill='white', anchor='center')
    numhigh[10] = canvas.create_text(179, 263, text='10', font=("Press Start 2P", 20), fill='#967d8d', anchor='center')
    numhigh[10] = canvas.create_text(176, 260, text='10', font=("Press Start 2P", 20), fill='white', anchor='center')
    numhigh[11] = canvas.create_text(250, 184, text='11', font=("Press Start 2P", 20), fill='#967d8d', anchor='center')
    numhigh[11] = canvas.create_text(247, 181,text='11', font=("Press Start 2P", 20), fill='white', anchor='center' )
    canvas._needle = needle_frames[0]
    shadow = canvas.create_image(354, 354, anchor='center', image=needle_frames[0])
    canvas._shadow = shadow_frames[0]
    needle = canvas.create_image(350, 350, anchor='center', image=needle_frames[0])
    canvas.lift(shadow)
    canvas.lift(needle)
normal(canvas, canvasbg)
rotate_needle()
highlightnumb()



app.mainloop()