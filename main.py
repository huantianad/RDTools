import tkinter as tk
from pynput import keyboard


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.on = True

    def create_widgets(self):
        self.master.title("RDTools")
        self.master.iconbitmap("resources/icon.ico")

        self.canvas = tk.Canvas(self)
        self.canvas.pack()

        self.create_menus()

        self.main_text = tk.Text(self.canvas, font=("Segoe UI", 20))
        self.main_text.tag_configure("center", justify='center')
        self.main_text.insert("insert", 'Welcome to huantian\'s RDTools!\nClick the "Tools" tab to select a tool!')
        self.main_text.tag_add("center", "1.0", "end")
        self.main_text.pack(side="top")

    def create_menus(self):
        menu = tk.Menu(self)
        self.master.config(menu=menu)

        file = tk.Menu(self, tearoff=0)
        file.add_command(label="Hide", command=self.withdraw, accelerator="(Ctrl + Shift + H)")
        file.add_command(label="Exit", command=self.master.destroy)
        menu.add_cascade(label="File", menu=file)

        tools = tk.Menu(self, tearoff=0)
        tools.add_command(label="Bulk Downloader", command=self.bulk_download)
        tools.add_command(label="Auto Extract")
        tools.add_command(label="Auto Download New Levels")
        tools.add_command(label="Auto Daily Blend")
        menu.add_cascade(label="Tools", menu=tools)

    def withdraw(self):
        if self.on:
            root.withdraw()
            self.on = False
        else:
            root.deiconify()
            self.on = True

    def reset_canvas(self):
        self.canvas.destroy()
        self.canvas = tk.Canvas(self)
        self.canvas.pack()

    def bulk_download(self):
        self.reset_canvas()

        self.download_button = tk.Button(self.canvas, text="Download").pack(side="bottom")


root = tk.Tk()
root.geometry("450x300")
app = Application(master=root)

listener = keyboard.GlobalHotKeys({'<ctrl>+<shift>+h': app.withdraw})
listener.start()

app.mainloop()
