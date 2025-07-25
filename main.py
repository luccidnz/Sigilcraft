import os
os.system("pip install flask pillow")

from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont
import string
import math
import io
import base64

app = Flask(__name__)

def create_sigil(phrase, size=400):
    """Create a sigil image and return it as base64 encoded string"""
    original_phrase = phrase
    phrase = phrase.upper()
    phrase = ''.join([c for c in phrase if c in string.ascii_uppercase])
    phrase = ''.join(sorted(set(phrase), key=phrase.index))

    if not phrase:
        return None, "Please enter text with at least one letter"

    # Calculate numerological value
    numerology_value = calculate_numerology(original_phrase)

    # Create image with anti-aliasing
    img = Image.new('RGBA', (size * 2, size * 2), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center = (size, size)  # Center for 2x size

    # Create enhanced mystical gradient background based on numerology
    numerology_colors = {
        1: (40, 20, 80), 2: (80, 40, 120), 3: (60, 80, 40), 4: (120, 80, 40),
        5: (80, 120, 40), 6: (40, 120, 80), 7: (120, 40, 80), 8: (80, 40, 120),
        9: (120, 80, 120), 11: (200, 150, 255), 22: (255, 200, 150), 33: (150, 255, 200)
    }

    base_colors = numerology_colors.get(numerology_value, (40, 20, 80))

    for y in range(size * 2):
        for x in range(size * 2):
            # Distance from center for radial gradient
            dist = math.sqrt((x - center[0])**2 + (y - center[1])**2)
            max_dist = math.sqrt(2) * size

            # Multi-layered gradient with numerological influence
            gradient_factor = 1 - (dist / max_dist)

            # Sacred geometric wave influences
            wave1 = math.sin(dist * 0.01 * numerology_value)
            wave2 = math.cos(dist * 0.008 * numerology_value + math.pi/3)
            wave3 = math.sin(dist * 0.012 * numerology_value + math.pi/2)

            r = int(base_colors[0] + gradient_factor * 60 + 40 * wave1)
            g = int(base_colors[1] + gradient_factor * 80 + 50 * wave2)
            b = int(base_colors[2] + gradient_factor * 100 + 60 * wave3)

            # Add numerology-based sparkle effect
            noise = hash((x + numerology_value, y + numerology_value)) % 256
            sparkle_threshold = 255 - (numerology_value * 8)
            if noise > sparkle_threshold:
                intensity = (noise - sparkle_threshold) * 4
                r = min(255, r + intensity)
                g = min(255, g + intensity)
                b = min(255, b + intensity)

            img.putpixel((x, y), (r, g, b, 255))

    # Create sacred geometry foundation
    create_sacred_geometry(draw, center, size, numerology_value)

    # Add chaos grid for raw energy
    create_chaos_grid(draw, center, size, original_phrase)

    # Add spiral energy flows
    create_spiral_energy(draw, center, size, 1)  # Clockwise
    create_spiral_energy(draw, center, size, -1)  # Counter-clockwise

    # Add enhanced mystical circles and energy patterns
    draw_mystical_circles(draw, center, size, numerology_value)

    # Replace simple triangles with complex sacred geometry patterns
    draw_sacred_geometry(draw, center, size, numerology_value)

    # Add central mystical mandala with numerological significance
    draw_central_mandala(draw, center, size, numerology_value)

    # Drawing the letters as before, but with scaled down size
    try:
        font = ImageFont.truetype("arial.ttf", max(10, size//30))
    except:
        font = ImageFont.load_default()

    radius = size * 0.35
    angle_step = 360 / len(phrase)
    points = []

    for i, letter in enumerate(phrase):
        angle = math.radians(i * angle_step - 90)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)

        # Get text size for better centering
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        draw.text((x - text_width//2, y - text_height//2), letter, font=font, fill='white')
        points.append((x, y))

    if len(points) > 1:
        draw.line(points, fill='red', width=max(2, size//150))

    # Crop the image
    cropped_img = img.crop((0, 0, size * 2, size * 2))

    # Convert to base64
    img_buffer = io.BytesIO()
    cropped_img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

    return img_base64, None

def calculate_numerology(text):
    text = text.upper()
    total = 0
    for char in text:
        if 'A' <= char <= 'Z':
            total += ord(char) - ord('A') + 1
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(digit) for digit in str(total))
    return total

def create_sacred_geometry(draw, center, size, numerology_value):
    # Draw complex sacred geometric patterns
    pattern_layers = 3 + (numerology_value // 3)

    for layer in range(pattern_layers):
        layer_radius = size * (0.8 - layer * 0.15)
        pattern_count = numerology_value + layer * 2

        for i in range(pattern_count):
            angle = (2 * math.pi * i) / pattern_count + (layer * math.pi / 6)

            # Create sacred triangular forms
            triangle_size = size * (0.12 - layer * 0.02)

            # Base triangle point
            base_x = center[0] + layer_radius * math.cos(angle)
            base_y = center[1] + layer_radius * math.sin(angle)

            # Create various sacred shapes based on numerology
            if numerology_value % 3 == 0:  # Trinity-based patterns
                # Tri-point pattern
                for tri_point in range(3):
                    tri_angle = angle + (tri_point * 2 * math.pi / 3)
                    x1 = base_x + triangle_size * math.cos(tri_angle)
                    y1 = base_y + triangle_size * math.sin(tri_angle)
                    x2 = base_x + triangle_size * 0.6 * math.cos(tri_angle + 2.1)
                    y2 = base_y + triangle_size * 0.6 * math.sin(tri_angle + 2.1)
                    x3 = base_x + triangle_size * 0.6 * math.cos(tri_angle - 2.1)
                    y3 = base_y + triangle_size * 0.6 * math.sin(tri_angle - 2.1)

                    color_shift = (layer * 50 + i * 20) % 255
                    tri_color = (150 + color_shift % 105, 100 + (color_shift * 2) % 155, 255, 100 + layer * 20)

                    draw.polygon([(x1, y1), (x2, y2), (x3, y3)], fill=tri_color)

            elif numerology_value % 4 == 0:  # Square/stability patterns
                # Diamond patterns
                diamond_size = triangle_size * 0.8
                diamond_points = []
                for dp in range(4):
                    dp_angle = angle + (dp * math.pi / 2)
                    dp_x = base_x + diamond_size * math.cos(dp_angle)
                    dp_y = base_y + diamond_size * math.sin(dp_angle)
                    diamond_points.append((dp_x, dp_y))

                color_shift = (layer * 60 + i * 25) % 255
                diamond_color = (255, 150 + color_shift % 105, 100 + (color_shift * 2) % 155, 110 + layer * 15)
                draw.polygon(diamond_points, fill=diamond_color)

            else:  # Pentagonal/hexagonal patterns
                sides = 5 if numerology_value % 5 == 0 else 6
                poly_points = []
                for pp in range(sides):
                    pp_angle = angle + (pp * 2 * math.pi / sides)
                    pp_x = base_x + triangle_size * math.cos(pp_angle)
                    pp_y = base_y + triangle_size * math.sin(pp_angle)
                    poly_points.append((pp_x, pp_y))

                color_shift = (layer * 40 + i * 30) % 255
                poly_color = (100 + (color_shift * 3) % 155, 255, 150 + color_shift % 105, 105 + layer * 18)
                draw.polygon(poly_points, fill=poly_color)

def create_chaos_grid(draw, center, size, phrase):
    grid_density = 0.04
    chaos_intensity = 0.6
    phrase_hash = hash(phrase)

    for i in range(int(size * grid_density)):
        x = (phrase_hash % size) + (i * (phrase_hash % 5 - 2)) * chaos_intensity
        y = ((phrase_hash >> 16) % size) + (i * ((phrase_hash >> 8) % 5 - 2)) * chaos_intensity

        x = (x % size) + size
        y = (y % size) + size

        line_length = size * 0.05
        angle = (phrase_hash % 360) + i * ((phrase_hash >> 24) % 20 - 10)

        end_x = x + line_length * math.cos(math.radians(angle))
        end_y = y + line_length * math.sin(math.radians(angle))

        line_color = (
            (phrase_hash % 155) + 100,
            ((phrase_hash >> 8) % 155) + 100,
            ((phrase_hash >> 16) % 155) + 100,
            50
        )

        draw.line([x, y, end_x, end_y], fill=line_color, width=1)

def create_spiral_energy(draw, center, size, direction=1):
    spiral_radius = size * 0.25
    num_spirals = 2
    spiral_width = 2

    for i in range(num_spirals):
        start_angle = i * 45
        end_angle = 720 + i * 45

        for angle in range(start_angle, end_angle, 10):
            x = center[0] + spiral_radius * math.cos(math.radians(angle) * direction)
            y = center[1] + spiral_radius * math.sin(math.radians(angle) * direction)

            spiral_color = (
                100,
                (angle % 155) + 100,
                255,
                80
            )

            draw.ellipse([x - spiral_width, y - spiral_width, x + spiral_width, y + spiral_width], fill=spiral_color)

            spiral_radius += size * 0.0004

def draw_mystical_circles(draw, center, size, numerology_value):
    # Draw multiple mystical circles based on numerology
    circle_count = min(12, max(3, numerology_value))
    outer_radius = size * 0.95

    for circle_idx in range(circle_count):
        circle_radius = outer_radius - (circle_idx * (size * 0.08))
        progress = circle_idx / circle_count

        # Color shifts based on numerological energy
        base_hue = (numerology_value * 30 + circle_idx * 25) % 360
        r = int(150 + 100 * math.sin(math.radians(base_hue)))
        g = int(150 + 100 * math.sin(math.radians(base_hue + 120)))
        b = int(150 + 100 * math.sin(math.radians(base_hue + 240)))
        alpha = int(200 - circle_idx * 15)

        color = (r, g, b, alpha)

        # Draw circle with varying thickness
        thickness = max(1, 4 - circle_idx // 2)
        draw.ellipse([
            center[0] - circle_radius, center[1] - circle_radius,
            center[0] + circle_radius, center[1] + circle_radius
        ], outline=color, width=thickness)

        # Add energy nodes on circle
        if circle_idx % 2 == 0:
            node_count = numerology_value + circle_idx
            for node in range(node_count):
                angle = (2 * math.pi * node) / node_count
                node_x = center[0] + circle_radius * math.cos(angle)
                node_y = center[1] + circle_radius * math.sin(angle)

                node_size = 3 + circle_idx
                node_color = (255, 255 - circle_idx * 20, 100 + circle_idx * 15, alpha)

                draw.ellipse([
                    node_x - node_size, node_y - node_size,
                    node_x + node_size, node_y + node_size
                ], fill=node_color)

def draw_sacred_geometry(draw, center, size, numerology_value):
    # Draw complex sacred geometric patterns
    pattern_layers = 3 + (numerology_value // 3)

    for layer in range(pattern_layers):
        layer_radius = size * (0.8 - layer * 0.15)
        pattern_count = numerology_value + layer * 2

        for i in range(pattern_count):
            angle = (2 * math.pi * i) / pattern_count + (layer * math.pi / 6)

            # Create sacred triangular forms
            triangle_size = size * (0.12 - layer * 0.02)

            # Base triangle point
            base_x = center[0] + layer_radius * math.cos(angle)
            base_y = center[1] + layer_radius * math.sin(angle)

            # Create various sacred shapes based on numerology
            if numerology_value % 3 == 0:  # Trinity-based patterns
                # Tri-point pattern
                for tri_point in range(3):
                    tri_angle = angle + (tri_point * 2 * math.pi / 3)
                    x1 = base_x + triangle_size * math.cos(tri_angle)
                    y1 = base_y + triangle_size * math.sin(tri_angle)
                    x2 = base_x + triangle_size * 0.6 * math.cos(tri_angle + 2.1)
                    y2 = base_y + triangle_size * 0.6 * math.sin(tri_angle + 2.1)
                    x3 = base_x + triangle_size * 0.6 * math.cos(tri_angle - 2.1)
                    y3 = base_y + triangle_size * 0.6 * math.sin(tri_angle - 2.1)

                    color_shift = (layer * 50 + i * 20) % 255
                    tri_color = (150 + color_shift % 105, 100 + (color_shift * 2) % 155, 255, 100 + layer * 20)

                    draw.polygon([(x1, y1), (x2, y2), (x3, y3)], fill=tri_color)

            elif numerology_value % 4 == 0:  # Square/stability patterns
                # Diamond patterns
                diamond_size = triangle_size * 0.8
                diamond_points = []
                for dp in range(4):
                    dp_angle = angle + (dp * math.pi / 2)
                    dp_x = base_x + diamond_size * math.cos(dp_angle)
                    dp_y = base_y + diamond_size * math.sin(dp_angle)
                    diamond_points.append((dp_x, dp_y))

                color_shift = (layer * 60 + i * 25) % 255
                diamond_color = (255, 150 + color_shift % 105, 100 + (color_shift * 2) % 155, 110 + layer * 15)
                draw.polygon(diamond_points, fill=diamond_color)

            else:  # Pentagonal/hexagonal patterns
                sides = 5 if numerology_value % 5 == 0 else 6
                poly_points = []
                for pp in range(sides):
                    pp_angle = angle + (pp * 2 * math.pi / sides)
                    pp_x = base_x + triangle_size * math.cos(pp_angle)
                    pp_y = base_y + triangle_size * math.sin(pp_angle)
                    poly_points.append((pp_x, pp_y))

                color_shift = (layer * 40 + i * 30) % 255
                poly_color = (100 + (color_shift * 3) % 155, 255, 150 + color_shift % 105, 105 + layer * 18)
                draw.polygon(poly_points, fill=poly_color)

def draw_central_mandala(draw, center, size, numerology_value):
    # Add central mystical mandala based on numerology
    mandala_radius = size // 6

    # Draw multiple concentric patterns
    for mandala_layer in range(4):
        layer_radius = mandala_radius * (1 - mandala_layer * 0.2)

        # Sacred number-based pattern
        pattern_points = numerology_value + mandala_layer * 2
        layer_points = []

        for i in range(pattern_points):
            angle = (2 * math.pi * i) / pattern_points + (mandala_layer * math.pi / 8)
            x = center[0] + layer_radius * math.cos(angle)
            y = center[1] + layer_radius * math.sin(angle)
            layer_points.append((x, y))

        # Connect points based on sacred ratios
        connection_step = max(1, pattern_points // numerology_value)

        for i in range(pattern_points):
            start_point = layer_points[i]
            end_point = layer_points[(i + connection_step) % pattern_points]

            # Color based on sacred number relationships
            color_intensity = 150 + (i * numerology_value) % 105
            line_color = (
                255 - mandala_layer * 40,
                color_intensity,
                200 + mandala_layer * 15,
                180 - mandala_layer * 30
            )

            line_width = max(1, 5 - mandala_layer)
            draw.line([start_point, end_point], fill=line_color, width=line_width)

        # Add energy nodes at intersection points
        for point in layer_points[::2]:  # Every other point
            node_size = 4 - mandala_layer
            node_color = (255, 255, 255, 200 - mandala_layer * 40)

            draw.ellipse([
                point[0] - node_size, point[1] - node_size,
                point[0] + node_size, point[1] + node_size
            ], fill=node_color)

    # Central power symbol based on numerology
    if numerology_value in [11, 22, 33]:  # Master numbers get special treatment
        # Draw powerful central star
        master_points = []
        for i in range(12):
            angle = (2 * math.pi * i) / 12
            radius = mandala_radius * 0.3
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            master_points.append((x, y))

        # Connect in sacred pattern
        for i in range(12):
            start_point = master_points[i]
            end_point = master_points[(i + 5) % 12]  # Golden ratio approximation
            draw.line([start_point, end_point], fill=(255, 255, 255, 255), width=3)
    else:
        # Regular central symbol
        central_size = mandala_radius * 0.2
        draw.ellipse([
            center[0] - central_size, center[1] - central_size,
            center[0] + central_size, center[1] + central_size
        ], fill=(255, 255, 255, 220))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    phrase = data.get('phrase', '')

    if not phrase.strip():
        return jsonify({'error': 'Please enter your intent or desire'})

    img_base64, error = create_sigil(phrase.strip())

    if error:
        return jsonify({'error': error})

    return jsonify({'image': f'data:image/png;base64,{img_base64}'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)