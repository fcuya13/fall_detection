# pip install rarfile
# Add WinRAR to path

import os
import requests
import rarfile
import time

folders = {
    'Fall': {
        'bed': [8138607, 8138612, 8138614, 8138617],
        'chair': [8138622, 8138623, 8138624],
        'stand': [8138935, 8138937, 8138941]
    },
    'ADL': {
        'bed': [8140287, 8140288, 8140291, 8140295],
        'chair': [8140307, 8140309, 8140310],
        'stand': [8140315, 8140316, 8140317]
    }
}

base_dir = "data"
fallvision_dir = "FallVision"
full_base_dir = os.path.join(base_dir, fallvision_dir)

fall_dir = os.path.join(full_base_dir, "Fall")
no_fall_dir = os.path.join(full_base_dir, "ADL")

os.makedirs(fall_dir, exist_ok=True)
os.makedirs(no_fall_dir, exist_ok=True)

base_url = "https://dataverse.harvard.edu/api/access/datafile/"

def download_file(file_url, dest_path, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(file_url, stream=True)
            if response.status_code == 200:
                with open(dest_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Descargado: {dest_path}")
                return True
            else:
                print(f"Error al descargar {file_url}: Código de estado {response.status_code}")
                return False
        except Exception as e:
            print(f"Error al descargar {file_url}: {e}")
            attempt += 1
            time.sleep(5)
    return False

def extract_rar(rar_path, dest_folder):
    try:
        with rarfile.RarFile(rar_path) as rf:
            for file in rf.namelist():
                rf.extract(file, dest_folder)
                extracted_file_path = os.path.join(dest_folder, file)
                if os.path.isdir(extracted_file_path):
                    for inner_file in os.listdir(extracted_file_path):
                        os.rename(os.path.join(extracted_file_path, inner_file), os.path.join(dest_folder, inner_file))
                    os.rmdir(extracted_file_path)
        print(f"Archivo descomprimido: {rar_path}")
    except rarfile.BadRarFile as e:
        print(e)
        print(f"Error de archivo RAR dañado: {rar_path}")
        return False
    except Exception as e:
        print(f"Error al descomprimir {rar_path}: {e}")
        return False
    return True

def process_files():
    for category, subfolders in folders.items():
        if category == 'Fall':
            category_folder = fall_dir
        elif category == 'ADL':
            category_folder = no_fall_dir
        else:
            continue

        os.makedirs(category_folder, exist_ok=True)

        for subfolder, file_ids in subfolders.items():
            for idx, file_id in enumerate(file_ids):
                subfolder_name = f"{subfolder}_{idx + 1}"
                subfolder_path = os.path.join(category_folder, subfolder_name)
                os.makedirs(subfolder_path, exist_ok=True)

                file_url = f"{base_url}{file_id}"
                file_name = f"{file_id}.rar"
                file_path = os.path.join(category_folder, file_name)

                if not download_file(file_url, file_path):
                    print(f"No se pudo descargar {file_url}. Saltando este archivo.")
                    continue

                if not extract_rar(file_path, subfolder_path):
                    print(f"No se pudo descomprimir {file_path}. Saltando este archivo.")
                    continue

                os.remove(file_path)
                print(f"Archivo .rar eliminado: {file_path}")

if __name__ == "__main__":
    process_files()
