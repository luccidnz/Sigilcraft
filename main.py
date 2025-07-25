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

    # Create ultra-complex cosmic background with fractal noise
    numerology_colors = {
        1: (60, 20, 120), 2: (120, 40, 180), 3: (80, 140, 60), 4: (180, 120, 60),
        5: (120, 180, 60), 6: (60, 180, 120), 7: (180, 60, 120), 8: (120, 60, 180),
        9: (180, 120, 180), 11: (255, 200, 255), 22: (255, 255, 200), 33: (200, 255, 255)
    }

    base_colors = numerology_colors.get(numerology_value, (60, 20, 120))

    # Create multi-dimensional background with fractal complexity
    for y in range(size * 2):
        for x in range(size * 2):
            # Multiple distance calculations for layered effects
            dist = math.sqrt((x - center[0])**2 + (y - center[1])**2)
            max_dist = math.sqrt(2) * size
            
            # Fractal noise layers
            fractal1 = math.sin(x * 0.02) * math.cos(y * 0.02)
            fractal2 = math.sin(x * 0.05 + y * 0.03) * math.cos(x * 0.03 - y * 0.05)
            fractal3 = math.sin(dist * 0.008) * math.cos(dist * 0.012)
            
            # Cosmic interference patterns
            cosmic1 = math.sin(math.sqrt(x**2 + y**2) * 0.01 + numerology_value)
            cosmic2 = math.cos(math.atan2(y - center[1], x - center[0]) * numerology_value)
            cosmic3 = math.sin((x + y) * 0.015 + numerology_value * math.pi)
            
            # Energy vortex calculations
            angle = math.atan2(y - center[1], x - center[0])
            vortex_strength = 1.0 / (1.0 + dist / (size * 0.3))
            vortex1 = math.sin(angle * numerology_value + dist * 0.01) * vortex_strength
            vortex2 = math.cos(angle * (numerology_value + 3) - dist * 0.008) * vortex_strength
            
            # Multi-layered gradient with extreme complexity
            gradient_factor = 1 - (dist / max_dist)
            
            # Combine all effects
            total_r = base_colors[0] + gradient_factor * 100 + 80 * fractal1 + 60 * cosmic1 + 40 * vortex1
            total_g = base_colors[1] + gradient_factor * 120 + 90 * fractal2 + 70 * cosmic2 + 50 * vortex2
            total_b = base_colors[2] + gradient_factor * 140 + 100 * fractal3 + 80 * cosmic3 + 60 * (vortex1 + vortex2) * 0.5
            
            # Add cosmic sparkle with fractal distribution
            cosmic_noise = hash((x * numerology_value, y * numerology_value, int(dist))) % 512
            if cosmic_noise > 480:
                sparkle_intensity = (cosmic_noise - 480) * 8
                total_r += sparkle_intensity
                total_g += sparkle_intensity * 1.2
                total_b += sparkle_intensity * 1.5
            
            # Add aurora-like wave effects
            aurora_wave = math.sin(y * 0.02 + x * 0.01 + numerology_value) * math.cos(x * 0.015 - y * 0.025)
            if aurora_wave > 0.7:
                aurora_intensity = (aurora_wave - 0.7) * 200
                total_r += aurora_intensity * 0.8
                total_g += aurora_intensity * 1.2
                total_b += aurora_intensity * 0.6
            
            # Clamp and apply colors
            r = max(0, min(255, int(total_r)))
            g = max(0, min(255, int(total_g)))
            b = max(0, min(255, int(total_b)))

            img.putpixel((x, y), (r, g, b, 255))

    # Add quantum energy fields
    create_quantum_fields(draw, center, size, numerology_value, original_phrase)
    
    # Create dimensional portals
    create_dimensional_portals(draw, center, size, numerology_value)

    # Create sacred geometry foundation with fractal complexity
    create_sacred_geometry(draw, center, size, numerology_value)

    # Add chaos grid for raw energy
    create_chaos_grid(draw, center, size, original_phrase)

    # Add multi-dimensional spiral energy flows
    create_spiral_energy(draw, center, size, 1)  # Clockwise
    create_spiral_energy(draw, center, size, -1)  # Counter-clockwise
    create_fractal_spirals(draw, center, size, numerology_value)

    # Add enhanced mystical circles and energy patterns
    draw_mystical_circles(draw, center, size, numerology_value)

    # Replace simple triangles with complex sacred geometry patterns
    draw_sacred_geometry(draw, center, size, numerology_value)
    
    # Add cosmic constellation patterns
    draw_cosmic_constellations(draw, center, size, numerology_value, original_phrase)

    # Add central mystical mandala with numerological significance
    draw_central_mandala(draw, center, size, numerology_value)
    
    # Add energy vortex overlay
    create_energy_vortex(draw, center, size, numerology_value)

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

