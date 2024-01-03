from PIL import Image

PALETTE_SIZE = 5
PALETTE_UPSCALE = 10
ACCURACY = 100  # 0-255

img = Image.open('test.jpg')

# Counting colors
pixels = {}
for x in range(img.width):
    for y in range(img.height):
        t = img.getpixel((x, y))
        if t not in pixels:
            pixels[t] = 1
        else:
            pixels[t] += 1

# Exclude pixels that occur once
filtered_pixels = {}
for key in pixels:
    if pixels[key] != 1:
        filtered_pixels[key] = pixels[key]

# Sort colors by frequency
pixels = list(dict(sorted(filtered_pixels.items(), key=lambda item: item[1])))
pixels.reverse()

# Create palette based on ACCURACY
palette = []
for p in pixels:
    contain_approximate_color = False
    for c in palette:
        if contain_approximate_color:
            break
        if abs(p[0] - c[0]) < ACCURACY and abs(p[1] - c[1]) < ACCURACY and abs(p[2] - c[2]) < ACCURACY:
            contain_approximate_color = True
    if not contain_approximate_color:
        palette.append(p)
        if len(palette) == PALETTE_SIZE:
            break

# Display the palette
img = Image.new("RGB", (PALETTE_SIZE, 1))
for idx, i in enumerate(palette):
    img.putpixel((idx, 0), i)
img = img.resize((img.width * PALETTE_UPSCALE, img.height * PALETTE_UPSCALE), Image.Resampling.NEAREST)

# Output
print(palette)
img.save("output.jpg")
img.show()
