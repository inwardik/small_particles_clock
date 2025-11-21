import cv2
import numpy as np
from scipy.spatial import distance

def process_image(input_path, output_path, max_dots=600):
    """
    Process an image with white background and black lines to create
    white dots on black background where the lines were.

    Args:
        input_path: Path to input image
        output_path: Path to save output image
        max_dots: Maximum number of dots to place (default 600)
    """
    # Read the image
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Could not read image from {input_path}")

    height, width = img.shape

    # Threshold to get black pixels (lines)
    # Black pixels have low values, white pixels have high values
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    # Find all black line pixels
    line_pixels = np.column_stack(np.where(binary > 0))

    if len(line_pixels) == 0:
        print("No black lines found in the image")
        return

    # Estimate line thickness by looking at the morphological structure
    kernel = np.ones((3, 3), np.uint8)
    eroded = cv2.erode(binary, kernel, iterations=1)
    line_thickness = max(1, int(np.mean(binary[binary > 0]) / 255 * 5))

    # Calculate the actual line thickness more accurately
    # by finding the distance transform
    dist_transform = cv2.distanceTransform(binary, cv2.DIST_L2, 3)
    line_thickness = max(1, int(np.max(dist_transform) * 2))

    # Sample points along the lines
    # Calculate spacing based on number of line pixels and max dots
    total_line_pixels = len(line_pixels)

    if total_line_pixels <= max_dots:
        # Use all pixels if we have fewer than max_dots
        sampled_points = line_pixels
    else:
        # Sample evenly spaced points
        spacing = total_line_pixels / max_dots
        indices = np.linspace(0, total_line_pixels - 1, max_dots, dtype=int)
        sampled_points = line_pixels[indices]

        # Further filter points to ensure they're spatially distributed
        # using a simple distance-based approach
        final_points = [sampled_points[0]]
        min_distance = max(3, line_thickness)

        for point in sampled_points[1:]:
            # Check if point is far enough from all selected points
            distances = distance.cdist([point], final_points)
            if np.min(distances) >= min_distance:
                final_points.append(point)
                if len(final_points) >= max_dots:
                    break

        sampled_points = np.array(final_points)

    # Create output image with black background
    output_img = np.zeros((height, width), dtype=np.uint8)

    # Draw white dots at sampled positions
    dot_radius = 3  # Fixed radius of 3 pixels (diameter 6 pixels)

    for y, x in sampled_points:
        cv2.circle(output_img, (x, y), dot_radius, 255, -1)

    # Save the original image (before downscaling)
    cv2.imwrite(output_path, output_img)

    # Downscale the image by 6x using max pooling
    # This ensures white dots (radius 6) become single white pixels
    scale_factor = 6
    new_height = height // scale_factor
    new_width = width // scale_factor

    downscaled_img = np.zeros((new_height, new_width), dtype=np.uint8)

    for i in range(new_height):
        for j in range(new_width):
            # Take 6x6 block and find maximum value
            block = output_img[i*scale_factor:(i+1)*scale_factor,
                              j*scale_factor:(j+1)*scale_factor]
            downscaled_img[i, j] = np.max(block)

    # Save the downscaled image with _small suffix
    import os
    base_name, ext = os.path.splitext(output_path)
    small_output_path = f"{base_name}_small{ext}"
    cv2.imwrite(small_output_path, downscaled_img)

    print(f"Original image saved to {output_path}")
    print(f"Downscaled image saved to {small_output_path}")
    print(f"Original size: {width}x{height}")
    print(f"Downscaled size: {new_width}x{new_height}")
    print(f"Total dots placed: {len(sampled_points)}")
    print(f"Dot radius: {dot_radius} pixels")
    print(f"After downscaling, dots are 1 pixel each")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python process_image.py <input_image> <output_image> [max_dots]")
        print("Example: python process_image.py input.png output.png 600")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    max_dots = int(sys.argv[3]) if len(sys.argv) > 3 else 600

    process_image(input_path, output_path, max_dots)
