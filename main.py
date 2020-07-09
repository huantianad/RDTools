import tkinter as tk
from tkinter import filedialog

from pynput import keyboard

from tools import bulk_downloader


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.font = ("Segoe UI", 20)
        self.create_widgets()
        self.on = True

    def create_widgets(self):
        self.master.title("RDTools")
        self.master.iconbitmap("resources/icon.ico")

        self.canvas = tk.Canvas(self)
        self.canvas.pack()

        self.create_menus()

        self.main_text = tk.Text(self.canvas, font=self.font)
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

        others = tk.Menu(self, tearoff=0)
        others.add_command(label="Samurai.", command=self.samurai)
        menu.add_cascade(label="Others", menu=others)

    def withdraw(self):
        if self.on:
            root.withdraw()
            self.on = False
        else:
            root.deiconify()
            self.on = True

    def reset_canvas(self):
        # Funciton to reset canvas
        self.canvas.destroy()
        self.canvas = tk.Canvas(self)
        self.canvas.pack()

    def samurai(self):
        self.reset_canvas()

        text = tk.Label(self.canvas, text="Samurai.").pack()

    def bulk_download(self):
        # Resets canvas
        self.reset_canvas()

        # Get initial list of levels and displays amount
        self.levels_list = bulk_downloader.get_initial()
        self.amount_display = tk.Label(self.canvas, text=f"Total amount of levels: {len(self.levels_list)}").pack(
            anchor="n")

        self.bulk_option_frame = tk.Frame(self.canvas)
        self.bulk_option_frame.pack()

        # Setup positional/difference selection
        self.mode = tk.IntVar(root)
        self.mode_positional = tk.Radiobutton(self.bulk_option_frame, text="Positional", variable=self.mode, value=0,
                                              command=self.bulk_positional).grid(row=1, column=0, sticky="W")
        self.mode_difference = tk.Radiobutton(self.bulk_option_frame, text="Difference", variable=self.mode, value=1,
                                              command=self.bulk_difference).grid(row=2, column=0, sticky="W")

        self.file_mode = tk.IntVar(root)
        self.mode_rename = tk.Radiobutton(self.bulk_option_frame, text="Rename", variable=self.file_mode, value=0).grid(
            row=1, column=1, sticky="W")
        self.mode_overwrite = tk.Radiobutton(self.bulk_option_frame, text="Overwrite", variable=self.file_mode,
                                             value=1).grid(row=2, column=1, sticky="W")
        self.mode_skip = tk.Radiobutton(self.bulk_option_frame, text="Skip", variable=self.file_mode, value=2).grid(
            row=3, column=1, sticky="W")

        # Create frame for downloading content.
        self.bulk_frame = tk.Frame(self.canvas)
        self.bulk_frame.pack()

        self.bulk_positional()

    def bulk_positional(self):
        # Reset frame
        self.bulk_frame.destroy()
        self.bulk_frame = tk.Frame(self.canvas)
        self.bulk_frame.pack()

        # Create inputs for level selection.
        self.start_label = tk.Label(self.bulk_frame, text="Start:").grid(row=1)
        self.start_select = tk.Spinbox(self.bulk_frame, from_=1, to=len(self.levels_list), width=10)
        self.start_select.grid(column=2, row=1)

        self.start_label = tk.Label(self.bulk_frame, text="End:").grid(row=2)
        self.end_select = tk.Spinbox(self.bulk_frame, from_=1, to=len(self.levels_list), width=10)
        self.end_select.grid(column=2, row=2)

        self.start_label = tk.Label(self.bulk_frame, text="Threads:").grid(row=3)
        self.thread_select = tk.Spinbox(self.bulk_frame, from_=1, to=64, width=10)
        self.thread_select.grid(column=2, row=3)
        self.thread_select.delete(0, "end")
        self.thread_select.insert(0, 8)

        # Create download button
        self.download_button = tk.Button(self.bulk_frame,
                                         text="Download",
                                         command=lambda: bulk_downloader.download_all(self.levels_list,
                                                                                      int(self.start_select.get()),
                                                                                      int(self.end_select.get()),
                                                                                      int(self.thread_select.get()),
                                                                                      int(self.file_mode.get())))
        self.download_button.grid(columnspan=3)

    def positional_file_save(self):
        # Function to save the name of the selected file.
        self.positional_file_name = filedialog.askopenfilename(initialdir="/",
                                                               title="Select file",
                                                               filetypes=(("Text files", "*.txt"),))

    def bulk_difference(self):
        self.bulk_frame.destroy()
        self.bulk_frame = tk.Frame(self.canvas)
        self.bulk_frame.pack()

        self.start_label = tk.Label(self.bulk_frame, text="Threads:").grid(row=1)
        self.thread_select = tk.Spinbox(self.bulk_frame, from_=1, to=64, width=10)
        self.thread_select.grid(column=2, row=1)
        self.thread_select.delete(0, "end")
        self.thread_select.insert(0, 8)

        self.select_file = tk.Button(self.bulk_frame, text="Select File", command=self.positional_file_save)
        self.select_file.grid(columnspan=3, row=2)

        self.download_button = tk.Button(self.bulk_frame,
                                         text="Download",
                                         command=lambda: bulk_downloader.positional_download(self.levels_list,
                                                                                             self.positional_file_name,
                                                                                             int(self.thread_select.get())))
        self.download_button.grid(columnspan=3)


root = tk.Tk()
root.geometry("450x300")
app = Application(master=root)

listener = keyboard.GlobalHotKeys({'<ctrl>+<shift>+h': app.withdraw})
listener.start()

app.mainloop()
