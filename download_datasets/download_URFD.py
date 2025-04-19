import os
import requests
from zipfile import ZipFile
import shutil

def download_file(url, save_path):
    print(f"Downloading: {url}")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {url} successfully.")
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")

def unzip_file(zip_path, extract_to):
    try:
        with ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Extracted {zip_path} to {extract_to}")

        extracted_folder = os.path.join(extract_to, zip_ref.namelist()[0].split(os.path.sep)[0])
        camera_folder = os.path.join(extract_to, "Camera")
        os.rename(extracted_folder, camera_folder)
        print(f"Renamed extracted folder to 'Camera'.")

    except Exception as e:
        print(f"Error extracting {zip_path}: {e}")

def organize_files(zip_path, destination_dir, folder_name):
    video_dir = os.path.join(destination_dir, folder_name)
    os.makedirs(video_dir, exist_ok=True)
    unzip_file(zip_path, video_dir)

    os.remove(zip_path)
    print(f"Deleted zip file: {zip_path}")

def move_csv_data(csv_file, destination_dir, folder_name):
    csv_dest = os.path.join(destination_dir, folder_name, csv_file.split(os.path.sep)[-1])
    shutil.move(csv_file, csv_dest)
    print(f"Moved accelerometer data {csv_file} to {destination_dir}/{folder_name}")

def download_and_extract_urfd(fall_urls, adl_urls, fall_accel_urls, adl_accel_urls, fall_sync_urls, adl_sync_urls, base_dir, fall_dir, no_fall_dir):
    for i, url in enumerate(fall_urls):
        filename = url.split('/')[-1]
        file_path = os.path.join(base_dir, filename)
        print(file_path)

        download_file(url, file_path)

        folder_name = f"Fall{str(i + 1).zfill(2)}"
        organize_files(file_path, fall_dir, folder_name)

        accel_url = fall_accel_urls[i]
        accel_filename = accel_url.split('/')[-1]
        accel_file_path = os.path.join(base_dir, accel_filename)
        download_file(accel_url, accel_file_path)
        move_csv_data(accel_file_path, fall_dir, folder_name)

        sync_url = fall_sync_urls[i]
        sync_filename = sync_url.split('/')[-1]
        sync_file_path = os.path.join(base_dir, sync_filename)
        download_file(sync_url, sync_file_path)
        move_csv_data(sync_file_path, fall_dir, folder_name)

    for i, url in enumerate(adl_urls):
        filename = url.split('/')[-1]
        file_path = os.path.join(base_dir, filename)

        download_file(url, file_path)

        folder_name = f"NoFall{str(i + 1).zfill(2)}"
        organize_files(file_path, no_fall_dir, folder_name)

        accel_url = adl_accel_urls[i]
        accel_filename = accel_url.split('/')[-1]
        accel_file_path = os.path.join(base_dir, accel_filename)
        download_file(accel_url, accel_file_path)
        move_csv_data(accel_file_path, no_fall_dir, folder_name)

        sync_url = adl_sync_urls[i]
        sync_filename = sync_url.split('/')[-1]
        sync_file_path = os.path.join(base_dir, sync_filename)
        download_file(sync_url, sync_file_path)
        move_csv_data(sync_file_path, no_fall_dir, folder_name)

    print("Download and extraction complete.")