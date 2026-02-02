import os
from PIL import Image, ImageOps

output_dir = "/Users/a3/Desktop/藤子ちゃん/img"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Helper to save crop
def save_crop(img, bbox, path):
    cropped = img.crop(bbox)
    cropped.save(path)
    print(f"Saved {path}")

# 1. Process the Grid
grid_path = "/Users/a3/.gemini/antigravity/brain/f5a8aec3-b90c-4148-b201-14bf12c02429/logo_animation_grid_1769769485686.png"

if os.path.exists(grid_path):
    img = Image.open(grid_path).convert("RGBA")
    gray = img.convert("L")
    threshold = 200
    binary = gray.point(lambda p: 255 if p > threshold else 0)

    width, height = binary.size
    pixels = binary.load()
    visited = set()
    grid_objects = []

    for y in range(height):
        for x in range(width):
            if pixels[x, y] == 255 and (x, y) not in visited:
                min_x, max_x, min_y, max_y = x, x, y, y
                stack = [(x, y)]
                visited.add((x, y))
                while stack:
                    cx, cy = stack.pop()
                    min_x = min(min_x, cx)
                    max_x = max(max_x, cx)
                    min_y = min(min_y, cy)
                    max_y = max(max_y, cy)
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if pixels[nx, ny] == 255 and (nx, ny) not in visited:
                                visited.add((nx, ny))
                                stack.append((nx, ny))
                if (max_x - min_x) * (max_y - min_y) > 100:
                    grid_objects.append((min_x, min_y, max_x, max_y))

    # Sort
    rows = {}
    for obj in grid_objects:
        cy = (obj[1] + obj[3]) // 2
        found_row = False
        for ry in rows:
            if abs(ry - cy) < 50:
                rows[ry].append(obj)
                found_row = True
                break
        if not found_row:
            rows[cy] = [obj]

    sorted_objects = []
    for ry in sorted(rows.keys()):
        row_items = sorted(rows[ry], key=lambda o: o[0])
        sorted_objects.extend(row_items)

    for i, bbox in enumerate(sorted_objects[:5]):
        save_crop(img, bbox, os.path.join(output_dir, f"logo_new_icon_{i+1}.png"))
else:
    print("Grid image not found.")


# 2. Process the Text from logo_colored_1.png
logo_path = os.path.join(output_dir, "logo_colored_1.png")
if os.path.exists(logo_path):
    l_img = Image.open(logo_path).convert("RGBA")
    l_gray = l_img.convert("L")
    l_alpha = l_img.split()[3]
    l_binary = l_alpha.point(lambda p: 255 if p > 50 else 0)
    
    width, height = l_binary.size
    pixels = l_binary.load()
    visited = set()
    l_objects = []
    
    for y in range(height):
        for x in range(width):
            if pixels[x, y] == 255 and (x, y) not in visited:
                min_x, max_x, min_y, max_y = x, x, y, y
                stack = [(x, y)]
                visited.add((x, y))
                while stack:
                    cx, cy = stack.pop()
                    min_x, max_x, min_y, max_y = min(min_x, cx), max(max_x, cx), min(min_y, cy), max(max_y, cy)
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if pixels[nx, ny] == 255 and (nx, ny) not in visited:
                                visited.add((nx, ny))
                                stack.append((nx, ny))
                if (max_x - min_x) * (max_y - min_y) > 10:
                    l_objects.append((min_x, min_y, max_x, max_y))
    
    l_objects.sort(key=lambda o: o[0])
    
    if l_objects:
        if len(l_objects) > 1:
            text_objs = l_objects[1:]
            t_min_x = min(o[0] for o in text_objs)
            t_min_y = min(o[1] for o in text_objs)
            t_max_x = max(o[2] for o in text_objs)
            t_max_y = max(o[3] for o in text_objs)
            save_crop(l_img, (t_min_x, t_min_y, t_max_x, t_max_y), os.path.join(output_dir, "logo_text.png"))
            print("Separated text from logo.")
        else:
            print("Could not separate text (only 1 object found or text is connected to icon). Saving whole thing as text fallback.")
            l_img.save(os.path.join(output_dir, "logo_text.png"))
    else:
        print("No objects found in logo_colored_1.png")
