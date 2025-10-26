<!-- Powered by BMAD™ Core -->

# Optimize Visuals

---

task:
id: optimize-visuals
name: Optimize Visuals
description: Optimize images for web and print by resizing, compressing, and converting to optimal formats
persona_default: screenshot-specialist
inputs: - image-path (path to image file to optimize) - optimization-target (web, print, or both) - quality-threshold (optional: acceptable quality loss percentage)
steps: - Analyze current image properties (dimensions, format, file size) - Determine target dimensions based on usage - Resize to appropriate dimensions - Compress without significant quality loss - Convert to optimal format if needed (PNG/JPEG/SVG/WebP) - Generate multiple resolutions if needed (1×, 2× for Retina) - Optimize for print (300 DPI) if required - Verify quality meets standards - Generate optimized file(s)
output: Optimized image file(s) with metadata report

---

## Purpose

This task helps you optimize images for their intended use, balancing quality with file size. Proper optimization improves web page load times, reduces book file sizes, and ensures print quality while maintaining professional appearance.

## Prerequisites

Before starting this task:

- Original high-resolution image available
- Target usage defined (web, print, or both)
- Understanding of quality requirements
- Image optimization tools installed

## Optimization Tools

### Command-Line Tools

**ImageMagick (Cross-platform, Free):**

```bash
# Install
brew install imagemagick          # macOS
sudo apt install imagemagick      # Linux
choco install imagemagick         # Windows

# Usage
convert input.png -resize 1600x -quality 85 output.jpg
```

**pngquant (PNG optimization, Free):**

```bash
# Install
brew install pngquant             # macOS
sudo apt install pngquant         # Linux

# Usage
pngquant --quality=65-80 input.png --output output.png
```

**jpegoptim (JPEG optimization, Free):**

```bash
# Install
brew install jpegoptim            # macOS
sudo apt install jpegoptim        # Linux

# Usage
jpegoptim --max=85 --strip-all input.jpg
```

**oxipng (Advanced PNG optimization, Free):**

```bash
# Install
brew install oxipng               # macOS
cargo install oxipng              # Rust

# Usage
oxipng -o 4 --strip safe input.png
```

**cwebp (WebP conversion, Free):**

```bash
# Install
brew install webp                 # macOS
sudo apt install webp             # Linux

# Usage
cwebp -q 80 input.png -o output.webp
```

### GUI Tools

**Squoosh (Web-based, Free):**

- URL: https://squoosh.app
- Pros: Visual comparison, multiple formats
- Best for: Individual image optimization

**ImageOptim (macOS, Free):**

- Pros: Drag-and-drop, batch processing
- Best for: Batch PNG/JPEG optimization

**TinyPNG (Web-based, Free tier):**

- URL: https://tinypng.com
- Pros: Excellent compression, simple
- Cons: 5MB limit, 20 images/day on free tier

**XnConvert (Cross-platform, Free):**

- Pros: Batch processing, many formats
- Best for: Complex batch operations

## Optimization Targets

### Web Optimization

**Goals:**

- Fast page load (target: < 200KB per image)
- Retina display support (2× resolution)
- Modern format support (WebP, AVIF)
- Responsive images (multiple sizes)

**Target specifications:**

```
Content width: 800px
Retina multiplier: 2×
Target image width: 1600px
Target file size: < 200KB
Format: WebP (primary), JPEG (fallback), PNG (if transparency needed)
```

### Print Optimization

**Goals:**

- High resolution (300 DPI)
- Color accuracy (CMYK for professional printing)
- Appropriate file format (TIFF, high-quality PDF, or PNG)

**Target specifications:**

```
Print width: 5 inches (example)
Required DPI: 300
Required pixels: 5 × 300 = 1500px
Target file size: < 5MB (for book production)
Format: PNG or TIFF (lossless)
Color space: CMYK (for offset printing) or RGB (for digital printing)
```

### Both Web and Print

**Workflow:**

1. Keep original high-resolution image (print quality)
2. Create web-optimized versions from original
3. Organize into folders: `original/`, `web/`, `print/`

## Workflow Steps

### 1. Analyze Current Image

