import requests
import zipfile
import os

url = "https://futn0rzrll.ufs.sh/f/j4V6zoXeTEG9XX9KCOYGlUt1cM0JgDbzOAwKHa65dvioRsxQ"

zip_filename = "GMDCSA24.zip"
base_dir = "data"
urfd_dir = "GMDCSA24"
full_base_dir = os.path.join(base_dir, urfd_dir)
os.makedirs(full_base_dir, exist_ok=True)

print(f"Downloading dataset...")
response = requests.get(url)

if response.status_code == 200:
    with open(zip_filename, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {url} successfully.")

    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(os.path.join(full_base_dir))
    print(f"Renamed extracted folder to GMDCSA24'.")

    os.remove(zip_filename)
    print(f"Deleted zip file: {zip_filename}")
else:
    print(f"Error al descargar el archivo. Código de estado: {response.status_code}")
