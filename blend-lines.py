import sys
from PIL import Image
import numpy as np

def main():
    if len(sys.argv) < 3:
        print("Usage: python blend-lines.py <input_image> <output_image> <black_value>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    black_value = 50
    if len(sys.argv) == 4:
        try:
            black_value = int(sys.argv[3])
            if not (0 <= black_value <= 255):
                raise ValueError
        except ValueError:
            print("Black value must be an integer between 0 and 255.")
            sys.exit(1)

    img = Image.open(input_path).convert("RGB")
    data = np.array(img)

    # Create masks using vectorized operations
    white_mask = np.all(data > 230, axis=2)
    black_mask = np.all(data < black_value, axis=2)
    
    # Mask for non-white and non-black pixels
    mask = ~(white_mask | black_mask)

    # Get average color from valid pixels
    valid_pixels = data[mask]
    if len(valid_pixels) == 0:
        print("No valid pixels to calculate average color.")
        sys.exit(1)

    avg_color = valid_pixels.mean(axis=0).astype(int)

    # Calculate replacement color
    replacement_color = (avg_color * 0.5).astype(int)

    # Replace pure black pixels
    data[black_mask] = replacement_color

    # Save the output image
    Image.fromarray(data).save(output_path)
    print(f"Saved modified image to {output_path}")

if __name__ == "__main__":
    main()