**Check image properties:**

```bash
# Using ImageMagick
identify -verbose image.png

# Key information to check:
# - Dimensions (width × height)
# - File size
# - Format (PNG, JPEG, etc.)
# - Color space (RGB, CMYK)
# - Bit depth
# - DPI/resolution
```

**Example output:**

```
Filename: screenshot.png
Dimensions: 3200x2000 pixels
File size: 2.4MB
Format: PNG (Portable Network Graphics)
Color space: sRGB
Bit depth: 8-bit
Resolution: 144×144 DPI
```

**Analysis:**

- **Issue 1:** 3200×2000 is too large for web (target: 1600px width)
- **Issue 2:** 2.4MB is too large for web (target: < 200KB)
- **Issue 3:** 144 DPI is insufficient for print (target: 300 DPI)

### 2. Determine Target Dimensions

**Based on usage:**

**Web content area:**

```
Max content width: 800px
Retina multiplier: 2×
Target width: 1600px
Maintain aspect ratio
```

**Print book (example):**

```
Book trim size: 6" × 9"
Image width on page: 5"
Required DPI: 300
Target width: 5 × 300 = 1500px
```

**Both:**

```
Web: 1600px width
Print: 1500px width (minimum)
Decision: Use 1600px for both (meets both requirements)
```

### 3. Resize to Appropriate Dimensions

**Using ImageMagick:**

```bash
# Resize to specific width, maintain aspect ratio
convert input.png -resize 1600x output.png

# Resize to specific dimensions (may distort)
convert input.png -resize 1600x1000 output.png

# Resize with maximum dimensions (maintains aspect)
convert input.png -resize 1600x1000\> output.png

# Batch resize all PNG files
for file in *.png; do
  convert "$file" -resize 1600x "optimized/$file"
done
```

**Using sips (macOS built-in):**

```bash
# Resize to width
sips -Z 1600 input.png --out output.png

# Batch resize
sips -Z 1600 *.png
```

**Quality considerations:**

- **Downscaling:** Safe, improves file size
- **Upscaling:** Avoid when possible (reduces quality)
- **Aspect ratio:** Always maintain unless specific design requirement

### 4. Compress Without Quality Loss

**PNG compression (lossless):**

```bash
# Using pngquant (lossy but visually lossless)
pngquant --quality=65-80 input.png --output output.png

# Using oxipng (truly lossless)
oxipng -o 4 --strip safe input.png

# Using ImageOptim (macOS GUI)
# Drag files to ImageOptim app
```

**JPEG compression (lossy):**

```bash
# Using ImageMagick
convert input.jpg -quality 85 -strip output.jpg

# Using jpegoptim
jpegoptim --max=85 --strip-all input.jpg

# Quality guidelines:
# 90-100: High quality (large file)
# 80-89: Good quality (recommended for most screenshots)
# 70-79: Acceptable quality (for large images)
# < 70: Visible artifacts (avoid for professional work)
```

**Compression comparison test:**

```bash
# Test different quality levels
convert input.jpg -quality 95 output-q95.jpg
convert input.jpg -quality 85 output-q85.jpg
convert input.jpg -quality 75 output-q75.jpg
convert input.jpg -quality 65 output-q65.jpg

# Compare file sizes
ls -lh output-q*.jpg

# Visual comparison: open all in image viewer
```

### 5. Convert to Optimal Format

**Format selection guide:**

| Content Type     | Web          | Print        |
| ---------------- | ------------ | ------------ |
| Screenshots (UI) | PNG or WebP  | PNG          |
| Code editor      | PNG          | PNG          |
| Photos           | JPEG or WebP | JPEG or TIFF |
| Diagrams         | SVG or PNG   | SVG or PDF   |
| Icons            | SVG          | SVG or PDF   |
| Logos            | SVG or PNG   | SVG or PDF   |

**PNG → JPEG (when transparency not needed):**

```bash
# Convert PNG to JPEG
convert input.png -quality 85 -background white -flatten output.jpg

# Explanation:
# -quality 85: Good quality/size balance
# -background white: Fill transparency with white
# -flatten: Merge layers
```