def create_quantum_fields(draw, center, size, numerology_value, phrase):
    """Create quantum energy field effects"""
    field_intensity = len(phrase) % 5 + 3
    
    for field_layer in range(field_intensity):
        field_radius = size * (0.9 - field_layer * 0.15)
        
        # Create quantum particle effects
        particle_count = numerology_value * 8 + field_layer * 12
        
        for particle in range(particle_count):
            # Quantum uncertainty in positioning
            base_angle = (2 * math.pi * particle) / particle_count + field_layer * 0.3
            uncertainty_x = (hash(phrase + str(particle)) % 40 - 20) * 0.01 * size
            uncertainty_y = (hash(phrase + str(particle * 2)) % 40 - 20) * 0.01 * size
            
            x = center[0] + field_radius * math.cos(base_angle) + uncertainty_x
            y = center[1] + field_radius * math.sin(base_angle) + uncertainty_y
            
            # Quantum energy visualization
            energy_level = (particle + numerology_value + field_layer) % 7
            
            if energy_level >= 5:  # High energy particles
                particle_size = 8 - field_layer
                energy_color = (255, 200 + energy_level * 8, 100 + energy_level * 20, 180)
                
                # Create energy burst
                for burst in range(6):
                    burst_angle = base_angle + (burst * math.pi / 3)
                    burst_x = x + particle_size * 2 * math.cos(burst_angle)
                    burst_y = y + particle_size * 2 * math.sin(burst_angle)
                    
                    draw.line([x, y, burst_x, burst_y], fill=energy_color, width=2)
                
                draw.ellipse([x - particle_size, y - particle_size, 
                            x + particle_size, y + particle_size], fill=energy_color)
            
            elif energy_level >= 3:  # Medium energy
                particle_size = 5 - field_layer
                energy_color = (150 + energy_level * 15, 255, 180 + energy_level * 10, 150)
                draw.ellipse([x - particle_size, y - particle_size, 
                            x + particle_size, y + particle_size], fill=energy_color)
            
            else:  # Low energy field distortion
                distortion_size = 3
                energy_color = (100 + energy_level * 25, 100 + energy_level * 30, 255, 100)
                draw.ellipse([x - distortion_size, y - distortion_size, 
                            x + distortion_size, y + distortion_size], fill=energy_color)

