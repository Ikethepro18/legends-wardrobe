import sys
import os
import urllib.request
import zipfile
import io
import shutil
import tkinter as tk
import pathlib
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
import json

def get_resource_path(relative_path):
    """Get the absolute path to a resource, accounting for PyInstaller one-file mode"""
    if hasattr(sys, "_MEIPASS"):
        base_path = pathlib.Path(sys._MEIPASS)
    else:
        base_path = pathlib.Path(__file__).resolve().parent

    return str(base_path / relative_path)

def install_hero():
    urls = [
        "https://edge.forgecdn.net/files/4527/470/miclee_skin.zip",
        "https://github.com/LegendsModding/Jeb-Hero/files/11467695/jeb_ml_01.zip"
    ]
    choice = choice_var.get()
    if choice not in [1, 2]:
        return messagebox.showerror("Error", "Invalid choice")
    folder = os.path.join(
        os.getenv("APPDATA"), "Legend's Wardrobe"
    )
    with urllib.request.urlopen(urls[choice - 1]) as response, zipfile.ZipFile(io.BytesIO(response.read())) as zip_ref:
        zip_ref.extractall(folder)
    if not rename_folder(folder):
        return

def rename_folder(folder_path):
    old_path = os.path.join(folder_path, os.listdir(folder_path)[0])
    while True:
        new_name = simpledialog.askstring("Rename Mod Folder", "Enter a new name for the folder (cannot include spaces): ")
        if not new_name:
            shutil.rmtree(old_path)
            return
        new_path = os.path.join(
            os.getenv("APPDATA"), "Minecraft Legends", "internalStorage", "premium_cache", "resource_packs", new_name
        )
        if os.path.exists(new_path):
            choice = messagebox.askyesnocancel(
                "Error", f"Folder '{new_name}' already exists. Do you want to overwrite it?"
            )
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

def browse_file():
    file_path = filedialog.askopenfilename(
        initialdir="", title="Select Zip File", filetypes=[("Zip Files", "*.zip")]
    )
    if file_path:
        folder = os.path.join(
            os.getenv("APPDATA"), "Legend's Wardrobe"
        )
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(folder)
        if not rename_folder(folder):
            return

def get_pack_name(folder_path):
    lang = "en_US"
    texts_folder = os.path.join(folder_path, "texts")
    lang_file_path = os.path.join(texts_folder, f"{lang}.lang")

    if os.path.exists(lang_file_path):
        with open(lang_file_path, "r", encoding="utf-8") as lang_file:
            for line in lang_file:
                if line.startswith("pack.name="):
                    return line[len("pack.name="):].strip()

    return None

def scan_installed_heroes():
    installed_heroes_list.delete(0, tk.END)
    folder = os.path.join(
        os.getenv("APPDATA"), "Minecraft Legends", "internalStorage", "premium_cache", "resource_packs"
    )
    manifest_folders = []
    for root_dir, dirs, files in os.walk(folder):
        if "manifest.json" in files:
            dlc_metadata_path = os.path.join(root_dir, "dlc_data", "dlc_metadata.json")
            if os.path.exists(dlc_metadata_path):
                with open(dlc_metadata_path, encoding="utf-8") as dlc_metadata_file:
                    try:
                        dlc_metadata = json.load(dlc_metadata_file)
                        if "type" in dlc_metadata:
                            dlc_type = dlc_metadata["type"]
                            if dlc_type not in ["myth", "lost_legend"]:
                                pack_name = get_pack_name(root_dir)
                                if pack_name:
                                    manifest_folders.append(pack_name)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        print(f"Error decoding JSON file or non-ASCII characters found: {dlc_metadata_path}")

    for folder_name in manifest_folders:
        installed_heroes_list.insert(tk.END, folder_name)

def refresh_installed_heroes():
    scan_installed_heroes()

root = tk.Tk()
root.geometry("400x200")
root.title("Legend's Wardrobe")
root.iconbitmap(default=get_resource_path("icon.ico"))

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

standard_tab = ttk.Frame(notebook, width=400, height=180)
tk.Label(standard_tab, text="What hero would you like to install?").pack(anchor=tk.W)
choice_var = tk.IntVar(value=1)
tk.Radiobutton(standard_tab, text="Miclee skin", variable=choice_var, value=1).pack(anchor=tk.W)
tk.Radiobutton(standard_tab, text="Jeb_ skin", variable=choice_var, value=2).pack(anchor=tk.W)
tk.Button(standard_tab, text="Install Hero", command=install_hero).pack(anchor=tk.W)

browse_tab = ttk.Frame(notebook, width=400, height=180)
tk.Label(browse_tab, text="Select a ZIP file to install:").pack()
tk.Button(browse_tab, text="Browse", command=browse_file).pack()

installed_heroes_tab = ttk.Frame(notebook, width=400, height=180)
installed_heroes_list = tk.Listbox(installed_heroes_tab)
installed_heroes_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
refresh_frame = tk.Frame(installed_heroes_tab)
refresh_frame.pack(side=tk.TOP, fill=tk.X)
refresh_button = tk.Button(refresh_frame, text="Refresh", command=refresh_installed_heroes)
refresh_button.pack(side=tk.BOTTOM, padx=10, pady=5)

notebook.add(standard_tab, text="Standard")
notebook.add(browse_tab, text="Browse")
notebook.add(installed_heroes_tab, text="Installed Heroes")

scan_installed_heroes()

root.mainloop()
