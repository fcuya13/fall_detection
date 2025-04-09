from download_datasets.download_GMDCSA24 import download_and_extract_gmdcsa24
from download_datasets.download_FallVision import process_fallvision_files
from download_datasets.download_URFD import process_urfd_files
import os

BASE_DIR = "data"

# Configuration for gmdcsa24_downloader
GMDCSA_URL = "https://futn0rzrll.ufs.sh/f/j4V6zoXeTEG9XX9KCOYGlUt1cM0JgDbzOAwKHa65dvioRsxQ"
GMDCSA_ZIP_FILENAME = "GMDCSA24.zip"
GMDCSA_DIR = "GMDCSA24"

# Configuration for fallvision_downloader
FALLVISION_FOLDERS = {
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

FALLVISION_BASE_URL = "https://dataverse.harvard.edu/api/access/datafile/"

FALLVISION_DIR = "FallVision"
FALL_DIR = os.path.join(BASE_DIR, FALLVISION_DIR, "Fall")
NO_FALL_DIR = os.path.join(BASE_DIR, FALLVISION_DIR, "ADL")

# Configuration for urfd_downloader
FALL_URLS = [f"https://fenix.ur.edu.pl/mkepski/ds/data/fall-{i + 1:02d}-cam0-rgb.zip" for i in range(30)]
ADL_URLS = [f"https://fenix.ur.edu.pl/mkepski/ds/data/adl-{i + 1:02d}-cam0-rgb.zip" for i in range(40)]
FALL_ACCEL_URLS = [f"https://fenix.ur.edu.pl/mkepski/ds/data/fall-{i + 1:02d}-acc.csv" for i in range(30)]
ADL_ACCEL_URLS = [f"https://fenix.ur.edu.pl/mkepski/ds/data/adl-{i + 1:02d}-acc.csv" for i in range(40)]
FALL_SYNC_URLS = [f"https://fenix.ur.edu.pl/mkepski/ds/data/fall-{i + 1:02d}-data.csv" for i in range(30)]
ADL_SYNC_URLS = [f"https://fenix.ur.edu.pl/mkepski/ds/data/adl-{i + 1:02d}-data.csv" for i in range(40)]
URFD_BASE_DIR = "data"
URFD_FALL_DIR = os.path.join(URFD_BASE_DIR, "Fall")
URFD_NO_FALL_DIR = os.path.join(URFD_BASE_DIR, "ADL")

def main():
    # Run gmdcsa24_downloader
    download_and_extract_gmdcsa24(GMDCSA_URL, BASE_DIR, GMDCSA_DIR, GMDCSA_ZIP_FILENAME)

    # Run fallvision_downloader
    process_fallvision_files(FALLVISION_FOLDERS, FALLVISION_BASE_URL, FALL_DIR, NO_FALL_DIR)

    # Run urfd_downloader
    process_urfd_files(FALL_URLS, ADL_URLS, FALL_ACCEL_URLS, ADL_ACCEL_URLS, FALL_SYNC_URLS, ADL_SYNC_URLS, URFD_BASE_DIR, URFD_FALL_DIR, URFD_NO_FALL_DIR)