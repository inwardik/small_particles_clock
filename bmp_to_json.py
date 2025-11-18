#!/usr/bin/env python3
"""
BMP to JSON Converter
Extracts white points from a BMP image and saves their coordinates to JSON.

This script reads a BMP file with white points on a black background and
converts the coordinates of all white pixels into a JSON file.

Usage:
    python bmp_to_json.py <input_bmp_file>

Output:
    Creates out.json with format: {"type": "geo", "data": [[x1, y1], [x2, y2], ...]}
"""

import sys
import json
from PIL import Image


def is_white_pixel(pixel, threshold=200):
    """
    Check if a pixel is white (or close to white).

    Args:
        pixel: Tuple of RGB values or a single grayscale value
        threshold: Minimum value for each RGB component to be considered white

    Returns:
        bool: True if pixel is white, False otherwise
    """
    # Handle grayscale images (single value)
    if isinstance(pixel, int):
        return pixel >= threshold

    # Handle RGB/RGBA images (tuple)
    if isinstance(pixel, tuple):
        # For RGBA, ignore alpha channel
        rgb_values = pixel[:3]
        return all(value >= threshold for value in rgb_values)

    return False


def extract_white_points(image_path):
    """
    Extract coordinates of all white pixels from a BMP image.

    Args:
        image_path: Path to the BMP file

    Returns:
        list: List of [x, y] coordinate pairs
    """
    try:
        # Open the image
        img = Image.open(image_path)

        # Convert to RGB if necessary
        if img.mode not in ('RGB', 'RGBA', 'L'):
            img = img.convert('RGB')

        # Get image dimensions
        width, height = img.size

        # Extract white points
        white_points = []

        # Iterate through all pixels
        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))

                if is_white_pixel(pixel):
                    white_points.append([x, y])

        return white_points

    except FileNotFoundError:
        print(f"Error: File '{image_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing image: {e}")
        sys.exit(1)


def save_to_json(points, output_file='out.json'):
    """
    Save points to JSON file in the required format.

    Args:
        points: List of [x, y] coordinate pairs
        output_file: Output file name (default: out.json)
    """
    output_data = {
        "type": "geo",
        "data": points
    }

    try:
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"Successfully saved {len(points)} points to {output_file}")
    except Exception as e:
        print(f"Error saving file: {e}")
        sys.exit(1)


def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python bmp_to_json.py <input_bmp_file>")
        print("\nExample:")
        print("  python bmp_to_json.py image.bmp")
        sys.exit(1)

    input_file = sys.argv[1]

    print(f"Processing {input_file}...")
    points = extract_white_points(input_file)

    if not points:
        print("Warning: No white points found in the image.")

    save_to_json(points)


if __name__ == "__main__":
    main()
