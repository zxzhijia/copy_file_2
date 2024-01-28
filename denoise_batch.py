import os
import json
import subprocess
import shutil

def run_denoise_util(input_dir, output_dir, noise_level):
    cmd = [
        "python", "denoise_util.py",
        "--input_image_format", ".tif",
        "--output_image_format", ".tif",
        "--input_directory", input_dir,
        "--output_directory", output_dir,
        "--params_json", "data.json",
        "--new_binary", "False"
    ]
    subprocess.run(cmd)

def update_noise_level(noise_level):
    with open('data.json', 'r+') as file:
        data = json.load(file)
        data['noise_level'] = noise_level
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

def copy_directory_structure(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isdir(src_path):
            copy_directory_structure(src_path, dst_path)
        else:
            shutil.copy2(src_path, dst_path)

def process_subfolders(parent_folder, output_base):
    for subdir, dirs, files in os.walk(parent_folder):
        if any(file.endswith('.tif') for file in files):
            rel_subdir = os.path.relpath(subdir, parent_folder)
            for noise_level in [3, 5, 7]:
                output_subdir = os.path.join(output_base, rel_subdir, 'noise_{}'.format(noise_level))
                os.makedirs(output_subdir, exist_ok=True)
                update_noise_level(noise_level)
                run_denoise_util(subdir, output_subdir, noise_level)

if __name__ == "__main__":
    parent_folder = "./../Image/Input"  # Change this to your parent folder path
    output_base = os.path.join('..', 'Image', 'Output')
    copy_directory_structure(parent_folder, output_base)
    process_subfolders(parent_folder, output_base)

