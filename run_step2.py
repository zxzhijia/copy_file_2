import os
import shutil
import subprocess
import time

def monitor_and_process(input_root, processing_path, output_root, test_script_path):
    while True:
        # Scan for '8bit' subfolders and process files
        for root, dirs, files in os.walk(input_root):
            if '8bit' in root:
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff')):
                        file_path = os.path.join(root, file)
                        dest_path = os.path.join(processing_path, file)
                        
                        # Copy file to processing path
                        shutil.copy2(file_path, dest_path)

                # Run test_xu.py (assuming it processes the files in processing_path)
                subprocess.run(['python', test_script_path])

                # Define and create the Ksharp folder
                ksharp_folder = os.path.join(root, 'Ksharp')
                if not os.path.exists(ksharp_folder):
                    os.makedirs(ksharp_folder)

                # Move output from output_root to Ksharp folder
                for output_file in os.listdir(output_root):
                    output_file_path = os.path.join(output_root, output_file)
                    shutil.move(output_file_path, ksharp_folder)

        # Sleep for a bit before checking again
        time.sleep(10)  # checks every 10 seconds

# Example usage
input_root = 'path/to/monitor'  # Root folder to monitor
processing_path = 'path/to/process/images'  # Path where images are copied and processed
output_root = 'path/to/output'  # Folder where test_xu.py saves its output
test_script_path = 'path/to/test_xu.py'  # Path to the test_xu.py script

monitor_and_process(input_root, processing_path, output_root, test_script_path)
