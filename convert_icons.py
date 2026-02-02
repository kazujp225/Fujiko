import os
from PIL import Image

output_dir = "/Users/a3/Desktop/藤子ちゃん/img"

# Helper: Extract color
def get_brand_color(image_path):
    if not os.path.exists(image_path):
        return (0, 0, 0, 255) # Fallback Black
    
    img = Image.open(image_path).convert("RGBA")
    pixels = img.load()
    w, h = img.size
    
    # Sample center-ish/scan for first non-transparent pixel
    for y in range(h):
        for x in range(w):
            if pixels[x, y][3] > 200:
                print(f"Sampled color: {pixels[x, y]}")
                return pixels[x, y]
    return (0, 0, 0, 255)

# logo_text_path = os.path.join(output_dir, "logo_text.png")
# brand_color = get_brand_color(logo_text_path)
brand_color = (59, 106, 160, 255) # Hardcoded Blue from CSS buttons

def make_transparent_colored(image_path, color):
    if not os.path.exists(image_path):
        print(f"Not found: {image_path}")
        return

    img = Image.open(image_path).convert("RGBA")
    gray = img.convert("L")
    new_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
    pixels = new_img.load()
    src_pixels = gray.load()
    
    width, height = img.size
    for y in range(height):
        for x in range(width):
            if src_pixels[x, y] > 200:
                # Use Brand Color
                pixels[x, y] = color
            else:
                pixels[x, y] = (0, 0, 0, 0)
                
    new_img.save(image_path)
    print(f"Converted {image_path} to brand color.")

# Process the icons
for i in range(1, 6):
    make_transparent_colored(os.path.join(output_dir, f"logo_new_icon_{i}.png"), brand_color)

# Check logo_text.png
# If it came from logo.png which was likely colored on transparent
# We don't need to change it, filters will handle it.
# But verify it exists.
if os.path.exists(os.path.join(output_dir, "logo_text.png")):
    print("logo_text.png exists.")
