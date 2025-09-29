import os
import shutil


def copy_folder_contents(src_folder, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    # Delete dest_folder contents
    for item in os.listdir(dest_folder):
        item_path = os.path.join(dest_folder, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)
    
    for item in os.listdir(src_folder):
        src_path = os.path.join(src_folder, item)
        dest_path = os.path.join(dest_folder, item)
        
        if os.path.isdir(src_path):
            copy_folder_contents(src_path, dest_path)
        else:
            print("Copying file:", src_path, "to", dest_path, " ...")
            shutil.copy(src_path, dest_path)
