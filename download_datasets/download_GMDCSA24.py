import requests
import zipfile
import os

def download_and_extract_gmdcsa24(url, base_dir, dataset_dir, zip_filename):
    """
    Downloads, extracts, and renames the dataset to `GMDCSA24`.

    Args:
        url (str): The URL to download the dataset from.
        base_dir (str): The base directory where the dataset will be stored.
        dataset_dir (str): The subdirectory for the dataset.
        zip_filename (str): The name of the temporary zip file.
    """
    full_base_dir = os.path.join(base_dir, dataset_dir)
    os.makedirs(full_base_dir, exist_ok=True)

    print(f"Downloading GMDCSA dataset...")
    response = requests.get(url)

    if response.status_code == 200:
        with open(zip_filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded dataset successfully.")

        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(full_base_dir)
        print(f"Extracted dataset to {full_base_dir}.")

        # Rename the extracted folder to `GMDCSA24`
        os.rename(full_base_dir, os.path.join(base_dir, "GMDCSA24"))
        print(f"Renamed dataset folder to `GMDCSA24`.")

        os.remove(zip_filename)
        print(f"Deleted zip file: {zip_filename}")
    else:
        print(f"Error downloading the file. Status code: {response.status_code}")