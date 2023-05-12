import sys
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import urllib.request, zipfile, os, io, subprocess
import shutil
import pathlib

def get_resource_path(relative_path):
    """Get the absolute path to a resource, accounting for PyInstaller one-file mode"""
    if hasattr(sys, "_MEIPASS"):
        base_path = pathlib.Path(sys._MEIPASS)
    else:
        base_path = pathlib.Path(__file__).resolve().parent

    return str(base_path / relative_path)

def install_hero():
    urls = ["https://edge.forgecdn.net/files/4527/470/miclee_skin.zip", "https://edge.forgecdn.net/files/4521/823/universal_face.zip"]
    choice = choice_var.get()
    if choice not in [1, 2]: return messagebox.showerror("Error", "Invalid choice")
    folder = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Minecraft Legends", "internalStorage", "premium_cache", "resource_packs")
    with urllib.request.urlopen(urls[choice - 1]) as response, zipfile.ZipFile(io.BytesIO(response.read())) as zip_ref: zip_ref.extractall(folder)
    if not rename_folder(folder): return

def rename_folder(folder_path):
    old_path = os.path.join(folder_path, os.listdir(folder_path)[0])
    while True:
        new_name = simpledialog.askstring("Rename Mod Folder", "Enter a new name for the folder (cannot include spaces): ")
        if not new_name:
            shutil.rmtree(old_path)
            return
        new_path = os.path.join(folder_path, new_name)
        if os.path.exists(new_path):
            choice = messagebox.askyesnocancel("Error", f"Folder '{new_name}' already exists. Do you want to overwrite it?")
            if choice is None:
                shutil.rmtree(old_path)
                return
            elif not choice:
                continue
            else:
                try:
                    shutil.rmtree(new_path)
                    break
                except OSError as e:
                    messagebox.showerror("Error", f"Failed to delete folder: {str(e)}")
                    shutil.rmtree(old_path)
                    return
        elif " " in new_name:
            messagebox.showerror("Error", "Invalid name. Please try again.")
            continue
        else:
            break
    try:
        os.rename(old_path, new_path)
        if messagebox.askyesno("Success", "Folder renamed successfully. Open the folder now?"):
            os.startfile(new_path)
    except OSError as e:
        messagebox.showerror("Error", f"Failed to rename folder: {str(e)}")
        shutil.rmtree(old_path)
        return

root = tk.Tk()
root.geometry("400x200")
root.title("Legend's Wardrobe")
root.iconbitmap(default=get_resource_path("icon.ico"))

tk.Label(root, text="What hero would you like to install?").pack(anchor=tk.W)
choice_var = tk.IntVar(value=1)
tk.Radiobutton(root, text="Miclee skin", variable=choice_var, value=1).pack(anchor=tk.W)
tk.Radiobutton(root, text="Universal face template", variable=choice_var, value=2).pack(anchor=tk.W)
tk.Button(root, text="Install Hero", command=install_hero).pack(anchor=tk.W)

root.mainloop()
