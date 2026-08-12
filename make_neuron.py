from PIL import Image, ImageDraw
import math
import random

random.seed(7)  # keeps the dendrite branching consistent between runs

size = 400
img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

cx, cy = 190, 170  # soma center, slightly off-center to leave room for the axon tail

BODY = "#F3C98A"
OUTLINE = "#D99B4E"
NUCLEUS = "#D99B4E"
MYELIN = "#F2A88A"
AXON = "#E0AC6F"


def draw_branch(x, y, angle, length, width, depth):
    """Recursively draws a tapering dendrite branch that splits a couple times."""
    if depth == 0 or length < 8:
        return
    end_x = x + length * math.cos(angle)
    end_y = y + length * math.sin(angle)
    draw.line([(x, y), (end_x, end_y)], fill=OUTLINE, width=max(1, int(width)))

    # split into 2-3 smaller branches
    n_splits = random.choice([2, 2, 3])
    for _ in range(n_splits):
        spread = random.uniform(-0.6, 0.6)
        draw_branch(
            end_x, end_y,
            angle + spread,
            length * random.uniform(0.55, 0.75),
            width * 0.65,
            depth - 1,
        )


# dendrites fanning out from the top/sides of the soma (not the axon side)
soma_radius = 70
n_dendrites = 9
for i in range(n_dendrites):
    base_angle = math.pi * (1.15 + i * (1.7 / n_dendrites))  # roughly top half, avoids axon side
    start_x = cx + soma_radius * 0.9 * math.cos(base_angle)
    start_y = cy + soma_radius * 0.9 * math.sin(base_angle)
    draw_branch(start_x, start_y, base_angle, random.uniform(35, 55), 4, depth=3)

# soma (cell body)
draw.ellipse(
    [cx - soma_radius, cy - soma_radius, cx + soma_radius, cy + soma_radius],
    fill=BODY, outline=OUTLINE, width=6
)

# nucleus, off-center like a real cell diagram
draw.ellipse([cx - 22, cy - 10, cx + 18, cy + 30], fill=NUCLEUS)

# axon hillock -> axon running down-right off the soma
axon_start = (cx + 45, cy + 55)
axon_points = [axon_start]
x, y = axon_start
axon_angle = 0.95  # roughly down-right
for seg in range(5):
    x += random.uniform(28, 38) * math.cos(axon_angle)
    y += random.uniform(28, 38) * math.sin(axon_angle)
    axon_angle += random.uniform(-0.12, 0.12)
    axon_points.append((x, y))

draw.line(axon_points, fill=AXON, width=10, joint="curve")

# myelin sheath segments along the axon (little sausage shapes, classic textbook look)
for i in range(len(axon_points) - 1):
    x1, y1 = axon_points[i]
    x2, y2 = axon_points[i + 1]
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    seg_len = math.hypot(x2 - x1, y2 - y1) * 0.7
    angle = math.atan2(y2 - y1, x2 - x1)
    dx, dy = seg_len / 2 * math.cos(angle), seg_len / 2 * math.sin(angle)
    perp = 9
    px, py = perp * math.sin(angle), -perp * math.cos(angle)
    draw.ellipse(
        [mx - dx - abs(px), my - dy - abs(py), mx + dx + abs(px), my + dy + abs(py)],
        fill=MYELIN, outline=OUTLINE, width=2
    )

# axon terminals branching at the end, like little synapse fingers
term_x, term_y = axon_points[-1]
for i in range(4):
    angle = axon_angle + random.uniform(-0.7, 0.7)
    length = random.uniform(18, 28)
    end_x = term_x + length * math.cos(angle)
    end_y = term_y + length * math.sin(angle)
    draw.line([(term_x, term_y), (end_x, end_y)], fill=OUTLINE, width=3)
    draw.ellipse([end_x - 4, end_y - 4, end_x + 4, end_y + 4], fill=MYELIN, outline=OUTLINE, width=1)

img.save("neuron.png")
print("Saved neuron.png!")

#this is all ai generated