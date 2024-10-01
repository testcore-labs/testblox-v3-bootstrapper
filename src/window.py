import customtkinter
import PIL.Image
from tkinter import *
# so its accesible from window.*
ctk = customtkinter
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("./assets/themes/purple.json")

w = ctk.CTk()
w.minsize(400, 250)
w.maxsize(400, 250)
w.wm_attributes('-type', 'splash')

def button_function():
  w.withdraw()
  time.sleep(1)
  w.deiconify()

resize_img_by = 3
logo_img = ctk.CTkImage(PIL.Image.open("./assets/img/logo.png"),
	size=(987 / resize_img_by, 195 / resize_img_by))

logo_label = ctk.CTkLabel(w, text="", image=logo_img)
logo_label.pack(pady=10)
logo_label.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

#button = ctk.CTkButton(master=w, text="CTkButton", command=button_function)
#button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

label = ctk.CTkLabel(w, text="launching client...", fg_color="transparent")
label.place(relx=0.5, rely=0.68, anchor=ctk.CENTER)

progressbar = ctk.CTkProgressBar(w, orientation="horizontal")
progressbar.configure(mode="indeterminate")
progressbar.place(relx=0.5, rely=0.75, anchor=ctk.CENTER)
progressbar.configure(width=200)
progressbar.configure(indeterminate_speed=0.6)
progressbar.start()