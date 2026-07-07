import customtkinter as ctk
from tkinter import Canvas
import random
targetnumber = [None]
clockminutes = [30]
generation = [0]
passedtarget = [False]
needle_on_target = [False]
needlespeed = [1]
equiped = [0]
from PIL import Image, ImageSequence, ImageTk
import sys
import threading
import os
firstpick = [True]
import time
inputlocked = [True]
gameover = [False]
instantlose = [False]
startclock = [30]
needleafter = [None]
highlightafter = [None]
afterid = None
app = ctk.CTk()
app.title("Pop The Clock!")
app.geometry("700x819")
app.resizable(False, False)
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
bottomafter = [None]
canvas = Canvas(app, width=700, height=819, highlightthickness=0, bd=0, bg='black')
canvas.place(x=0, y=0)
canvasbg = canvas.create_image(0, 0, anchor='nw')
def rounded_rect(canvas, x1, y1, x2, y2, r=20, color="#968d8d", width=2):
    items = []
    arc_kwargs = {"outline": color, "width": width}
    line_kwargs = {"fill": color, "width": width}
    items.append(canvas.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90, style="arc", **arc_kwargs))
    items.append(canvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, style="arc", **arc_kwargs))
    items.append(canvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, style="arc", **arc_kwargs))
    items.append(canvas.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, style="arc", **arc_kwargs))
    items.append(canvas.create_line(x1+r, y1, x2-r, y1, **line_kwargs))
    items.append(canvas.create_line(x1+r, y2, x2-r, y2, **line_kwargs))           
    items.append(canvas.create_line(x1, y1+r, x1, y2-r, **line_kwargs))
    items.append(canvas.create_line(x2, y1+r, x2, y2-r, **line_kwargs))
    return items
def gifbg():
    global afterid
    if afterid:
        app.after_cancel(afterid)
    frames = []
    gif = Image.open(getpath("Assets/outlinebg.gif"))
    for frame in ImageSequence.Iterator(gif):
        frame = frame.copy().convert("RGBA")
        r, g, b, a = frame.split()
        a = a.point(lambda x: x * 0.4)
        frame.putalpha(a)
        frames.append(ImageTk.PhotoImage(frame.resize((700, 700))))
    canvas._outlineframes = frames
    def animate(frame_index=0):
        global afterid
        canvas.itemconfig(canvasbg, image=frames[frame_index])
        afterid = app.after(35, animate, (frame_index + 1) % len(frames))
    animate()
def animatebottom():
    if 'bottombg' in canvas.__dict__:
        canvas.itemconfig(canvas._bottombg, image=bottombgframes[bottombgidx[0]])
        bottombgidx[0] = (bottombgidx[0]+1) % len(bottombgframes)
    bottomafter[0] = app.after(35, animatebottom)
bottombgidx = [0]
def clear(canvas, canvas_img):
    for item in canvas.find_all():
        if item != canvas_img and item not in loading_items:
            canvas.delete(item)
needle_raw = Image.open(getpath("Assets/needle.png")).convert('RGBA')
padded = Image.new('RGBA', (310, 260), (0, 0, 0, 0))
padded.paste(needle_raw, (97, 0))
scale = 1.6
needle_img = padded.resize((int(292 * scale), int(260 * scale)), Image.NEAREST)
import threading
loadingframes = []
loadinggif = Image.open(getpath("Assets/loading.gif"))
for frame in ImageSequence.Iterator(loadinggif):
    frame = frame.copy().convert("RGBA")
    loadingframes.append(ImageTk.PhotoImage(frame.resize((700, 800), Image.NEAREST)))
loadingimg = canvas.create_image(0, 0, anchor='nw', image=loadingframes[0])
loadinglabelshdw = canvas.create_text(353, 623, text='Loading...', font=("Press Start 2P", 18), fill='#968d8d')
loadingbottom = canvas.create_rectangle(0, 700, 700, 819, fill="#000000", outline="#000000")
loadinglabel = canvas.create_text(350, 620, text='Loading...', font=("Press Start 2P", 18), fill='white')
loadingcountshdw = canvas.create_text(353, 153, text='Frames rendered: 0\n    out of 210', font=('Press Start 2P', 18), fill='#968d8d')
loadingcount = canvas.create_text(350, 150, text='Frames rendered: 0\n    out of 210', font=("Press Start 2P", 18), fill='white' )
canvas._loadingframes = loadingframes
canvas.itemconfig(loadingimg, state='hidden')
canvas.itemconfig(loadinglabel, state='hidden')
canvas.itemconfig(loadinglabelshdw, state='hidden')
canvas.itemconfig(loadingcount, state='hidden')
canvas.itemconfig(loadingcountshdw, state='hidden')
canvas.itemconfig(loadingbottom, state='hidden')
loading_items = {loadingimg, loadinglabel, loadinglabelshdw, loadingcount, loadingcountshdw, loadingbottom}
loadingindx = [0]
loadingafter = [None]
loadingdone = threading.Event()
def animateloading():
    if loadingdone.is_set():
        return
    loadingindx[0] = (loadingindx[0] + 1) % len(loadingframes)
    canvas.itemconfig(loadingimg, image=loadingframes[loadingindx[0]])
    loadingafter[0] = app.after(50, animateloading)