**PNG/JPEG → WebP (modern web):**

```bash
# Convert to WebP
cwebp -q 80 input.png -o output.webp

# Batch convert
for file in *.png; do
  cwebp -q 80 "$file" -o "${file%.png}.webp"
done
```

**SVG optimization (for diagrams):**

```bash
# Install SVGO
npm install -g svgo

# Optimize SVG
svgo input.svg -o output.svg

# Batch optimize
svgo -f ./svg-folder -o ./svg-optimized
```

**RGB → CMYK (for professional printing):**

```bash
# Convert to CMYK using ImageMagick
convert input.png -colorspace CMYK output.tiff

# Note: Consult with print vendor for specific requirements
```

### 6. Generate Multiple Resolutions

**For responsive web (1×, 2×, 3×):**

```bash
# Generate 1× (base)
convert input.png -resize 800x output-1x.png

# Generate 2× (Retina)
convert input.png -resize 1600x output-2x.png

# Generate 3× (high-density displays)
convert input.png -resize 2400x output-3x.png

# Optimize all
pngquant --quality=65-80 output-*.png
```

**HTML usage:**

```html
<img
  src="image-1x.png"
  srcset="image-1x.png 1x, image-2x.png 2x, image-3x.png 3x"
  alt="Description"
  width="800"
  height="500"
/>
```

**Responsive images (different sizes):**

```bash
# Generate multiple widths
convert input.png -resize 400x output-400.png
convert input.png -resize 800x output-800.png
convert input.png -resize 1200x output-1200.png
convert input.png -resize 1600x output-1600.png
```

**HTML usage:**

```html
<img
  srcset="image-400.png 400w, image-800.png 800w, image-1200.png 1200w, image-1600.png 1600w"
  sizes="(max-width: 600px) 400px,
         (max-width: 900px) 800px,
         (max-width: 1200px) 1200px,
         1600px"
  src="image-800.png"
  alt="Description"
/>
```

### 7. Optimize for Print (300 DPI)

**Check/set DPI:**

```bash
# Check current DPI
identify -verbose input.png | grep Resolution
# Output: Resolution: 72x72

# Set DPI to 300 (doesn't resize, just sets metadata)
convert input.png -density 300 -units PixelsPerInch output.png

# Verify
identify -verbose output.png | grep Resolution
# Output: Resolution: 300x300
```

**Calculate required dimensions for print:**

```
Formula: Print size (inches) × DPI = Required pixels

Example:
Book page width: 5 inches
Required DPI: 300
Required width: 5 × 300 = 1500 pixels

If image is 3000px wide:
Print size: 3000 ÷ 300 = 10 inches ✓ (sufficient for 5" print)

If image is 1000px wide:
Print size: 1000 ÷ 300 = 3.33 inches ✗ (insufficient for 5" print)
```

**Upscaling for print (if necessary):**

```bash
# Only if original is too small and no better source available
# Use with caution - quality will be reduced

# Bicubic interpolation (best for upscaling)
convert input.png -resize 1500x -filter Lanczos -interpolate bicubic output.png

# Better approach: Recapture screenshot at higher resolution
```

### 8. Verify Quality

**Visual inspection:**

```bash
# Open original and optimized side-by-side
open input.png output.png

# Or use ImageMagick to create comparison
convert input.png output.png +append comparison.png
```

**Quality metrics:**

```bash
# Compare images (PSNR and SSIM)
compare -metric PSNR input.png output.png null:
# Output: 45.2 (higher is better, >40 is excellent)

# Calculate file size reduction
du -h input.png output.png
# Before: 2.4M
# After: 180K
# Savings: 92%
```

**Quality checklist:**

- [ ] Text is crisp and readable
- [ ] No visible compression artifacts
- [ ] Colors accurate
- [ ] No banding in gradients
- [ ] Annotations still clear
- [ ] File size meets target (< 200KB for web)
- [ ] Resolution meets target (300 DPI for print)

### 9. Generate Optimized Files

**Organized output:**

