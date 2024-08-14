import os
import shutil
import filecmp
import logging
import fnmatch
from pathlib import Path

ignore = ["*.DS_Store", "*.ffs_db", "__pycache__"]


def copy_and_overwrite(src, dest, copied_files=None):
    """Copy directory from src to dest, overwrite if different. Optionally return a list of copied file paths."""
    if copied_files is None:
        copied_files = []

    if not os.path.exists(dest):
        shutil.copytree(src, dest)
        logging.info(f"Copying directory {dest}.")
        for root, _, files in os.walk(dest):
            for file in files:
                copied_files.append(os.path.join(root, file))
        return copied_files

    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dest_item = os.path.join(dest, item)

        if os.path.isdir(src_item):
            copy_and_overwrite(src_item, dest_item, copied_files)
        else:
            copy_file_if_different(src_item, dest_item, copied_files)

    return copied_files


def copy_file_if_different(src, dest, copied_files=[]):
    """
    Copy a file from src to dest, overwrite if different.

    Parameters:
    - src (str): Source file path
    - dest (str): Destination file path
    """
    # Check if src file matches any pattern in the ignore list
    src_file_name = os.path.basename(src)
    if any(fnmatch.fnmatch(src_file_name, pattern) for pattern in ignore):
        logging.info(f"Skipping file {src} as it matches ignore pattern.")
        return

    if os.path.exists(dest):
        if not filecmp.cmp(src, dest, shallow=False):
            shutil.copy2(src, dest)
            logging.info(f"Overwriting file {dest} because it's different.")
        # else:
        # logging.info(f"File {dest} is identical, skipping copy.")
    else:
        shutil.copy2(src, dest)
        logging.info(f"Copying file {dest}.")
    copied_files.append(dest)

def get_theme_path(config):
    """Locate theme specified in config.json."""
    theme_name = config["theme"]
    theme_path = Path(theme_name)
    
    source_root = Path(config["directories"]["source"]["root"])
    theme_dir_in_reveal = source_root / "cached" / "reveal.js" / "css" / "theme" / "source"
    custom_theme_dir = Path("custom_theme")
    # Check if the theme is a builtin theme in the reveal.js directory
    def is_builtin_theme(theme_name):
        for filename in theme_dir_in_reveal.iterdir():
            if filename.stem == theme_name:
                return filename
        return None
    # Determine the theme path
    if theme_path.suffix == '.css':
        theme_full_path = theme_path
    elif theme_path.suffix in {'.scss', '.sass'}:
        if theme_path.is_file():
            theme_full_path = theme_path
        elif (custom_theme_dir / theme_path).is_file():
            theme_full_path = custom_theme_dir / theme_path
        elif is_builtin_theme(theme_path.stem):
            theme_full_path = is_builtin_theme(theme_path.stem)
        else:
            theme_full_path = None
    else:
        # No extension provided, assume .scss
        if (theme_path.with_suffix('.scss')).is_file():
            theme_full_path = theme_path.with_suffix('.scss')
        elif (custom_theme_dir / theme_path.with_suffix('.scss')).is_file():
            theme_full_path = custom_theme_dir / theme_path.with_suffix('.scss')
        elif is_builtin_theme(theme_path.stem):
            theme_full_path = is_builtin_theme(theme_path.stem)
        else:
            theme_full_path = custom_theme_dir / theme_path.with_suffix('.scss').name
    if theme_full_path is None or not theme_full_path.exists():
        return ""
    else:
        return str(theme_full_path)

def cleanup_temp_files(files_list):
    """Delete specified files and remove their parent directories if they become empty."""
    for file_path in files_list:
        # Delete the file if it exists
        if os.path.isfile(file_path):
            os.remove(file_path)
            logging.debug(f"Deleted file: {file_path}")
        else:
            logging.warning(f"File not found: {file_path}")
        
        # Check if the parent directory exists and is empty, then remove it
        parent_dir = os.path.dirname(file_path)
        while parent_dir:
            if os.path.exists(parent_dir):
                if not os.listdir(parent_dir):  # Check if directory is empty
                    os.rmdir(parent_dir)
                    logging.debug(f"Deleted empty directory: {parent_dir}")
                else:
                    break  # Stop if directory is not empty
            else:
                logging.debug(f"Directory does not exist: {parent_dir}")
                break  # Exit the loop if the directory doesn't exist
            
            parent_dir = os.path.dirname(parent_dir)
