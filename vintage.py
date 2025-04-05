from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import sys

def add_vintage_effect(image_path, output_path):
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

    # Blend sepia image
    faded = Image.blend(faded, img, alpha=0.5)

    # Add subtle noise/grain
    # Generate noise once and repeat it for all channels
    width, height = faded.size
    noise = np.random.normal(0, 5, width * height).reshape((height, width))
    noise_rgb = np.stack([noise, noise, noise], axis=2)    
    noisy_image = np.array(faded) + noise_rgb
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    final_img = Image.fromarray(noisy_image)

    # Revert all pure white pixels from the original back to pure white
    original_pixels = np.array(img)
    final_pixels = np.array(final_img)
    mask = np.all(original_pixels == [255, 255, 255], axis=-1)
    final_pixels[mask] = [255, 255, 255]
    final_img = Image.fromarray(final_pixels)

    final_img = final_img.convert("RGB")  # Remove alpha for saving

    final_img.save(output_path)
    print(f"Saved vintage image to {output_path}")

# Read the path from the CLI args
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python vintage.py <input_path> <output_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    add_vintage_effect(input_path, output_path)