```bash
# Create folder structure
mkdir -p optimized/{web,print,original}

# Web optimization
convert input.png -resize 1600x -quality 85 optimized/web/image-web.png
pngquant --quality=65-80 optimized/web/image-web.png --ext .png --force
cwebp -q 80 optimized/web/image-web.png -o optimized/web/image-web.webp

# Print optimization
convert input.png -resize 1500x -density 300 optimized/print/image-print.png

# Copy original
cp input.png optimized/original/image-original.png
```

**Metadata report:**

```bash
# Generate report
cat > optimized/image-report.txt <<EOF
Image Optimization Report
Generated: $(date)

Original:
  File: input.png
  Dimensions: $(identify -format "%wx%h" input.png)
  File size: $(du -h input.png | cut -f1)
  DPI: $(identify -format "%x×%y" input.png)

Web version:
  File: image-web.png
  Dimensions: $(identify -format "%wx%h" optimized/web/image-web.png)
  File size: $(du -h optimized/web/image-web.png | cut -f1)
  Format: PNG

WebP version:
  File: image-web.webp
  File size: $(du -h optimized/web/image-web.webp | cut -f1)
  Format: WebP

Print version:
  File: image-print.png
  Dimensions: $(identify -format "%wx%h" optimized/print/image-print.png)
  File size: $(du -h optimized/print/image-print.png | cut -f1)
  DPI: 300

Optimization: $(echo "scale=1; ($(stat -f%z input.png) - $(stat -f%z optimized/web/image-web.png)) * 100 / $(stat -f%z input.png)" | bc)% size reduction
EOF
```

## Success Criteria

Image optimization is complete when:

- [ ] Image resized to target dimensions
- [ ] File size meets targets (< 200KB web, < 5MB print)
- [ ] Quality verified (no visible artifacts)
- [ ] Correct format selected (PNG/JPEG/WebP)
- [ ] DPI set correctly for print (300 DPI)
- [ ] Multiple resolutions generated if needed (1×, 2×)
- [ ] Files organized in appropriate folders
- [ ] Metadata report generated
- [ ] Original high-resolution image preserved

## Optimization Workflows

### Workflow 1: Web-Only Screenshot

```bash
#!/bin/bash
# optimize-web.sh

INPUT=$1
OUTPUT_DIR="optimized/web"
mkdir -p "$OUTPUT_DIR"

# Resize to 1600px width
convert "$INPUT" -resize 1600x -strip temp.png

# Optimize PNG
pngquant --quality=65-80 temp.png --ext .png --force

# Generate WebP
cwebp -q 80 temp.png -o "${OUTPUT_DIR}/$(basename ${INPUT%.*}).webp"

# Move optimized PNG
mv temp.png "${OUTPUT_DIR}/$(basename ${INPUT%.*}).png"

echo "Optimized for web: ${OUTPUT_DIR}"
ls -lh "${OUTPUT_DIR}"
```

**Usage:**

```bash
chmod +x optimize-web.sh
./optimize-web.sh screenshot.png
```

### Workflow 2: Print-Only Screenshot

```bash
#!/bin/bash
# optimize-print.sh

INPUT=$1
OUTPUT_DIR="optimized/print"
PRINT_WIDTH=1500  # 5 inches × 300 DPI
mkdir -p "$OUTPUT_DIR"

# Resize if needed (only downscale, never upscale)
WIDTH=$(identify -format "%w" "$INPUT")
if [ $WIDTH -gt $PRINT_WIDTH ]; then
  convert "$INPUT" -resize ${PRINT_WIDTH}x -density 300 "${OUTPUT_DIR}/$(basename $INPUT)"
else
  # Just set DPI metadata
  convert "$INPUT" -density 300 "${OUTPUT_DIR}/$(basename $INPUT)"
fi

echo "Optimized for print: ${OUTPUT_DIR}"
identify -verbose "${OUTPUT_DIR}/$(basename $INPUT)" | grep -E "Geometry|Resolution|Filesize"
```

### Workflow 3: Both Web and Print

