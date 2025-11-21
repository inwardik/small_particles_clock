# Image Processing Project Documentation

## Description

This project is designed to transform images with black lines on a white background into images with white dots on a black background. The dots are placed along the lines with even distribution.

## Key Features

- Automatic detection of black lines on white background
- Line thickness estimation
- Placement of white dots along lines with even spacing
- Limitation of maximum number of dots (default 600)
- Generation of two output images:
  - Original with dots of 3-pixel radius (6-pixel diameter)
  - Downscaled 6x with 1-pixel dots

## Installation

### Requirements

- Python 3.6+
- OpenCV
- NumPy
- SciPy

### Installing Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python process_image.py <input_image> <output_image> [max_dots]
```

### Parameters

- `input_image` - path to input image (white background, black lines)
- `output_image` - path to save output image
- `max_dots` - (optional) maximum number of dots, default 600

### Examples

```bash
# Process with maximum 600 dots
python process_image.py input.png output.png

# Process with maximum 1000 dots
python process_image.py input.png output.png 1000

# Process image in different folder
python process_image.py C:\images\input.png C:\images\output.png 600
```

## Output Files

The script creates two files:

1. **output.png** - original image
   - Black background
   - White dots with 3-pixel radius (6-pixel diameter)
   - Size matches input image

2. **output_small.png** - downscaled image
   - Black background
   - White dots of 1 pixel each
   - Size reduced 6x in width and height

## Algorithm Workflow

### 1. Loading and Processing Input Image

- Read image in grayscale
- Binary thresholding to extract black lines
- Find all pixels belonging to lines

### 2. Determining Line Parameters

- Calculate line thickness using distance transform
- Count total number of line pixels

### 3. Dot Placement

- Uniform sampling of points along lines
- Apply minimum distance filter for even distribution
- Limit number of dots to specified maximum

### 4. Creating Output Image

- Create image with black background
- Draw white dots with 3-pixel radius
- Save original image

### 5. Image Downscaling

- Apply max pooling with 6x6 pixel blocks
- Guarantee preservation of all dots (if block contains white pixel, resulting pixel is white)
- Save downscaled image with `_small` suffix

## Technical Details

### Image Downscaling Method

**Max pooling** method is used for downscaling:

```python
# For each 6x6 pixel block
block = output_img[i*6:(i+1)*6, j*6:(j+1)*6]
downscaled_img[i, j] = np.max(block)
```

Advantages:
- Guarantees preservation of all dots
- Does not blur the image
- Dots remain sharp and bright

### Dot Placement

A two-stage approach is used:

1. **Uniform sampling** - selecting points at equal intervals by pixel index
2. **Spatial filtering** - checking minimum distance between dots

Minimum distance between dots:
```python
min_distance = max(3, line_thickness)
```

### Dot Size

- **Radius**: 3 pixels
- **Diameter**: 6 pixels
- **After downscaling**: 1 pixel

Mathematics:
- Dot diameter = 6 pixels
- Downscaling factor = 6
- Resulting size = 6 / 6 = 1 pixel

## Limitations

- Input image must have white background and black lines
- Image dimensions should be multiples of 6 for correct downscaling
- Maximum number of dots affects detail level of result
- Very thin lines (1-2 pixels) may be processed less accurately

## Sample Output

```
Processed image saved to output.png
Downscaled image saved to output_small.png
Original size: 1200x800
Downscaled size: 200x133
Total dots placed: 600
Dot radius: 3 pixels
After downscaling, dots are 1 pixel each
```

## Project Structure

```
proj/
├── process_image.py    # Main processing script
├── requirements.txt    # Python dependencies
├── task.txt           # Task description
└── claude.md          # Documentation
```

## Troubleshooting

### Error: "No black lines found in the image"

**Cause**: Image does not contain sufficiently dark pixels

**Solution**: Check that:
- Input image has white background
- Lines are dark enough (black or dark gray)
- Image format is supported (PNG, JPG, BMP, etc.)

### Too few dots

**Cause**: Image contains fewer lines than maximum number of dots

**Solution**:
- Increase maximum number of dots
- Check input image

### Dots are distributed unevenly

**Cause**: Spatial filtering algorithm removes some dots

**Solution**: This is normal behavior to ensure even distribution

## License

Project created for educational purposes.

## Author

Created with Claude Code
