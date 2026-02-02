from PIL import Image
import os

source_path = "/Users/a3/.gemini/antigravity/brain/f5a8aec3-b90c-4148-b201-14bf12c02429/uploaded_media_1769842091763.png"
output_path = "/Users/a3/Desktop/藤子ちゃん/img/logo_white.png"

def extract_white_logo(src, dst):
    if not os.path.exists(src):
        print(f"Source not found: {src}")
        return

    img = Image.open(src).convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        # Check if white (high brightness)
        # item is (R, G, B, A)
        if item[0] > 200 and item[1] > 200 and item[2] > 200:
            # Keep as White
            new_data.append((255, 255, 255, 255))
        else:
            # Transparent
            new_data.append((255, 255, 255, 0)) # Masking other colors

    img.putdata(new_data)
    # Crop to content to remove excess transparent space
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    img.save(dst)
    print(f"Saved transparent logo to {dst}")

extract_white_logo(source_path, output_path)