```bash
#!/bin/bash
# optimize-both.sh

INPUT=$1
BASE_NAME=$(basename ${INPUT%.*})
mkdir -p optimized/{web,print,original}

# Preserve original
cp "$INPUT" "optimized/original/${BASE_NAME}-original.png"

# Web version
convert "$INPUT" -resize 1600x -strip temp.png
pngquant --quality=65-80 temp.png --ext .png --force
mv temp.png "optimized/web/${BASE_NAME}-web.png"
cwebp -q 80 "optimized/web/${BASE_NAME}-web.png" -o "optimized/web/${BASE_NAME}-web.webp"

# Print version
convert "$INPUT" -resize 1500x -density 300 "optimized/print/${BASE_NAME}-print.png"

echo "Optimization complete:"
echo "Web: $(du -h optimized/web/${BASE_NAME}-web.png | cut -f1)"
echo "WebP: $(du -h optimized/web/${BASE_NAME}-web.webp | cut -f1)"
echo "Print: $(du -h optimized/print/${BASE_NAME}-print.png | cut -f1)"
```

### Workflow 4: Batch Process All Images

```bash
#!/bin/bash
# batch-optimize.sh

INPUT_DIR=${1:-.}
OUTPUT_DIR="optimized"

mkdir -p "${OUTPUT_DIR}"/{web,print,original}

for img in "${INPUT_DIR}"/*.{png,jpg,jpeg}; do
  [ -f "$img" ] || continue

  echo "Processing: $(basename $img)"

  base=$(basename "${img%.*}")
  ext="${img##*.}"

  # Original
  cp "$img" "${OUTPUT_DIR}/original/${base}.${ext}"

  # Web
  convert "$img" -resize 1600x -strip temp.png
  pngquant --quality=65-80 temp.png --ext .png --force 2>/dev/null || mv temp.png "${OUTPUT_DIR}/web/${base}.png"
  [ -f temp.png ] && mv temp.png "${OUTPUT_DIR}/web/${base}.png"

  # WebP
  cwebp -q 80 "${OUTPUT_DIR}/web/${base}.png" -o "${OUTPUT_DIR}/web/${base}.webp" 2>/dev/null

  # Print
  convert "$img" -resize 1500x -density 300 "${OUTPUT_DIR}/print/${base}.png"

  echo "✓ Optimized: $(basename $img)"
done

echo ""
echo "Summary:"
echo "Total images: $(ls ${INPUT_DIR}/*.{png,jpg,jpeg} 2>/dev/null | wc -l)"
echo "Web folder: $(du -sh ${OUTPUT_DIR}/web | cut -f1)"
echo "Print folder: $(du -sh ${OUTPUT_DIR}/print | cut -f1)"
```

**Usage:**

```bash
chmod +x batch-optimize.sh
./batch-optimize.sh ./screenshots
```

## Common Pitfalls to Avoid

**❌ Over-compression:**

```bash
convert input.png -quality 50 output.jpg  # Too aggressive
```

✅ **Balanced compression:**

```bash
convert input.png -quality 85 output.jpg  # Good quality/size ratio
```

**❌ Upscaling low-resolution images:**

```bash
# 800px image upscaled to 1600px - looks bad
convert small.png -resize 1600x output.png
```

✅ **Recapture at higher resolution:**

```bash
# Recapture original screenshot at 1600px+
```

**❌ Wrong format for content:**

```bash
# PNG for photo (huge file size)
# JPEG for UI screenshot (compression artifacts)
```

✅ **Appropriate format:**

```bash
# PNG for UI/text
# JPEG for photos
# WebP for modern web
```

**❌ Not preserving originals:**

```bash
# Overwriting original
convert input.png -resize 800x input.png
```

✅ **Keep originals:**

```bash
# Output to different file
convert input.png -resize 800x output.png
```

**❌ Inconsistent dimensions:**

```bash
# Different sizes for similar images
image1.png: 1400px
image2.png: 1800px
image3.png: 1600px
```

✅ **Standardized dimensions:**

```bash
# All screenshots at 1600px
```

## Next Steps

After optimizing images:

1. Run `execute-checklist.md` with `screenshot-quality-checklist.md`
2. Insert optimized images into chapter manuscript
3. Test web page load times
4. Verify print quality with test print
5. Update image inventory with file locations
6. Archive original high-resolution versions
7. Document optimization settings for future consistency