animateloading()
needle_frames = []
shadow_frames = []
def prerender():
    needle_frames.clear()
    shadow_frames.clear()
    loadingdone.clear()
    loadingindx[0] = 0
    for i in range(210):
        angle = i * (360 / 210)
        rotated = needle_img.rotate(-angle, resample=Image.BICUBIC, expand=False)
        needle_frames.append(ImageTk.PhotoImage(rotated))
        r, g, b, a = rotated.split()
        a = a.point(lambda x: x * 0.4)
        shadow = Image.merge('RGBA', [r.point(lambda x: 0), g.point(lambda x: 0), b.point(lambda x: 0), a])
        shadow_frames.append(ImageTk.PhotoImage(shadow))
        app.after(0, lambda n=i+1: canvas.itemconfig(loadingcount, text=f"Frames rendered: {n}\n    out of 210"))
        app.after(0, lambda n=i+1: canvas.itemconfig(loadingcountshdw, text=f'Frames rendered: {n}\n    out of 210'))
    loadingdone.set()
    app.after(0, rendercomplete)
def rendercomplete():
    if loadingafter[0]:
        app.after_cancel(loadingafter[0])
    canvas.itemconfig(loadingimg, state='hidden')
    canvas.itemconfig(loadinglabel, state='hidden')
    canvas.itemconfig(loadinglabelshdw, state='hidden')
    canvas.itemconfig(loadingcount, state='hidden')
    canvas.itemconfig(loadingcountshdw, state='hidden')
    canvas.itemconfig(loadingbottom, state='hidden')
    gameover[0] = False
    inputlocked[0] = True
    clockminutes[0] = startclock[0]
    normal(canvas, canvasbg)
    newtarget()
    generation[0] += 1
    showcountdown(3, generation[0])
needle_angle = 0
needledir = 1
overlayitems = []
def showgameover(penalty=True):
    global needle_angle, needledir
    if penalty and not instantlose[0]:
        clockminutes[0] -= 1
        updateclock()
        if targetnumber[0] in numhigh:
            canvas.itemconfig(numhigh[targetnumber[0]], fill="#fd1b5b")
        lasthigh[0] = None
        if clockminutes[0] >= 0:
            return
    gameover[0] = True
    inputlocked[0] = True
    dimimg = Image.new('RGBA', (700, 819), (0, 0, 0, 140))
    dimphoto = ImageTk.PhotoImage(dimimg)
    dim = canvas.create_image(0, 0, anchor='nw', image=dimphoto)
    canvas._dimphoto = dimphoto
    boxw, boxh = 420, 220
    x0, y0 = (700-boxw)//2, (819-boxh)//2
    box = canvas.create_rectangle(x0, y0, x0+boxw, y0+boxh, fill="#201e1e", outline="#cac7c8", width=3)
    titleshdw = canvas.create_text(353, y0+73, text='GAME OVER', font=("Press Start 2P", 24), fill='#968d8d')
    title = canvas.create_text(350, y0+70, text='GAME OVER', font=("Press Start 2P", 24), fill='white')
    retryshdw = canvas.create_text(268, y0+143, text="RETRY", font=("Press Start 2P", 18), fill='#968d8d')
    retry = canvas.create_text(265, y0+140, text='RETRY', font=("Press Start 2P", 18), fill='white')
    homeshdw = canvas.create_text(438, y0+143, text="BACK", font=("Press Start 2P", 18), fill="#968d8d")
    home = canvas.create_text(435, y0+140, text='BACK', font=("Press Start 2P", 18), fill='white')
    overlayitems.extend([dim, box, title, titleshdw, retryshdw, retry, homeshdw, home])
    def restartent(e):
        canvas.itemconfig(retryshdw, fill="#1c1c1c")
        canvas.itemconfig(retry, fill="#968d8d")
    def restartlev(e):
        canvas.itemconfig(retry, fill="white")
        canvas.itemconfig(retryshdw, fill='#968d8d')
    canvas.tag_bind(retry, "<Leave>", restartlev)
    canvas.tag_bind(retry, "<Enter>", restartent)
    canvas.tag_bind(retryshdw, "<Leave>", restartlev)
    canvas.tag_bind(retry, "<Enter>", restartent)
    canvas.tag_bind(retry, "<Button-1>", restartgame)
    canvas.tag_bind(retryshdw, "<Button-1>", restartgame)
    def homeent(e):
        canvas.itemconfig(homeshdw, fill="#1c1c1c")
        canvas.itemconfig(home, fill="#968d8d")
    def homelev(e):
        canvas.itemconfig(homeshdw, fill="#968d8d")
        canvas.itemconfig(home, fill='white')
    canvas.tag_bind(home, "<Leave>", homelev)
    canvas.tag_bind(homeshdw, "<Leave>", homelev)
    canvas.tag_bind(home, "<Enter>", homeent)
    canvas.tag_bind(homeshdw, "<Enter>",homeent)
    canvas.tag_bind(home, "<Button-1>", gohome)
    canvas.tag_bind(homeshdw, "<Button-1>", gohome)
def restartgame(e=None):
    global needle_angle, needledir
    for item in overlayitems:
        canvas.delete(item)
    overlayitems.clear()
    if needleafter[0]:
        app.after_cancel(needleafter[0])
        needleafter[0] = None
    if highlightafter[0]:
        app.after_cancel(highlightafter[0])
        highlightafter[0] = None
    needle_angle = 0
    needledir = 1
    lasthigh[0] = None
    gameover[0] = False
    clockminutes[0] = startclock[0]
    updateclock()
    firstpick[0] = True
    newtarget()
    generation[0] += 1
    showcountdown(3, generation[0])
