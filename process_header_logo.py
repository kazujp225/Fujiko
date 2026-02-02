from PIL import Image

# Reload original image
img = Image.open('/Users/a3/Downloads/IMG_6768.jpg')
img = img.convert('RGBA')
data = img.getdata()

new_data = []
for item in data:
    r, g, b, a = item
    # Wide range blue background removal
    if (0 <= r <= 150) and (50 <= g <= 200) and (120 <= b <= 255):
        new_data.append((255, 255, 255, 0))
    # Also catch darker blues
    elif (0 <= r <= 80) and (30 <= g <= 120) and (80 <= b <= 180):
        new_data.append((255, 255, 255, 0))
    else:
        new_data.append(item)

img.putdata(new_data)
img.save('img/logo_header.png')
print('Done')
