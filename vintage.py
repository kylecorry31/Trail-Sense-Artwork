from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import sys
import argparse

def add_vintage_effect(image_path, output_path, sepia_amount=0.5, noise_amount=5, preserve_white=True):
    # Load image
    img = Image.open(image_path).convert("RGB")

    # Resize
    img.thumbnail((1500, 1500))

    # Apply sepia tone (vectorized)
    sepia = np.array(img)
    sepia_flat = sepia.reshape(-1, 3)
    
    # Matrix multiplication for sepia tone conversion
    sepia_matrix = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    
    transformed = np.dot(sepia_flat, sepia_matrix.T)
    tr, tg, tb = transformed[:, 0], transformed[:, 1], transformed[:, 2]

    sepia_image = np.stack([
        np.clip(tr, 0, 255),
        np.clip(tg, 0, 255),
        np.clip(tb, 0, 255)
    ], axis=1).astype(np.uint8).reshape(sepia.shape)

    sepia_img = Image.fromarray(sepia_image)

    # Add slight blur and reduce contrast for faded look
    faded = sepia_img.filter(ImageFilter.GaussianBlur(0.5))
    enhancer = ImageEnhance.Contrast(faded)
    faded = enhancer.enhance(0.85)

    # Blend sepia image (using configurable sepia amount)
    faded = Image.blend(faded, img, alpha=1-sepia_amount)

    # Add subtle noise/grain with configurable amount
    width, height = faded.size
    noise = np.random.normal(0, noise_amount, width * height).reshape((height, width))
    noise_rgb = np.stack([noise, noise, noise], axis=2)    
    noisy_image = np.array(faded) + noise_rgb
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    final_img = Image.fromarray(noisy_image)

    # Optionally preserve white pixels
    if preserve_white:
        original_pixels = np.array(img)
        final_pixels = np.array(final_img)
        mask = np.all(original_pixels == [255, 255, 255], axis=-1)
        final_pixels[mask] = [255, 255, 255]
        final_img = Image.fromarray(final_pixels)

    final_img = final_img.convert("RGB")  # Remove alpha for saving

    final_img.save(output_path)
    print(f"Saved vintage image to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Apply vintage effect to an image')
    parser.add_argument('input_path', help='Path to input image')
    parser.add_argument('output_path', help='Path for output image')
    parser.add_argument('--sepia', type=float, default=0.5, 
                        help='Amount of sepia effect (0.0-1.0, default: 0.5)')
    parser.add_argument('--noise', type=float, default=5.0,
                        help='Amount of noise/grain (default: 5.0)')
    parser.add_argument('--no-preserve-white', action='store_false', dest='preserve_white',
                        help='Disable preserving white pixels from the original image')
    
    args = parser.parse_args()
    
    add_vintage_effect(
        args.input_path,
        args.output_path,
        sepia_amount=args.sepia,
        noise_amount=args.noise,
        preserve_white=args.preserve_white
    )