def gohome(e=None):
    global needle_angle, needledir, afterid
    for item in overlayitems:
        canvas.delete(item)
    overlayitems.clear()
    generation[0] += 1
    gameover[0] = True
    inputlocked[0] = True
    if bottomafter[0]:
        app.after_cancel(bottomafter[0])
        bottomafter[0] = None
    if afterid:
        app.after_cancel(afterid)
        afterid = None
    if needleafter[0]:
        app.after_cancel(needleafter[0])
        needleafter[0] = None
    if highlightafter[0]:
        app.after_cancel(highlightafter[0])
        highlightafter[0] = None
    clear(canvas, canvasbg)
    canvas.itemconfig(canvasbg, image='')
    numhigh.clear()
    fading.clear()
    lasthigh[0] = None
    targetnumber[0] = None
    firstpick[0] = True
    needle_angle = 0
    needledir = 1
    instantlose[0] = False
    startclock[0] = 30
    clockminutes[0] = 30
    main(straight_to_noob=True)
countdownitems = []
clocktextids = {}
def updateclock():
    total = 11*60 + clockminutes[0]
    hrs = (total // 60) % 12
    mins = total % 60
    timestr = f'{hrs}:{mins:02d}'
    if 'shdw' in clocktextids:
        canvas.itemconfig(clocktextids['shdw'], text=timestr)
        canvas.itemconfig(clocktextids['main'], text=timestr)
def showcountdown(n, gen):
    for item in countdownitems:
        canvas.delete(item)
    countdownitems.clear()
    if gen != generation[0]:
        return
    if n == 0:
        inputlocked[0] = False
        rotate_needle(gen)
        highlightnumb(gen)
        return
    inputlocked[0] = True
    dimimg = Image.new('RGBA', (700, 819), (0, 0, 0, 140))
    dimphoto = ImageTk.PhotoImage(dimimg)
    dim = canvas.create_image(0, 0, anchor='nw', image=dimphoto)
    canvas._cddimphoto = dimphoto
    boxw, boxh = 420, 220
    x0, y0 = (700-boxw)//2, (819-boxh)//2
    box = canvas.create_rectangle(x0, y0, x0+boxw, y0+boxh, fill='#201e1e', outline='#cac7c8', width=3)
    numshdw = canvas.create_text(353, y0+113, text=str(n), font=("Press Start 2P", 55), fill="#968d8d")
    num = canvas.create_text(350, y0+110, text=str(n), font=("Press Start 2P", 55), fill='white')
    countdownitems.extend([dim, box, numshdw, num])
    app.after(800, lambda: showcountdown(n-1, gen))
def rotate_needle(gen=None):
    global needle_angle
    if gen is not None and gen != generation[0]:
        return
    if gameover[0]:
        return
    needle_angle = (needle_angle + needlespeed[0] * needledir) % 210
    canvas.itemconfig(shadow, image=shadow_frames[needle_angle])
    canvas._shadow = shadow_frames[needle_angle]
    canvas.itemconfig(needle, image=needle_frames[needle_angle])
    canvas._needle = needle_frames[needle_angle]
    needleafter[0] = app.after(10, lambda: rotate_needle(generation[0]))
def flipdirection(e=None):
    global needledir
    if gameover[0] or inputlocked[0]:
        return
    needledir *= -1
    degrees = (needle_angle / 210) * 360
    number = int((degrees / 30 +3.3)% 12) or 12
    if number == targetnumber[0]:
        numberclick(number)
        newtarget()
    else:
        showgameover()
canvas.bind("<Button-1>", flipdirection)
canvas.bind("<space>", flipdirection)
lasthigh = [None]
numhigh = {}
def newtarget():
    needle_on_target[0] = False
    if targetnumber[0] is not None and targetnumber[0] in numhigh:
        canvas.itemconfig(numhigh[targetnumber[0]], fill='white')
    if firstpick[0]:
        choices = [n for n in numhigh if n != targetnumber[0] and n not in (2, 3, 4, 5)]
        firstpick[0] = False
    else:
        prev = targetnumber[0]
        choices = [n for n in numhigh if n != prev and (abs(n - prev) >= 3 or abs(n - prev) >= 9)]
    targetnumber[0] = random.choice(choices)
    canvas.itemconfig(numhigh[targetnumber[0]], fill="#fd1b5b")
def highlightnumb(gen=None):
    if gen is not None and gen != generation[0]:
        return
    if gameover[0]:
        return
    degrees = (needle_angle / 210) * 360
    number = int((degrees / 30 + 3.3) % 12) or 12
    is_on_target = (number == targetnumber[0])
    if needle_on_target[0] and not is_on_target:
        if instantlose[0]:
            showgameover(penalty=False)
            return
        clockminutes[0] -= 1
        updateclock()
        if targetnumber[0] in numhigh:
            canvas.itemconfig(numhigh[targetnumber[0]], fill="#fd1b5b")
        if clockminutes[0] < 0:
            showgameover(penalty=False)
            return
    needle_on_target[0] = is_on_target
    if lasthigh[0] != number:
        if lasthigh[0] is not None and lasthigh[0] in numhigh and lasthigh[0] not in fading:
            if lasthigh[0] == targetnumber[0]:
                canvas.itemconfig(numhigh[lasthigh[0]], fill="#fd1b5b")
            else:
                canvas.itemconfig(numhigh[lasthigh[0]], fill="white")
        if number in numhigh and number not in fading:
            if number == targetnumber[0]:
                canvas.itemconfig(numhigh[number], fill="#610822")
            else:
                canvas.itemconfig(numhigh[number], fill="#353232")
        lasthigh[0] = number
    highlightafter[0] = app.after(10, lambda: highlightnumb(generation[0]))
fading = {}
def showwin():   
    gameover[0] = True
    inputlocked[0] = True
    dimimg = Image.new("RGBA", (700, 818), (0, 0, 0, 140))
    dimphoto = ImageTk.PhotoImage(dimimg)
    dim = canvas.create_image(0, 0, anchor='nw', image=dimphoto)
    canvas._windimphoto = dimphoto
    winframes = []
    wingif = Image.open(getpath("Assets/main.gif"))
    for frame in ImageSequence.Iterator(wingif):
        frame = frame.copy().convert("RGBA")
        r, g, b, a = frame.split()
        a = a.point(lambda x: x*0.6)
        frame.putalpha(a)
        winframes.append(ImageTk.PhotoImage(frame.resize((700, 930))))
    wincanvas = Canvas(app, width=700, height=930, highlightthickness=0, bd=0, bg='black')
    wincanvas.place(x=0, y=0)
    wincanvasbg = wincanvas.create_image(0, 0, anchor='nw')
    wincanvas._winframes = winframes
    winafterid = [None]
    def animatewin(frame_index=0):
        if not wincanvas.winfo_exists():
            return
        wincanvas.itemconfig(wincanvasbg, image=winframes[frame_index] )
        winafterid[0] = app.after(35, animatewin, (frame_index+1) %len(winframes))
    animatewin()
    backshdw = wincanvas.create_text(42, 41, text="←", font=("Arial", 39), fill="#968d8d")
    back = wincanvas.create_text(40, 40, text="←", font=("Arial", 39), fill='white')
    def backent(e):
        wincanvas.itemconfig(back, fill='#968d8d')
        wincanvas.itemconfig(backshdw, fill="#1c1c1c")
    def backlev(e):
        wincanvas.itemconfig(back, fill="white")
        wincanvas.itemconfig(backshdw, fill='#968d8d')
    def goback(e=None):
        if winafterid[0]:
            app.after_cancel(winafterid[0])
        wincanvas.destroy()
        gameover[0] = False
        generation[0] += 1
        gohome()
    wincanvas.tag_bind(back, "<Enter>", backent)
    wincanvas.tag_bind(backshdw, "<Enter>", backent)
    wincanvas.tag_bind(back, "<Leave>", backlev)
    wincanvas.tag_bind(backshdw, "<Leave>", backlev)
    wincanvas.tag_bind(back, "<Button-1>", goback)
    wincanvas.tag_bind(backshdw, "<Button-1>", goback)
    wincanvas.create_text(381, 181, text='Dissapointing... \n You beat the \n easiest level. \n  Now go on \n  and try PRO!', font=("Press Start 2P", 20), fill="#968d8d", anchor='center')
    wincanvas.create_text(378, 178, text='Dissapointing... \n You beat the \n easiest level. \n  Now go on \n  and try PRO!', font=("Press Start 2P", 20), fill='white', anchor='center')
    wincanvas.create_text(353, 368, text='    You have\nearned the NOVICE\n      badge', font=("Press Start 2P", 20), fill='#968d8d', anchor='center')
    wincanvas.create_text(350, 365, text='    You have\nearned the NOVICE\n      badge', font=("Press Start 2P", 20), fill='white', anchor='center')
    noviceimg = Image.open("Assets/novice.png")
    imgnovice = ImageTk.PhotoImage(noviceimg)
    wincanvas._noviceimg = imgnovice
    wincanvas.create_image(350, 555, anchor='center', image=imgnovice)
    rounded_rect(wincanvas, 60, 320, 640, 695, r=23,color="#968d8d", width=2 )
    equipshdw = wincanvas.create_text(353, 743, text="EQUIP", font=("Press Start 2P", 22), fill="#914949")
    equip= wincanvas.create_text(350, 740, text='EQUIP', font=("Press Start 2P", 22), fill="#CB5757")
    equiped[0] = 0
    def eqbutton(e):
        if equiped[0] == 0:
            equiped[0] = 1
        else:
            equiped[0] = 0
    def eqent(e):
        if equiped[0] == 0:
            wincanvas.itemconfig(equip, fill="#2C1B1B")
            wincanvas.itemconfig(equipshdw, fill="#4c2c2c")
        elif equiped[0] == 1:
            wincanvas.itemconfig(equip, fill='#426343')
            wincanvas.itemconfig(equipshdw, fill="#132014")
    def eqlev(e):
        if equiped[0] == 0:
            wincanvas.itemconfig(equip, fill='#CB5757')
            wincanvas.itemconfig(equipshdw, fill='#914949')
        elif equiped[0] == 1:
            wincanvas.itemconfig(equip, fill="#74d172")
            wincanvas.itemconfig(equipshdw, fill="#426343")
    wincanvas.tag_bind(equip, "<Enter>",eqent )
    wincanvas.tag_bind(equipshdw, "<Enter>", eqent)
    wincanvas.tag_bind(equip, "<Leave>", eqlev)
    wincanvas.tag_bind(equipshdw, "<Leave>", eqlev)
    wincanvas.tag_bind(equip, "<Button-1>", eqbutton)
    wincanvas.tag_bind(equipshdw, "<Button-1>", eqbutton)
def numberclick(number):
    if number not in numhigh:
        return
    fading[number] = 255
    execfade(number)
    clockminutes[0] = min(clockminutes[0] + 1, 60)
    updateclock()
    lasthigh[0] = None
    needle_on_target[0] = False
    if clockminutes[0] >= 60:
        showwin()
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
bottombgframes = []
bottombg_gif = Image.open(getpath("Assets/bottomgif.gif"))
for frame in ImageSequence.Iterator(bottombg_gif):
    frame = frame.copy().convert("RGBA")
    r, g, b, a = frame.split()
    a = a.point(lambda x: x * 0.8)
    frame.putalpha(a)
    bottombgframes.append(ImageTk.PhotoImage(frame.resize((700, 230), Image.NEAREST)))
def normal(canvas, canvas_img):
    global needle, shadow
    numhigh.clear()
    fading.clear()
    clocktextids.clear()
    clear(canvas, canvas_img)
    gifbg()
    bottombg_img = canvas.create_image(0, 700, anchor='nw', image=bottombgframes[0])
    canvas._bottombg = bottombg_img
    canvas.__dict__['bottombg'] =True
    animatebottom()
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
    divideimg = Image.open(getpath("Assets/lione2.png"))
    resizeimg = divideimg.resize((770, 200), Image.Resampling.LANCZOS)
    sepimg = ImageTk.PhotoImage(resizeimg)
    clocktextids['shdw'] = canvas.create_text(353, 753, text='11:30', font=("Press Start 2P", 28), fill='#968d8d', anchor='center' )
    clocktextids['main'] = canvas.create_text(350, 750, text='11:30', font=("Press Start 2P", 28), fill='white', anchor='center')
    canvas.create_image(350, 702, anchor='center', image=sepimg)
    canvas._sepimg = sepimg
    canvas._needle = needle_frames[0]
    shadow = canvas.create_image(354, 354, anchor='center', image=shadow_frames[0])
    canvas._shadow = shadow_frames[0]
    needle = canvas.create_image(350, 350, anchor='center', image=needle_frames[0])
    canvas.lift(shadow)
    canvas.lift(needle)
def main(canvas_img_unused=None, canvasbg_unused=None, straight_to_noob=False):
    global afterid
    if afterid:
        app.after_cancel(afterid)
    frames = []
    gif = Image.open(getpath("Assets/main.gif"))
    for frame in ImageSequence.Iterator(gif):
        frame = frame.copy().convert("RGBA")
        r, g, b, a = frame.split()
        a = a.point(lambda x: x * 0.4)
        frame.putalpha(a)
        frames.append(ImageTk.PhotoImage(frame.resize((700, 819))))
    menucanvas = Canvas(app, width=700, height=819, highlightthickness=0, bd=0, bg='black')
    menucanvas.place(x=0, y=0)
    menucanvasbg = menucanvas.create_image(0, 0, anchor='nw')
    menucanvas._frames = frames
    def animate(frame_index=0):
        global afterid
        if not menucanvas.winfo_exists():
            return
        menucanvas.itemconfig(menucanvasbg, image=frames[frame_index])
        afterid = app.after(35, animate, (frame_index + 1) % len(frames))
    animate()
    def main_rounded_rect(menucanvas, x1, y1, x2, y2, r=20, color="#968d8d", width=2):
        itemz = []
        arc_kwargs = {"outline": color, "width": width}
        line_kwargs = {"fill": color, "width": width}
        itemz.append(menucanvas.create_arc(x1, y1, x1+2*r, y1+2*r, start=90, extent=90, style="arc", **arc_kwargs))
        itemz.append(menucanvas.create_arc(x2-2*r, y1, x2, y1+2*r, start=0, extent=90, style="arc", **arc_kwargs))
        itemz.append(menucanvas.create_arc(x1, y2-2*r, x1+2*r, y2, start=180, extent=90, style="arc", **arc_kwargs))
        itemz.append(menucanvas.create_arc(x2-2*r, y2-2*r, x2, y2, start=270, extent=90, style="arc", **arc_kwargs))
        itemz.append(menucanvas.create_line(x1+r, y1, x2-r, y1, **line_kwargs))
        itemz.append(menucanvas.create_line(x1+r, y2, x2-r, y2, **line_kwargs))           
        itemz.append(menucanvas.create_line(x1, y1+r, x1, y2-r, **line_kwargs))
        itemz.append(menucanvas.create_line(x2, y1+r, x2, y2-r, **line_kwargs))
        return itemz
    main_rounded_rect(menucanvas, 20, 430, 283, 490, r=23, color="#968d8d", width=2)
    main_rounded_rect(menucanvas, 425, 430, 670, 490, r=23, color="#968d8d", width=2)
    badgeshdw = menucanvas.create_text(643, 58, text='✪', fill='#968d8d', font=("Arial", 44))
    badge = menucanvas.create_text(640, 55, text="✪", fill='white', font=("Arial", 44))
    def badgescreen(e=None):
        for item in menucanvas.find_all():
            if item!= menucanvasbg:
                menucanvas.delete(item)
        menucanvas.create_text(353, 33, text="BADGES", fill='#968d8d', font=("Press Start 2P", 30))
        menucanvas.create_text(350,30, text='BADGES', fill='white', font=("Press Start 2P", 30))
        badgebckshdw = menucanvas.create_text(42, 41, text="←", font=("Arial", 39), fill="#968d8d")
        badgebck = menucanvas.create_text(39, 38, text="←", font=("Arial", 39), fill='white')
        noviceimg = Image.open("Assets/novice.png")
        imgnovice = ImageTk.PhotoImage(noviceimg)
        menucanvas._noviceimg = imgnovice
        menucanvas.create_image(150, 200, anchor='center', image=imgnovice)
        proimg = Image.open("Assets/pro.png").resize((1100, 700))
        imgpro = ImageTk.PhotoImage(proimg)
        menucanvas._proimg = imgpro
        menucanvas.create_image(240, 330, anchor='center', image=imgpro)
        hackerimg = Image.open("Assets/hacker.png")
        imghacker = ImageTk.PhotoImage(hackerimg)
        menucanvas._hackerimg = imghacker
        menucanvas.create_image(150, 560, anchor='center', image=imghacker)
        godimg = Image.open('Assets/god.png').resize((300, 200))
        imggod = ImageTk.PhotoImage(godimg)
        menucanvas._godimg = imggod
        menucanvas.create_image(520, 540, anchor='center', image=imggod)
        def bbckent(e):
            menucanvas.itemconfig(badgebck, fill='#968d8d')
            menucanvas.itemconfig(badgebckshdw, fill='#1c1c1c')
        def bbcklev(e):
            menucanvas.itemconfig(badgebckshdw, fill='#968d8d')
            menucanvas.itemconfig(badgebck, fill="white")
        def goback(e=None):
            global afterid
            if afterid:
                app.after_cancel(afterid)
                afterid = None
            menucanvas.destroy()
            main()
        menucanvas.tag_bind(badgebck, "<Enter>", bbckent)
        menucanvas.tag_bind(badgebckshdw, "<Enter>", bbckent)
        menucanvas.tag_bind(badgebckshdw, "<Leave>", bbcklev)
        menucanvas.tag_bind(badgebck, "<Leave>", bbcklev)
        menucanvas.tag_bind(badgebck, "<Button-1>", goback)
        menucanvas.tag_bind(badgebckshdw, "<Button-1>", goback)
        menucanvas.create_text(152, 352, text="NOVICE", fill='#968d8d', font=("Press Start 2P", 10))
        menucanvas.create_text(150, 350, text="NOVICE", fill='white', font=("Press Start 2P", 10))
        menucanvas.create_text(550, 352, text="PRO", fill='#968d8d', font=("Press Start 2P",10))
        menucanvas.create_text(548, 350, text="PRO", fill='white', font=("Press Start 2P", 10))
        menucanvas.create_text(152, 652, text='HACKER', fill='#968d8d', font=("Press Start 2P", 10))
        menucanvas.create_text(150, 650, text='HACKER', fill='white', font=("Press Start 2P", 10))
        menucanvas.create_text(523, 652, text='GOD', font=("Press Start 2P", 10), fill='#968d8d')
        menucanvas.create_text(521, 650, text='GOD', font=("Press Start 2P", 10), fill='white')
        equipnoviceshdw = menucanvas.create_text(153, 403, text="EQUIP", fill='#968d8d', font=("Press Start 2P", 23))
        equipnovice = menucanvas.create_text(150, 400, text='EQUIP', fill='white', font=("Press Start 2P", 23))
        equipproshdw= menucanvas.create_text(551, 403, text="EQUIP", fill='#968d8d', font=("Press Start 2P", 23))
        equippro = menucanvas.create_text(548, 400, text='EQUIP', fill='white', font=("Press Start 2P", 23))
        equiphackershdw = menucanvas.create_text(153, 703, text='EQUIP', fill="#968d8d", font=("Press Start 2P", 23))
        equiphacker = menucanvas.create_text(150, 700, text='EQUIP', fill='white', font=("Press Start 2P", 23))
        equipgodshdw = menucanvas.create_text(524, 703, text="EQUIP", font=("Press Start 2P", 23), fill='#968d8d')
        equipgod = menucanvas.create_text(521, 700, text="EQUIP", fill='white', font=("Press Start 2P", 23))
    def badgeent(e):
        menucanvas.itemconfig(badge, fill='#968d8d')
        menucanvas.itemconfig(badgeshdw, fill='#1c1c1c')
    def badgelev(e):
        menucanvas.itemconfig(badge, fill='white')
        menucanvas.itemconfig(badgeshdw, fill='#968d8d')
    menucanvas.tag_bind(badge, "<Enter>", badgeent)
    menucanvas.tag_bind(badge, "<Leave>", badgelev)
    menucanvas.tag_bind(badgeshdw, "<Enter>", badgeent)
    menucanvas.tag_bind(badgeshdw, "<Leave>", badgelev)
    menucanvas.tag_bind(badgeshdw, "<Button-1>", badgescreen)
    menucanvas.tag_bind(badge, "<Button-1>", badgescreen)
    menucanvas.create_text(353, 333, text="POP THE CLOCK", font=("Press Start 2P", 32), fill='#968d8d')
    menucanvas.create_text(350, 330, text='POP THE CLOCK', font=("Press Start 2P",32), fill='white')
    classicshdw= menucanvas.create_text(153, 463, text='CLASSIC', font=("Press Start 2P", 24), fill='#968d8d')
    classic = menucanvas.create_text(150, 460, text="CLASSIC", font=("Press Start 2P" ,24), fill='white')
    specshdw= menucanvas.create_text(553, 463, text="SPECIAL", font=("Press Start 2P", 24), fill="#968d8d")
    spec = menucanvas.create_text(550, 460, text='SPECIAL', font=("Press Start 2P", 24), fill='white')
    infoshdw = menucanvas.create_text(641, 309, text="ⓘ", font=("Arial", 15), fill='#968d8d')
    info = menucanvas.create_text(639, 308, text="ⓘ", font=("Arial", 15), fill='white')
    def infoent(e):
        menucanvas.itemconfig(info, fill="#968d8d")
        menucanvas.itemconfig(infoshdw, fill="#1c1c1c")
    def infolev(e):
        menucanvas.itemconfig(infoshdw, fill='#968d8d')
        menucanvas.itemconfig(info, fill='white')
    menucanvas.tag_bind(info, "<Leave>", infolev)
    menucanvas.tag_bind(infoshdw, "<Leave>", infolev)
    menucanvas.tag_bind(info, "<Enter>", infoent)
    menucanvas.tag_bind(infoshdw, "<Enter>", infoent)
    def specent(e):
        menucanvas.itemconfig(spec, fill='#968d8d')
        menucanvas.itemconfig(specshdw, fill='#1c1c1c')
    def speclev(e):
        menucanvas.itemconfig(spec, fill="white")
        menucanvas.itemconfig(specshdw, fill="#968d8d")
    menucanvas.tag_bind(spec, "<Leave>", speclev)
    menucanvas.tag_bind(specshdw, "<Leave>", speclev)
    menucanvas.tag_bind(specshdw, "<Enter>", specent)
    menucanvas.tag_bind(spec, "<Enter>", specent)
    def classicent(e):
        menucanvas.itemconfig(classic, fill="#968d8d")
        menucanvas.itemconfig(classicshdw, fill="#1c1c1c")
    def classiclev(e):
        menucanvas.itemconfig(classic, fill='white')
        menucanvas.itemconfig(classicshdw, fill='#968d8d')
    menucanvas.tag_bind(classic, "<Enter>", classicent)
    menucanvas.tag_bind(classicshdw, "<Enter>", classicent)
    menucanvas.tag_bind(classic, "<Leave>", classiclev)
    menucanvas.tag_bind(classicshdw, "<Leave>", classiclev)
    infoitems = []
    def showinfo(e=None):
        dimimg = Image.new("RGBA", (700, 819), (0, 0, 0, 140))
        dimphoto = ImageTk.PhotoImage(dimimg)
        dim = menucanvas.create_image(0, 0, anchor='nw', image=dimphoto)
        menucanvas._infodimphoto = dimphoto
        boxw, boxh = 420, 220
        x0, y0 = (700-boxw)//2, (819-boxh)//2
        box = menucanvas.create_rectangle(x0, y0, x0+boxw, y0+boxh, fill='#201e1e', outline="#cac7c8", width=3)
        textshdw=menucanvas.create_text(353, y0+103, text='A really tuff\ngame inspired by\nthe classic Pop\nThe Clock arcade\ngame :)', font=("Press Start 2P", 17), fill='#968d8d', anchor='center')
        text= menucanvas.create_text(350, y0+100, text='A really tuff\ngame inspired by\nthe classic Pop\nThe Clock arcade\ngame :)', font=("Press Start 2P", 17), fill='white', anchor='center')
        infoitems.extend([dim, box, textshdw, text])
        menucanvas.tag_bind(dim, "<Button-1>", closeinfo)
    def closeinfo(e=None):
        for item in infoitems:
            menucanvas.delete(item)
        infoitems.clear()
    menucanvas.tag_bind(info, "<Button-1>", showinfo)
    menucanvas.tag_bind(infoshdw, "<Button-1>", showinfo)
    def clickclassic(e=None):
        for item in menucanvas.find_all():
            if item != menucanvasbg:
                menucanvas.delete(item)
        backshdw = menucanvas.create_text(42, 41, text="←", font=("Arial", 39), fill="#968d8d")
        back = menucanvas.create_text(40, 40, text="←", font=("Arial", 39), fill='white')
        def backent(e):
            menucanvas.itemconfig(backshdw, fill="#1c1c1c")
            menucanvas.itemconfig(back, fill='#968d8d')
        def backlev(e):
            menucanvas.itemconfig(back, fill='white')
            menucanvas.itemconfig(backshdw, fill="#968d8d")
        def goback(e=None):
            global afterid
            if afterid:
                app.after_cancel(afterid)
                afterid =None
            menucanvas.destroy()
            main()
        menucanvas.tag_bind(back, "<Enter>", backent)
        menucanvas.tag_bind(backshdw, "<Enter>", backent)
        menucanvas.tag_bind(backshdw, "<Leave>", backlev)
        menucanvas.tag_bind(back, "<Leave>", backlev)
        menucanvas.tag_bind(back, "<Button-1>", goback)
        menucanvas.tag_bind(backshdw, "<Button-1>", goback)
        main_rounded_rect(menucanvas, 30, 102, 230, 157, r=23, color="#968d8d", width=2)   
        noobshdw = menucanvas.create_text(133, 133, text="NOOB", font=("Press Start 2P", 33 ), fill='#968d8d', anchor='center')
        noob = menucanvas.create_text(130, 130, text='NOOB', font=("Press Start 2P", 33), fill='white', anchor='center')
        def noobent(e):
            menucanvas.itemconfig(noobshdw, fill="#1c1c1c")
            menucanvas.itemconfig(noob, fill="#968d8d")
        def nooblev(e):
            menucanvas.itemconfig(noob, fill='white')   
            menucanvas.itemconfig(noobshdw, fill="#968d8d")
        def startgame(e=None):
            global afterid
            instantlose[0] = False
            startclock[0] = 30
            needlespeed[0] = 1
            if afterid:
                app.after_cancel(afterid)
                afterid = None
            menucanvas.destroy()
            for item in (loadingimg, loadinglabel, loadinglabelshdw, loadingcount, loadingcountshdw, loadingbottom):
                canvas.itemconfig(item, state='normal')
            loadingdone.clear()
            loadingindx[0] = 0
            if loadingafter[0]:
                app.after_cancel(loadingafter[0])
                loadingafter[0] = None
            animateloading()
            threading.Thread(target=prerender, daemon=True).start()
        menucanvas.tag_bind(noob, "<Enter>", noobent)
        menucanvas.tag_bind(noob, "<Leave>", nooblev)
        menucanvas.tag_bind(noobshdw, "<Leave>", nooblev)
        menucanvas.tag_bind(noobshdw, "<Enter>", noobent)
        menucanvas.tag_bind(noobshdw, "<Button-1>", startgame)
        menucanvas.tag_bind(noob, "<Button-1>", startgame)
        main_rounded_rect(menucanvas, 30, 177, 230, 232, r=23, color="#968d8d", width=2)
        proshdw = menucanvas.create_text(133, 208, text="PRO", font=("Press Start 2P", 33), fill='#968d8d', anchor='center')
        pro = menucanvas.create_text(130, 205, text='PRO', font=("Press Start 2P", 33), fill='white', anchor='center')
        def proent(e):
            menucanvas.itemconfig(proshdw, fill="#1c1c1c")
            menucanvas.itemconfig(pro, fill='#968d8d')
        def prolev(e):
            menucanvas.itemconfig(pro, fill='white')
            menucanvas.itemconfig(proshdw, fill="#968d8d")
        def startpro(e=None):
            global afterid
            instantlose[0] = True
            startclock[0] = 0
            needlespeed[0] = 1
            if afterid:
                app.after_cancel(afterid)
                afterid = None
            menucanvas.destroy()
            for item in (loadingimg, loadinglabel, loadinglabelshdw, loadingcount, loadingcountshdw, loadingbottom):
                canvas.itemconfig(item, state='normal')
            loadingdone.clear()
            loadingindx[0] = 0
            if loadingafter[0]:
                app.after_cancel(loadingafter[0])
                loadingafter[0] = None
            animateloading()
            threading.Thread(target=prerender, daemon=True).start()
        menucanvas.tag_bind(pro, "<Enter>", proent)
        menucanvas.tag_bind(proshdw, "<Enter>", proent)
        menucanvas.tag_bind(pro, "<Leave>", prolev)
        menucanvas.tag_bind(proshdw, "<Leave>", prolev)
        menucanvas.tag_bind(pro, "<Button-1>", startpro)
        menucanvas.tag_bind(proshdw, "<Button-1>", startpro)
        main_rounded_rect(menucanvas, 4, 252, 293, 306, r=23, color="#968d8d", width=2)
        hackershdw = menucanvas.create_text(153, 283, text="HACKER", font=("Press Start 2P", 33), fill='#968d8d', anchor='center')
        hacker = menucanvas.create_text(150,280, text='HACKER', font=("Press Start 2P", 33), fill='white', anchor='center' )
        def hackerent(e):
            menucanvas.itemconfig(hackershdw, fill="#1c1c1c")
            menucanvas.itemconfig(hacker,fill='#968d8d')
        def hackerlev(e):
            menucanvas.itemconfig(hackershdw, fill='#968d8d')
            menucanvas.itemconfig(hacker, fill='white')
        def starthacker(e=None):
            global afterid
            instantlose[0] = True
            startclock[0] = 0
            needlespeed[0] = 2 
            if afterid:
                app.after_cancel(afterid)
                afterid = None
            menucanvas.destroy()
            for item in (loadingimg, loadinglabel, loadinglabelshdw, loadingcount, loadingcountshdw, loadingbottom):
                canvas.itemconfig(item, state='normal')
            loadingdone.clear()
            loadingindx[0] = 0
            if loadingafter[0]:
                app.after_cancel(loadingafter[0])
                loadingafter[0] = None
            animateloading()
            threading.Thread(target=prerender, daemon=True).start()
        menucanvas.tag_bind(hacker, "<Leave>", hackerlev)
        menucanvas.tag_bind(hackershdw, "<Leave>", hackerlev)
        menucanvas.tag_bind(hacker, "<Enter>", hackerent)
        menucanvas.tag_bind(hackershdw, "<Enter>", hackerent)
        menucanvas.tag_bind(hacker, "<Button-1>", starthacker)
        menucanvas.tag_bind(hackershdw, "<Button-1>", starthacker)
        main_rounded_rect(menucanvas, 34, 327, 223, 381, r=23, color="#968d8d",width=2 )
        godmodeshdw = menucanvas.create_text(133, 358, text="GOD", font=("Press Start 2P", 33),fill='#968d8d', anchor='center')
        godmode = menucanvas.create_text(133, 355, text="GOD", font=("Press Start 2P", 33), fill='white', anchor='center')
        def godent(e):
            menucanvas.itemconfig(godmodeshdw, fill='#1c1c1c')
            menucanvas.itemconfig(godmode, fill='#968d8d')
        def godlev(e):
            menucanvas.itemconfig(godmode, fill="white")
            menucanvas.itemconfig(godmodeshdw, fill='#968d8d')
        def startgod(e=None):
            global afterid
            instantlose[0] = True
            startclock[0] = 0
            needlespeed[0] = 4
            if afterid:
                app.after_cancel(afterid)
                afterid = None
            menucanvas.destroy()
            for item in (loadingimg, loadinglabel, loadinglabelshdw,loadingcount, loadingcountshdw, loadingbottom ):
                canvas.itemconfig(item, state='normal')
            loadingdone.clear()
            loadingindx[0] = 0
            if loadingafter[0]:
                app.after_cancel(loadingafter[0])
                loadingafter[0] = None
            animateloading()
            threading.Thread(target=prerender, daemon=True).start()
        menucanvas.tag_bind(godmode, "<Leave>", godlev)
        menucanvas.tag_bind(godmodeshdw, "<Leave>", godlev)
        menucanvas.tag_bind(godmode, "<Enter>", godent)
        menucanvas.tag_bind(godmodeshdw, "<Enter>", godent)
        menucanvas.tag_bind(godmodeshdw, "<Button-1>", startgod)
        menucanvas.tag_bind(godmode, "<Button-1>", startgod)
    menucanvas.tag_bind(classic, "<Button-1>", clickclassic)
    menucanvas.tag_bind(classicshdw, "<Button-1>", clickclassic)
    if straight_to_noob:
        clickclassic()

main()
app.mainloop()