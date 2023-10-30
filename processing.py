import os
import json
import shutil

def update_json_and_run_script(folder_path):
    # Create "Data" and "Labels" folders if they don't exist
    data_dir = os.path.join(folder_path, "Data")
    labels_dir = os.path.join(folder_path, "Labels")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)

    # Move all .tif files in the folder_path to the "Data" folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".tif"):
            source_file = os.path.join(folder_path, filename)
            dest_file = os.path.join(data_dir, filename)
            shutil.move(source_file, dest_file)

            # Check and rename files without regular expressions
            parts = filename.split("_")
            if len(parts) > 1 and parts[0].isdigit():
                new_name = f"41427-@09-9-1_RT_{int(parts[0]):02}_SEM_EBR_AdlDef_CMix0_RID_0.tif"
                os.rename(dest_file, os.path.join(data_dir, new_name))
    
    # Read the current content of demo_ResultsManager.json
    with open('demo_ResultsManager.json', 'r') as f:
        data = json.load(f)
    
    # Update dataset and output_dir parameters
    data["dataset"] = folder_path
    data["output_dir"] = os.path.join(os.path.dirname(folder_path), "8_bit_aligned_results")
    
    # Write the updated content back to demo_ResultsManager.json
    with open('demo_ResultsManager.json', 'w') as f:
        json.dump(data, f, indent=4)
    
    # Run the Python script
    os.system('python demo_ResultsManager.py')

def main():
    current_dir = os.getcwd()

    # Walk through the current directory and all its subdirectories
    for dirpath, dirnames, filenames in os.walk(current_dir):
        if "8_bit_aligned" in dirnames:
            folder_path = os.path.join(dirpath, "8_bit_aligned")
            print(f"Processing {folder_path}...")
            update_json_and_run_script(folder_path)

if __name__ == "__main__":
    main()
