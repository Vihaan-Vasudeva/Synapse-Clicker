from PIL import Image, ImageDraw

# Create a transparent canvas
size = 200
img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Body (soft peachy circle)
draw.ellipse([30, 30, 170, 170], fill="#F3C98A", outline="#D99B4E", width=6)

# Cute eyes
draw.ellipse([65, 80, 85, 100], fill="#4A2F18")   # left eye
draw.ellipse([115, 80, 135, 100], fill="#4A2F18") # right eye

# Little smile
draw.arc([75, 95, 125, 130], start=20, end=160, fill="#4A2F18", width=4)

# Blush cheeks
draw.ellipse([50, 105, 70, 120], fill="#F2A88A")
draw.ellipse([130, 105, 150, 120], fill="#F2A88A")

img.save("neuron.png")
print("Saved neuron.png!")