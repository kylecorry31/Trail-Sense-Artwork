from PIL import Image
import sys
import os
import subprocess

# Read the path from the CLI args
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python apply-filter-to-all.py <input_path> <output_path> <filter_script_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    filter_script_path = sys.argv[3]

    # Check if filter script exists
    if not os.path.isfile(filter_script_path):
        print(f"Error: Filter script '{filter_script_path}' not found")
        sys.exit(1)
    
    # Check if input is a directory
    if os.path.isdir(input_path):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
        # Process all images in directory
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
        for filename in os.listdir(input_path):
            if any(filename.lower().endswith(ext) for ext in image_extensions):
                input_file = os.path.join(input_path, filename)
                output_file = os.path.join(output_path, filename)
                try:
                    # Run the specified filter script
                    subprocess.run([sys.executable, filter_script_path, input_file, output_file], check=True)
                    print(f"Processed {filename}")
                except subprocess.CalledProcessError as e:
                    print(f"Error processing {filename}: {e}")
    else:
        # Process single file
        subprocess.run([sys.executable, filter_script_path, input_path, output_path], check=True)
