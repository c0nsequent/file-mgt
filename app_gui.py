import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

import clean_up_pictures as cl


class picture_window:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cleaner Folders")
        self.root.geometry("1100x500")
        self.found_pictures = list()
        self.picture_folder = Path()
        self.target_folder = Path()
        self.rooting_var = tk.BooleanVar()
        self.sort_var = tk.BooleanVar()
        self.target = False
        self.move_pictures_button = tk.Button(
            self.root, text="move images", command=self.move_pictures
        )
        self.copy_pictures_button = tk.Button(
            self.root, text="copy images", command=self.copy_pictures
        )
        self.choose_folder_button = tk.Button(
            self.root, text="choose root directory", command=self.find_pictures
        )
        self.choose_target_folder = tk.Button(
            self.root, text="choose target directory", command=self.choose_target
        )
        self.found_pictures_text = tk.Text(self.root)
        self.found_pictures_text["state"] = "disabled"
        self.rooting = tk.Checkbutton(
            self.root, text="include underlying directories?", variable=self.rooting_var
        )
        self.sort = tk.Checkbutton(
            self.root, text="Sort by date", variable=self.sort_var
        )

        self.choose_folder_button.grid(row=0, column=0)
        self.move_pictures_button.grid(row=1, column=1)
        self.copy_pictures_button.grid(row=1, column=0)
        self.choose_target_folder.grid(row=0, column=1, padx=10)
        self.found_pictures_text.grid(row=0, column=3, rowspan=3)
        self.rooting.grid(row=2, column=1)
        self.sort.grid(row=2, column=0)

        self.root.mainloop()

    def move_pictures(self):
        if not self.target:
            messagebox.showinfo("Info", "Please choose a target directory")
            return
        try:
            if messagebox.askokcancel(
                "Continue?", "Are you sure, you want to move all selected pictures?"
            ):
                cl.move_pictures(
                    self.found_pictures, self.target_folder, self.sort_var.get()
                )
        except Exception as e:
            messagebox.showerror("Error", e)
        self.sync_pictures_in_folder()

    def copy_pictures(self):
        if not self.target:
            messagebox.showinfo("Info", "Please choose a target directory")
            return
        try:
            if messagebox.askokcancel(
                "Continue?", "Are you sure, you want to move all selected pictures?"
            ):
                cl.copy_pictures(
                    self.found_pictures, self.target_folder, self.sort_var.get()
                )
        except Exception as e:
            messagebox.showerror("Error", e)
        self.sync_pictures_in_folder()

    def find_pictures(self):
        try:
            self.picture_folder = filedialog.askdirectory(mustexist=True)
            self.sync_pictures_in_folder()
        except Exception as e:
            messagebox.showerror("Error", e)

    def sync_pictures_in_folder(self):
        try:
            self.found_pictures = cl.find_pictures(
                self.picture_folder, root=self.rooting_var.get()
            )
            self.found_pictures_text["state"] = "normal"
            self.found_pictures_text.delete(1.0, tk.END)
            found_index = 0
            for pic in self.found_pictures:
                pic = Path(pic)
                self.found_pictures_text.insert(tk.END, "\n" + pic.name)
                found_index += 1
            self.found_pictures_text.insert(1.0, f"{found_index} Bilder: ")
            self.found_pictures_text["state"] = "disabled"
        except Exception as e:
            messagebox.showerror("Error", e)
            self.found_pictures_text["state"] = "disabled"

    def choose_target(self):
        try:
            self.target_folder = filedialog.askdirectory(mustexist=True)
            self.target = True
        except Exception as e:
            messagebox.showerror("Error", e)
            self.target = False
