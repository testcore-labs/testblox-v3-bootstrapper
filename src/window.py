import executable
import config
import env

from pynput import keyboard
import customtkinter
import pyglet, os
import PIL.Image
import threading
import time
import sys

# so its accesible from window.*
ctk = customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme(os.path.join(executable.assets, "themes", "purple.json"))

class page_MAIN(customtkinter.CTkFrame):
  def __init__(self, master, **kwargs):
    super().__init__(master, **kwargs)
    
    # modify this according to your image
    # i could do this better but you fiddle with it not me :)
    resize_img_by = 3
    IMG_LOGO = PIL.Image.open(os.path.join(executable.assets, "img", "logo.png"))
    LOGO_WIDTH, LOGO_HEIGHT = IMG_LOGO.size 
    self.logo_img = ctk.CTkImage(IMG_LOGO, size=(LOGO_WIDTH / resize_img_by, LOGO_HEIGHT / resize_img_by))

    self.logo_label = ctk.CTkLabel(self, text="", image=self.logo_img)
    self.logo_label.pack(pady=10)
    self.logo_label.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

    #button = ctk.CTkButton(master=self, text="CTkButton", command=button_function)
    #button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    self.progress_text = ctk.CTkLabel(self, text="initializing...", fg_color="transparent")
    self.progress_text.place(relx=0.5, rely=0.75, anchor=ctk.CENTER)

    self.progressbar = ctk.CTkProgressBar(self, orientation="horizontal")
    self.progressbar.configure(mode="indeterminate")
    self.progressbar.place(relx=0.5, rely=1, anchor=ctk.N, y=0, in_=self.progress_text)
    self.progressbar.configure(width=200)
    self.progressbar.configure(indeterminate_speed=0.6)
    self.progressbar.start()

    self.version_text = ctk.CTkLabel(self, 
      padx=7, 
      text_color="#8a8a8a",
      font=ctk.CTkFont(size=9), 
      text=f"{env.app.version}", 
      fg_color="transparent",
    )
    self.version_text.place(rely=1.0, relx=1.0, x=0, y=0, anchor=ctk.SE)

class app(ctk.CTk):
  #Collect my pages..
  pages = {
    "main": None
  }

  def __init__(self):
    super().__init__()
    self.title("bootstrapper")
    self.resizable(False, False)
    self.minsize(400, 250)
    self.maxsize(400, 250)
    self.wm_attributes('-type', 'splash')
    self.wm_attributes('-topmost', False)

    self.settings = ctk.CTkToplevel(self)
    self.settings.title("settings")
    self.settings.resizable(False, False)
    self.settings.minsize(450, 250)
    self.settings.maxsize(450, 250)
    self.settings.wm_attributes('-topmost', True)
    if not config.bootstrapper.get("first_time"):
      self.settings.withdraw() # hide it
    else:
      config.bootstrapper.set(["first_time"], False)
      self.settings.withdraw()
      self.settings.iconify() 
      self.settings.focus()

    rpc_switch_var = ctk.StringVar(
      value=config.bootstrapper.get("discord", "rpc", "enabled")
    )
    def rpc_switch_fn():
      value = True if rpc_switch_var.get() else False
      config.bootstrapper.set(["discord", "rpc", "enabled"], value)

    rpc_switch = ctk.CTkSwitch(self.settings, 
      text="enable RPC", 
      command=rpc_switch_fn,
      variable=rpc_switch_var, 
      onvalue=True, 
      offvalue=False
    )

    rpc_switch.place(rely=0.15, relx=0.185, anchor=ctk.CENTER)

    self.info_restart = ctk.CTkLabel(self.settings,
      text_color="#8a8a8a",
      font=ctk.CTkFont(size=10),  
      padx=7, 
      text="changes will only show next start", 
      fg_color="transparent"
    )
    self.info_restart.place(rely=1.0, relx=0, x=0, y=0, anchor=ctk.SW)
    self.info_f8 = ctk.CTkLabel(self.settings,
      text_color="#8a8a8a",
      font=ctk.CTkFont(size=10),  
      padx=7, 
      text="you can close me with F8", 
      fg_color="transparent"
    )
    self.info_f8.place(rely=1.0, relx=1.0, x=0, y=0, anchor=ctk.SE)

    def settings_key_press(key):
      if key == keyboard.Key.f8:
        if self.settings.state() != "normal":
          self.settings.iconify() 
          self.settings.focus()
        else:
          self.settings.withdraw()

    keyboard.Listener(on_release=settings_key_press).start()

    self.grid_rowconfigure(0, weight=1)
    self.grid_columnconfigure(0, weight=1)
    self.pages["main"] = page_MAIN(master=self)
    self.show_main_page()


  def show_main_page(self):
    #closewith#self.pages["main"].grid_forget()
    self.pages["main"].grid(row=0, column=0, padx=3, pady=3, sticky="nsew")

  # wow so amazing python!
  # acceptable since we do wanna wait for the ui lol
  def page(self, page):
    hang_time = 0
    while self.pages[page] is None and hang_time < 5:
      time.sleep(0.1)
      hang_time = hang_time + 0.1 
    if hang_time >= 5:
      raise TimeoutError("timed out")
    return self.pages[page]

a = None
def window():
  global a
  a = app()
  a.mainloop()

# biggest hack of my LIFE
running = threading.Thread(
  target=window,
  daemon=True
)
running.start()

# we are waiting for the app from the thread
# we cant make a new class from a different thread
# because tkinter said so..
#
# :(
while a is None:
  time.sleep(0.1)