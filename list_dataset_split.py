import os

BASE_DIR = "data"

def _list_FallVision(base_dir):
    adl_files = []
    fall_files = []

    adl_path = os.path.join(base_dir, "FallVision", "ADL")
    fall_path = os.path.join(base_dir, "FallVision", "Fall")

    for path in [adl_path, fall_path]:
        if os.path.exists(adl_path):
            for subfolder in sorted(os.listdir(adl_path)):
                subfolder_path = os.path.join(adl_path, subfolder)
                if os.path.isdir(subfolder_path):
                    adl_files.extend([
                        os.path.join(subfolder_path, f)
                        for f in sorted(os.listdir(subfolder_path))
                        if f.endswith(".mp4")
                    ])

    if os.path.exists(fall_path):
        for subfolder in sorted(os.listdir(fall_path)):
            subfolder_path = os.path.join(fall_path, subfolder)
            if os.path.isdir(subfolder_path):
                fall_files.extend([
                    os.path.join(subfolder_path, f)
                    for f in sorted(os.listdir(subfolder_path))
                    if f.endswith(".mp4")
                ])

    return adl_files, fall_files

def _list_GMDCSA24(base_dir):
    adl_files = []
    fall_files = []

    GMDCSA24_path = os.path.join(base_dir, "GMDCSA24")

    for subject in sorted(os.listdir(GMDCSA24_path)):
        subject_path = os.path.join(GMDCSA24_path, subject)
        if os.path.isdir(subject_path):
            adl_path = os.path.join(subject_path, "ADL")
            fall_path = os.path.join(subject_path, "Fall")

            if os.path.exists(adl_path):
                adl_files.extend([os.path.join(adl_path, f) for f in sorted(os.listdir(adl_path)) if f.endswith(".mp4")])

            if os.path.exists(fall_path):
                fall_files.extend([os.path.join(fall_path, f) for f in sorted(os.listdir(fall_path)) if f.endswith(".mp4")])


    return adl_files, fall_files


def _list_URFD(base_dir):
    adl_dirs = []
    fall_dirs = []

    adl_path = os.path.join(base_dir, "URFD", "ADL")
    fall_path = os.path.join(base_dir, "URFD",  "Fall")

    if os.path.exists(adl_path):
        adl_dirs = [
            os.path.join(adl_path, d)
            for d in sorted(os.listdir(adl_path))
            if os.path.isdir(os.path.join(adl_path, d))
        ]

    if os.path.exists(fall_path):
        fall_dirs = [
            os.path.join(fall_path, d)
            for d in sorted(os.listdir(fall_path))
            if os.path.isdir(os.path.join(fall_path, d))
        ]

    return adl_dirs, fall_dirs

def _print_dataset_balance(adl_files, fall_files):
    len_adl = len(adl_files)
    len_fall = len(fall_files)
    total = len_adl + len_fall

    prop_adl = len_adl / total if total > 0 else 0
    prop_fall = len_fall / total if total > 0 else 0

    print(f"Total ADL: {len_adl} ({prop_adl:.2%})")
    print(f"Total Fall: {len_fall} ({prop_fall:.2%})")
    print(f"Total general: {total}")


def list_dataset_split():
    print("FallVision Dataset")
    fv_adl, fv_fall = _list_FallVision(BASE_DIR)
    _print_dataset_balance(fv_adl, fv_fall)

    print("\nGMDCSA24 Dataset")
    g24_adl, g24_fall = _list_GMDCSA24(BASE_DIR)
    _print_dataset_balance(g24_adl, g24_fall)

    print("\nURFD Dataset")
    urfd_adl, urfd_fall = _list_URFD(BASE_DIR)
    _print_dataset_balance(urfd_adl, urfd_fall)