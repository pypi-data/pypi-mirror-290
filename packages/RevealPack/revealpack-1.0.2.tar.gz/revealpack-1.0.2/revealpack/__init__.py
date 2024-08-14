import os
import shutil

def copy_file_or_directory(src, dest):
    """Copy a file or directory to the specified destination."""
    if os.path.isdir(src):
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
    else:
        shutil.copy(src, dest)

def copy_config_and_assets(destination=None):
    """Copy config.json and assets to the specified destination or current working directory."""
    current_dir = os.path.dirname(__file__)
    config_file = os.path.join(current_dir, 'config.json')
    assets_dir = os.path.join(current_dir, 'assets')

    if not destination:
        destination = os.getcwd()

    destination_config = os.path.join(destination, 'config.json')
    destination_assets = os.path.join(destination, 'assets')

    copy_file_or_directory(config_file, destination_config)
    copy_file_or_directory(assets_dir, destination_assets)
    print(f"config.json and assets have been copied to {destination}")
