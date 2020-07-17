import os
import sys
import tkinter as tk
from tkinter import filedialog

from pynput import keyboard

from tools import bulk_downloader


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        # Required variables
        self.font = ("Segoe UI", 20)
        self.on = True

        self.create_widgets()

        # Setup variable for storing download directory
        self.download_dir_name = tk.StringVar()
        self.download_dir_name.set(os.path.join('C:\\', 'Users', os.getlogin(), 'Documents', 'Rhythm Doctor', 'Levels'))

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def create_widgets(self):
        """Base Widget Creator"""
        # Window title and icon
        self.master.title("RDTools")
        self.master.iconbitmap(self.resource_path("resources/icon.ico"))

        # Create base canvas
        self.canvas = tk.Canvas(self)
        self.canvas.pack()

        self.create_menus()

        # Create main menu text
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
        tools.add_command(label="Auto Extract", command=self.not_exist)
        tools.add_command(label="Auto Download New Levels", command=self.not_exist)
        tools.add_command(label="Auto Daily Blend", command=self.not_exist)
        menu.add_cascade(label="Tools", menu=tools)

        others = tk.Menu(self, tearoff=0)
        others.add_command(label="Samurai.", command=self.samurai)
        menu.add_cascade(label="Others", menu=others)

    def withdraw(self):
        """Function to help with hiding window"""
        if self.on:
            root.withdraw()
            self.on = False
        else:
            root.deiconify()
            self.on = True

    def reset_canvas(self):
        """Function to reset canvas"""
        self.canvas.destroy()
        self.canvas = tk.Canvas(self)
        self.canvas.pack()

    def samurai(self):
        """Samurai menu item"""
        self.reset_canvas()

        text = tk.Label(self.canvas, text="Samurai.").pack()

    def not_exist(self):
        """Menu when funciton not implemented"""
        self.reset_canvas()

        self.main_text = tk.Text(self.canvas, font=self.font)
        self.main_text.tag_configure("center", justify='center')
        self.main_text.insert("insert", 'Samurai says:\n Hmmm... This function seems to not be implemented yet.')
        self.main_text.tag_add("center", "1.0", "end")
        self.main_text.pack()

    def bulk_download(self):
        """Main code for bulk downloader"""
        self.reset_canvas()

        # Get initial list of levels and displays amount
        self.levels_list = bulk_downloader.get_initial()
        self.amount_display = tk.Label(self.canvas, text=f"Total amount of levels: {len(self.levels_list)}").pack(
            anchor="n")

        # Create options frame for downloader
        self.bulk_option_frame = tk.Frame(self.canvas)
        self.bulk_option_frame.pack()

        # Positional/difference selection
        self.mode = tk.IntVar(root)
        self.mode_positional = tk.Radiobutton(self.bulk_option_frame, text="Positional", variable=self.mode, value=0,
                                              command=self.bulk_positional).grid(row=1, column=0, sticky="W")
        self.mode_difference = tk.Radiobutton(self.bulk_option_frame, text="Difference", variable=self.mode, value=1,
                                              command=self.bulk_difference).grid(row=2, column=0, sticky="W")

        # Same name selection
        self.file_mode = tk.IntVar(root)
        self.mode_rename = tk.Radiobutton(self.bulk_option_frame, text="Rename", variable=self.file_mode, value=0).grid(
            row=1, column=1, sticky="W")
        self.mode_overwrite = tk.Radiobutton(self.bulk_option_frame, text="Overwrite", variable=self.file_mode,
                                             value=1).grid(row=2, column=1, sticky="W")
        self.mode_skip = tk.Radiobutton(self.bulk_option_frame, text="Skip", variable=self.file_mode, value=2).grid(
            row=3, column=1, sticky="W")

        # Create main frame for downloading content.
        self.bulk_frame = tk.Frame(self.canvas)
        self.bulk_frame.pack()

        self.bulk_positional()

    def select_download_dir(self):
        """Prompts for directory to download file to."""
        self.download_dir_name.set(filedialog.askdirectory(initialdir="/",
                                                    title="Select download directory"))

    def bulk_positional(self):
        # Reset frame
        self.bulk_frame.destroy()
        self.bulk_frame = tk.Frame(self.canvas)
        self.bulk_frame.pack()

        # Create inputs for level selection.
        self.start_label = tk.Label(self.bulk_frame, text="Start:").grid(row=1, sticky="e")
        self.start_select = tk.Spinbox(self.bulk_frame, from_=1, to=len(self.levels_list), width=10)
        self.start_select.grid(column=1, row=1, sticky="w")

        self.start_label = tk.Label(self.bulk_frame, text="End:").grid(row=2, sticky="e")
        self.end_select = tk.Spinbox(self.bulk_frame, from_=1, to=len(self.levels_list), width=10)
        self.end_select.grid(column=1, row=2, sticky="w")

        self.start_label = tk.Label(self.bulk_frame, text="Threads:").grid(row=3, sticky="e")
        self.thread_select = tk.Spinbox(self.bulk_frame, from_=1, to=64, width=10)
        self.thread_select.grid(column=1, row=3, sticky="w")
        self.thread_select.delete(0, "end")
        self.thread_select.insert(0, 8)

        self.download_dir = tk.Button(self.bulk_frame, text="Download Dir", command=self.select_download_dir).grid(
            columnspan=2)
        self.download_label = tk.Label(self.bulk_frame, textvariable=self.download_dir_name).grid(columnspan=2)

        # Create download button
        self.download_button = tk.Button(self.bulk_frame,
                                         text="Download",
                                         command=lambda: bulk_downloader.download_all(self.levels_list,
                                                                                      int(self.start_select.get()),
                                                                                      int(self.end_select.get()),
                                                                                      int(self.thread_select.get()),
                                                                                      int(self.file_mode.get()),
                                                                                      self.download_dir_name.get()))
        self.download_button.grid(columnspan=2)

    def positional_file_save(self):
        """Prompts and saves positional file."""
        self.positional_file_name = filedialog.askopenfilename(initialdir="/",
                                                               title="Select file",
                                                               filetypes=(("Text files", "*.txt"),))

    def bulk_difference(self):
        self.bulk_frame.destroy()
        self.bulk_frame = tk.Frame(self.canvas)
        self.bulk_frame.pack()

        self.start_label = tk.Label(self.bulk_frame, text="Threads:").grid(row=1, sticky="e")
        self.thread_select = tk.Spinbox(self.bulk_frame, from_=1, to=64, width=10)
        self.thread_select.grid(column=1, row=1, sticky="w")
        self.thread_select.delete(0, "end")
        self.thread_select.insert(0, 8)

        self.select_file = tk.Button(self.bulk_frame, text="Select File", command=self.positional_file_save)
        self.select_file.grid(columnspan=2, row=2)

        self.download_dir = tk.Button(self.bulk_frame, text="Download Dir", command=self.select_download_dir).grid(
            columnspan=2)
        self.download_label = tk.Label(self.bulk_frame, textvariable=self.download_dir_name).grid(columnspan=2)

        self.download_button = tk.Button(self.bulk_frame,
                                         text="Download",
                                         command=lambda: bulk_downloader.positional_download(self.levels_list,
                                                                                             self.positional_file_name,
                                                                                             int(self.thread_select.get()),
                                                                                             self.download_dir_name.get()))
        self.download_button.grid(columnspan=3)


# Setup base tkinter app and create my app
root = tk.Tk()
root.geometry("450x300")
app = Application(master=root)

listener = keyboard.GlobalHotKeys({'<ctrl>+<shift>+h': app.withdraw})
listener.start()

app.mainloop()
