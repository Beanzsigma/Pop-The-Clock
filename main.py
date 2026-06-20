import customtkinter as ctk
from PIL import Image, ImageSequence, ImageTk
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
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

app.mainloop()
