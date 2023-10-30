import os
import json

def update_json_and_run_script(folder_path):
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
