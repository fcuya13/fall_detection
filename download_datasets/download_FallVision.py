import os
import requests
#import rarfile

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

def download_file(file_url, dest_path):
    try:
        response = session.get(file_url, stream=True)
        if response.status_code == 200:
            print(f"Downloading {dest_path}")
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            print(f"Downloaded: {dest_path}")
            return True
        else:
            print(f"Failed to download {file_url}. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading {file_url}: {e}")

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
        print(f"Extracted file: {rar_path}")
    except rarfile.BadRarFile as e:
        print(e)
        print(f"Corrupted RAR file: {rar_path}")
        return False
    except Exception as e:
        print(f"Error extracting {rar_path}: {e}")
        return False
    return True

def download_and_extract_fallvision(folders, base_url, fall_dir, no_fall_dir):
    for category, subfolders in folders.items():
        category_folder = fall_dir if category == 'Fall' else no_fall_dir

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
                    print(f"Failed to download {file_url}. Skipping this file.")
                    continue

                if not extract_rar(file_path, subfolder_path):
                    print(f"Failed to extract {file_path}. Skipping this file.")
                    continue

                os.remove(file_path)
                print(f"Deleted .rar file: {file_path}")