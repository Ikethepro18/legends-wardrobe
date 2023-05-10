import urllib.request
import zipfile
import os
import io
import subprocess

choice = input("What skin would you like to install?\n[1]Miclee skin [2]Universal face template ")

if choice == "1":
    url = "https://edge.forgecdn.net/files/4527/470/miclee_skin.zip"
elif choice == "2":
    url = "https://edge.forgecdn.net/files/4521/823/universal_face.zip"
else:
    print("Invalid choice")
    exit()

folder = os.path.expanduser("~\\AppData\\Roaming\\Minecraft Legends\\internalStorage\\premium_cache\\resource_packs")

with urllib.request.urlopen(url) as response:
    with zipfile.ZipFile(io.BytesIO(response.read())) as zip_ref:
        zip_ref.extractall(folder)

while True:
    new_name = input("Enter a new name for the folder (cannot include spaces): ")
    if " " not in new_name:
        break
    else:
        print("Invalid name. Please try again.")

old_path = os.path.join(folder, os.listdir(folder)[0])
new_path = os.path.join(folder, new_name)
os.rename(old_path, new_path)

subprocess.Popen(f'explorer "{new_path}"')

print("File downloaded and extracted to:")
print(folder)
