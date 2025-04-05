import sys
import argparse
from PIL import Image
import numpy as np

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Blend lines in an image.')
    parser.add_argument('input_image', help='Path to the input image file')
    parser.add_argument('output_image', help='Path for the output image file')
    parser.add_argument('--black-value', type=int, default=50, 
                        help='Threshold for black pixels (0-255, default: 50)')
    parser.add_argument('--white-value', type=int, default=230, 
                        help='Threshold for white pixels (0-255, default: 230)')
    parser.add_argument('--saturation', type=float, default=0.5, 
                        help='Saturation percentage for line color replacement (0-1, default: 0.5)')
    
    args = parser.parse_args()
    
    # Validate the arguments
    if not (0 <= args.black_value <= 255):
        print("Black value must be an integer between 0 and 255.")
        sys.exit(1)
    
    if not (0 <= args.white_value <= 255):
        print("White value must be an integer between 0 and 255.")
        sys.exit(1)
    
    if not (0 <= args.saturation <= 1):
        print("Saturation must be a value between 0 and 1.")
        sys.exit(1)

    img = Image.open(args.input_image).convert("RGB")
    data = np.array(img)

    # Create masks using vectorized operations
    white_mask = np.all(data > args.white_value, axis=2)
    black_mask = np.all(data < args.black_value, axis=2)
    
    # Mask for non-white and non-black pixels
    mask = ~(white_mask | black_mask)

    # Get average color from valid pixels
    valid_pixels = data[mask]
    if len(valid_pixels) == 0:
        print("No valid pixels to calculate average color.")
        sys.exit(1)

    avg_color = valid_pixels.mean(axis=0).astype(int)

    # Calculate replacement color using configurable saturation
    replacement_color = (avg_color * args.saturation).astype(int)

    # Replace pure black pixels
    data[black_mask] = replacement_color

    # Save the output image
    Image.fromarray(data).save(args.output_image)
    print(f"Saved modified image to {args.output_image}")

if __name__ == "__main__":
    main()