def create_dimensional_portals(draw, center, size, numerology_value):
    """Create dimensional portal effects"""
    portal_count = min(4, max(2, numerology_value // 3))
    
    for portal_idx in range(portal_count):
        # Position portals around the sigil
        portal_angle = (2 * math.pi * portal_idx) / portal_count + (numerology_value * 0.1)
        portal_distance = size * (0.6 + portal_idx * 0.1)
        
        portal_x = center[0] + portal_distance * math.cos(portal_angle)
        portal_y = center[1] + portal_distance * math.sin(portal_angle)
        
        # Create portal layers
        for layer in range(8):
            layer_radius = size * (0.08 - layer * 0.008)
            layer_alpha = 200 - layer * 20
            
            # Portal color shifts through dimensions
            dimension_hue = (portal_idx * 90 + layer * 30 + numerology_value * 20) % 360
            
            portal_r = int(128 + 127 * math.sin(math.radians(dimension_hue)))
            portal_g = int(128 + 127 * math.sin(math.radians(dimension_hue + 120)))
            portal_b = int(128 + 127 * math.sin(math.radians(dimension_hue + 240)))
            
            portal_color = (portal_r, portal_g, portal_b, layer_alpha)
            
            # Draw portal ring
            draw.ellipse([portal_x - layer_radius, portal_y - layer_radius,
                         portal_x + layer_radius, portal_y + layer_radius], 
                        outline=portal_color, width=max(1, 4 - layer // 2))
            
            # Add dimensional sparks
            if layer % 2 == 0:
                spark_count = 12 - layer
                for spark in range(spark_count):
                    spark_angle = (2 * math.pi * spark) / spark_count + layer * 0.5
                    spark_x = portal_x + layer_radius * 1.2 * math.cos(spark_angle)
                    spark_y = portal_y + layer_radius * 1.2 * math.sin(spark_angle)
                    
                    spark_size = 2 + layer // 2
                    spark_color = (255, portal_g, portal_b, layer_alpha)
                    
                    draw.ellipse([spark_x - spark_size, spark_y - spark_size,
                                spark_x + spark_size, spark_y + spark_size], fill=spark_color)

def create_fractal_spirals(draw, center, size, numerology_value):
    """Create fractal spiral patterns"""
    spiral_count = numerology_value // 2 + 2
    
    for spiral_idx in range(spiral_count):
        spiral_start_angle = (spiral_idx * 360 / spiral_count) + (numerology_value * 15)
        spiral_direction = 1 if spiral_idx % 2 == 0 else -1
        
        # Create multi-level fractal spirals
        for fractal_level in range(3):
            spiral_radius = size * (0.1 + fractal_level * 0.15)
            spiral_width = max(1, 4 - fractal_level)
            
            points = []
            for angle_step in range(0, 720, 5):  # Two full rotations
                current_angle = spiral_start_angle + (angle_step * spiral_direction)
                
                # Fractal modification to radius
                fractal_modifier = 1 + 0.3 * math.sin(math.radians(angle_step * (fractal_level + 1)))
                current_radius = spiral_radius * fractal_modifier
                
                x = center[0] + current_radius * math.cos(math.radians(current_angle))
                y = center[1] + current_radius * math.sin(math.radians(current_angle))
                
                points.append((x, y))
                
                # Increase radius for spiral effect
                spiral_radius += size * 0.0008
            
            # Draw fractal spiral
            if len(points) > 1:
                for i in range(len(points) - 1):
                    color_shift = (i + fractal_level * 50 + spiral_idx * 30) % 255
                    spiral_color = (
                        150 + color_shift % 105,
                        100 + (color_shift * 2) % 155,
                        255,
                        120 - fractal_level * 30
                    )
                    
                    draw.line([points[i], points[i + 1]], fill=spiral_color, width=spiral_width)

def draw_cosmic_constellations(draw, center, size, numerology_value, phrase):
    """Draw cosmic constellation patterns based on phrase energy"""
    constellation_count = len(phrase) // 3 + 2
    
    for constellation_idx in range(constellation_count):
        # Create constellation anchor point
        constellation_angle = (2 * math.pi * constellation_idx) / constellation_count
        constellation_distance = size * (0.4 + (constellation_idx % 3) * 0.2)
        
        anchor_x = center[0] + constellation_distance * math.cos(constellation_angle)
        anchor_y = center[1] + constellation_distance * math.sin(constellation_angle)
        
        # Generate star pattern based on phrase hash
        star_count = (hash(phrase + str(constellation_idx)) % 8) + 5
        star_positions = []
        
        for star_idx in range(star_count):
            # Generate pseudo-random but deterministic star positions
            star_hash = hash(phrase + str(constellation_idx) + str(star_idx))
            
            local_angle = (star_hash % 360) * math.pi / 180
            local_distance = (star_hash % 50 + 20) * size * 0.002
            
            star_x = anchor_x + local_distance * math.cos(local_angle)
            star_y = anchor_y + local_distance * math.sin(local_angle)
            
            star_positions.append((star_x, star_y))
            
            # Draw star
            star_brightness = (star_hash % 3) + 2
            star_size = star_brightness + 1
            
            star_color = (
                200 + (star_hash % 55),
                180 + ((star_hash >> 8) % 75),
                255,
                150 + star_brightness * 20
            )
            
            # Draw star with radiating points
            for ray in range(8):
                ray_angle = ray * math.pi / 4
                ray_length = star_size * 3
                ray_x = star_x + ray_length * math.cos(ray_angle)
                ray_y = star_y + ray_length * math.sin(ray_angle)
                
                draw.line([star_x, star_y, ray_x, ray_y], fill=star_color, width=1)
            
            draw.ellipse([star_x - star_size, star_y - star_size,
                         star_x + star_size, star_y + star_size], fill=star_color)
        
        # Connect stars in constellation pattern
        if len(star_positions) > 2:
            for i in range(len(star_positions)):
                next_star = (i + 2) % len(star_positions)  # Skip one star for interesting patterns
                
                connection_color = (
                    100 + (constellation_idx * 30) % 155,
                    150 + (constellation_idx * 20) % 105,
                    200 + (constellation_idx * 40) % 55,
                    80
                )
                
                draw.line([star_positions[i], star_positions[next_star]], 
                         fill=connection_color, width=1)

def create_energy_vortex(draw, center, size, numerology_value):
    """Create swirling energy vortex overlay"""
    vortex_layers = 5
    
    for layer in range(vortex_layers):
        layer_radius = size * (0.8 - layer * 0.12)
        rotation_offset = layer * 30 + numerology_value * 10
        
        # Create vortex arms
        arm_count = 3 + (numerology_value % 4)
        
        for arm in range(arm_count):
            arm_angle = (360 / arm_count * arm) + rotation_offset
            
            # Create curved vortex arm
            arm_points = []
            for curve_step in range(20):
                step_ratio = curve_step / 19.0
                
                # Logarithmic spiral for vortex effect
                current_radius = layer_radius * (1 - step_ratio * 0.8)
                current_angle = arm_angle + (step_ratio * 180 * (layer + 1))
                
                # Add turbulence
                turbulence = math.sin(step_ratio * math.pi * 4) * size * 0.02
                
                x = center[0] + (current_radius + turbulence) * math.cos(math.radians(current_angle))
                y = center[1] + (current_radius + turbulence) * math.sin(math.radians(current_angle))
                
                arm_points.append((x, y))
            
            # Draw vortex arm with gradient effect
            for i in range(len(arm_points) - 1):
                point_intensity = 1 - (i / len(arm_points))
                
                vortex_color = (
                    int(255 * point_intensity),
                    int((150 + layer * 20) * point_intensity),
                    int((200 + numerology_value * 8) * point_intensity),
                    int((120 - layer * 15) * point_intensity)
                )
                
                line_width = max(1, int((6 - layer) * point_intensity))
                draw.line([arm_points[i], arm_points[i + 1]], fill=vortex_color, width=line_width)

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