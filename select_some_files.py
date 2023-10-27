import os
import shutil

def select_two_files_from_subfolders(src_dir, dest_dir):
    # Ensure the destination directory exists; if not, create it
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Iterate over each main folder
    for main_folder_name in os.listdir(src_dir):
        main_folder_path = os.path.join(src_dir, main_folder_name)

        if os.path.isdir(main_folder_path):
            # For each subfolder, pick up to 2 files
            for subfolder_name in os.listdir(main_folder_path):
                subfolder_path = os.path.join(main_folder_path, subfolder_name)
                if os.path.isdir(subfolder_path):
                    selected_files = 0
                    for file_name in os.listdir(subfolder_path):
                        file_path = os.path.join(subfolder_path, file_name)
                        if os.path.isfile(file_path) and selected_files < 2:
                            # Copy the selected file to the destination directory
                            # Prefix the file name with its subfolder name to avoid collisions
                            shutil.copy2(file_path, os.path.join(dest_dir, subfolder_name + "_" + file_name))
                            selected_files += 1

if __name__ == "__main__":
    src_directory = "."  # Current directory
    final_directory = "final_folder"

    select_two_files_from_subfolders(src_directory, final_directory)
