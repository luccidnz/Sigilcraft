
import os
os.system("pip install flask pillow")

from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont
import string
import math
import io
import base64
import random

app = Flask(__name__)

def create_sigil(phrase, size=500):
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
    img = Image.new('RGBA', (size * 2, size * 2), color=(0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    center = (size, size)  # Center for 2x size

    # Create ultra-complex cosmic background with fractal noise
    numerology_colors = {
        1: (120, 40, 200), 2: (200, 60, 255), 3: (100, 255, 120), 4: (255, 180, 60),
        5: (180, 255, 100), 6: (60, 255, 200), 7: (255, 60, 180), 8: (180, 60, 255),
        9: (255, 180, 255), 11: (255, 220, 255), 22: (255, 255, 180), 33: (180, 255, 255)
    }

    base_colors = numerology_colors.get(numerology_value, (120, 40, 200))

    # Create multi-dimensional background with fractal complexity
    for y in range(size * 2):
        for x in range(size * 2):
            # Multiple distance calculations for layered effects
            dist = math.sqrt((x - center[0])**2 + (y - center[1])**2)
            max_dist = math.sqrt(2) * size
            
            # Enhanced fractal noise layers
            fractal1 = math.sin(x * 0.015) * math.cos(y * 0.018)
            fractal2 = math.sin(x * 0.035 + y * 0.028) * math.cos(x * 0.025 - y * 0.032)
            fractal3 = math.sin(dist * 0.012) * math.cos(dist * 0.008)
            
            # Cosmic interference patterns
            cosmic1 = math.sin(math.sqrt(x**2 + y**2) * 0.008 + numerology_value)
            cosmic2 = math.cos(math.atan2(y - center[1], x - center[0]) * numerology_value * 1.5)
            cosmic3 = math.sin((x + y) * 0.012 + numerology_value * math.pi)
            
            # Energy vortex calculations
            angle = math.atan2(y - center[1], x - center[0])
            vortex_strength = 1.0 / (1.0 + dist / (size * 0.4))
            vortex1 = math.sin(angle * numerology_value * 2 + dist * 0.015) * vortex_strength
            vortex2 = math.cos(angle * (numerology_value + 5) - dist * 0.012) * vortex_strength
            
            # Multi-layered gradient with extreme complexity
            gradient_factor = 1 - (dist / max_dist)
            
            # Combine all effects with enhanced intensity
            total_r = base_colors[0] + gradient_factor * 150 + 120 * fractal1 + 100 * cosmic1 + 80 * vortex1
            total_g = base_colors[1] + gradient_factor * 180 + 140 * fractal2 + 110 * cosmic2 + 90 * vortex2
            total_b = base_colors[2] + gradient_factor * 200 + 160 * fractal3 + 130 * cosmic3 + 100 * (vortex1 + vortex2) * 0.5
            
            # Add cosmic sparkle with fractal distribution
            cosmic_noise = hash((x * numerology_value, y * numerology_value, int(dist))) % 1000
            if cosmic_noise > 950:
                sparkle_intensity = (cosmic_noise - 950) * 10
                total_r += sparkle_intensity * 1.5
                total_g += sparkle_intensity * 1.8
                total_b += sparkle_intensity * 2.2
            
            # Add aurora-like wave effects
            aurora_wave = math.sin(y * 0.015 + x * 0.008 + numerology_value) * math.cos(x * 0.012 - y * 0.018)
            if aurora_wave > 0.6:
                aurora_intensity = (aurora_wave - 0.6) * 300
                total_r += aurora_intensity * 0.9
                total_g += aurora_intensity * 1.4
                total_b += aurora_intensity * 0.7
            
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

    # Add cosmic constellation patterns
    draw_cosmic_constellations(draw, center, size, numerology_value, original_phrase)

    # Add central mystical mandala with numerological significance
    draw_central_mandala(draw, center, size, numerology_value)
    
    # Add energy vortex overlay
    create_energy_vortex(draw, center, size, numerology_value)

    # Add crystalline matrix overlay
    create_crystalline_matrix(draw, center, size, numerology_value)
    
    # Add plasma energy effects
    create_plasma_effects(draw, center, size, numerology_value, original_phrase)

    # Drawing the letters with enhanced styling
    try:
        font = ImageFont.truetype("arial.ttf", max(12, size//25))
    except:
        font = ImageFont.load_default()

    radius = size * 0.4
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

        # Enhanced letter styling with glow effect
        letter_x = x - text_width//2
        letter_y = y - text_height//2
        
        # Draw glow effect
        for glow_offset in range(3, 0, -1):
            glow_alpha = 60 - glow_offset * 15
            glow_color = (255, 255, 255, glow_alpha)
            for dx in range(-glow_offset, glow_offset + 1):
                for dy in range(-glow_offset, glow_offset + 1):
                    if dx != 0 or dy != 0:
                        draw.text((letter_x + dx, letter_y + dy), letter, font=font, fill=glow_color)
        
        # Draw main letter
        draw.text((letter_x, letter_y), letter, font=font, fill=(255, 255, 255, 255))
        points.append((x, y))

    # Enhanced connecting lines with energy flow effect
    if len(points) > 1:
        for i in range(len(points)):
            start_point = points[i]
            end_point = points[(i + 1) % len(points)]
            
            # Draw multiple line layers for energy effect
            for line_layer in range(3):
                line_width = max(1, 6 - line_layer * 2)
                line_alpha = 255 - line_layer * 60
                line_color = (255, 100 + line_layer * 50, 100 + line_layer * 30, line_alpha)
                
                draw.line([start_point, end_point], fill=line_color, width=line_width)

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

def safe_ellipse(draw, coords, **kwargs):
    """Safe ellipse drawing with coordinate validation"""
    x1, y1, x2, y2 = coords
    if x2 > x1 and y2 > y1:
        draw.ellipse([x1, y1, x2, y2], **kwargs)

def create_sacred_geometry(draw, center, size, numerology_value):
    # Draw complex sacred geometric patterns
    pattern_layers = min(5, 3 + (numerology_value // 3))

    for layer in range(pattern_layers):
        layer_radius = size * (0.85 - layer * 0.12)
        pattern_count = min(24, numerology_value + layer * 3)

        for i in range(pattern_count):
            angle = (2 * math.pi * i) / pattern_count + (layer * math.pi / 8)

            # Create sacred triangular forms
            triangle_size = size * max(0.05, 0.15 - layer * 0.025)

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
                    tri_color = (150 + color_shift % 105, 100 + (color_shift * 2) % 155, 255, min(255, 100 + layer * 20))

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
                diamond_color = (255, 150 + color_shift % 105, 100 + (color_shift * 2) % 155, min(255, 110 + layer * 15))
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
                poly_color = (100 + (color_shift * 3) % 155, 255, 150 + color_shift % 105, min(255, 105 + layer * 18))
                draw.polygon(poly_points, fill=poly_color)

def create_chaos_grid(draw, center, size, phrase):
    grid_density = 0.06
    chaos_intensity = 0.8
    phrase_hash = abs(hash(phrase)) % 1000000

    for i in range(int(size * grid_density)):
        x = (phrase_hash % size) + (i * (phrase_hash % 7 - 3)) * chaos_intensity
        y = ((phrase_hash >> 16) % size) + (i * ((phrase_hash >> 8) % 7 - 3)) * chaos_intensity

        x = (x % size) + size
        y = (y % size) + size

        line_length = size * 0.08
        angle = (phrase_hash % 360) + i * ((phrase_hash >> 24) % 30 - 15)

        end_x = x + line_length * math.cos(math.radians(angle))
        end_y = y + line_length * math.sin(math.radians(angle))

        line_color = (
            (phrase_hash % 155) + 100,
            ((phrase_hash >> 8) % 155) + 100,
            ((phrase_hash >> 16) % 155) + 100,
            80
        )

        draw.line([x, y, end_x, end_y], fill=line_color, width=2)

def create_spiral_energy(draw, center, size, direction=1):
    spiral_radius = size * 0.15
    num_spirals = 3
    spiral_width = 3

    for i in range(num_spirals):
        start_angle = i * 60
        end_angle = 900 + i * 60
        current_radius = spiral_radius

        for angle in range(start_angle, end_angle, 8):
            x = center[0] + current_radius * math.cos(math.radians(angle) * direction)
            y = center[1] + current_radius * math.sin(math.radians(angle) * direction)

            spiral_color = (
                150 + (angle % 105),
                (angle % 155) + 100,
                255,
                120
            )

            safe_ellipse(draw, [x - spiral_width, y - spiral_width, x + spiral_width, y + spiral_width], fill=spiral_color)
            current_radius += size * 0.0008

def draw_mystical_circles(draw, center, size, numerology_value):
    # Draw multiple mystical circles based on numerology
    circle_count = min(15, max(5, numerology_value * 2))
    outer_radius = size * 0.95

    for circle_idx in range(circle_count):
        circle_radius = outer_radius - (circle_idx * (size * 0.06))
        if circle_radius <= 10:
            break

        # Color shifts based on numerological energy
        base_hue = (numerology_value * 25 + circle_idx * 30) % 360
        r = int(150 + 100 * math.sin(math.radians(base_hue)))
        g = int(150 + 100 * math.sin(math.radians(base_hue + 120)))
        b = int(150 + 100 * math.sin(math.radians(base_hue + 240)))
        alpha = max(50, int(220 - circle_idx * 12))

        color = (r, g, b, alpha)

        # Draw circle with varying thickness
        thickness = max(1, 5 - circle_idx // 3)
        draw.ellipse([
            center[0] - circle_radius, center[1] - circle_radius,
            center[0] + circle_radius, center[1] + circle_radius
        ], outline=color, width=thickness)

        # Add energy nodes on circle
        if circle_idx % 2 == 0:
            node_count = min(36, numerology_value * 2 + circle_idx)
            for node in range(node_count):
                angle = (2 * math.pi * node) / node_count
                node_x = center[0] + circle_radius * math.cos(angle)
                node_y = center[1] + circle_radius * math.sin(angle)

                node_size = max(2, 5 - circle_idx // 2)
                node_color = (255, max(100, 255 - circle_idx * 15), max(50, 100 + circle_idx * 10), alpha)

                safe_ellipse(draw, [node_x - node_size, node_y - node_size, node_x + node_size, node_y + node_size], fill=node_color)

def create_quantum_fields(draw, center, size, numerology_value, phrase):
    """Create quantum energy field effects with safe coordinates"""
    field_intensity = min(8, len(phrase) % 6 + 4)
    
    for field_layer in range(field_intensity):
        field_radius = size * max(0.1, 0.9 - field_layer * 0.12)
        
        # Create quantum particle effects
        particle_count = min(100, numerology_value * 6 + field_layer * 8)
        
        for particle in range(particle_count):
            # Quantum uncertainty in positioning
            base_angle = (2 * math.pi * particle) / particle_count + field_layer * 0.4
            uncertainty_x = (abs(hash(phrase + str(particle))) % 40 - 20) * 0.008 * size
            uncertainty_y = (abs(hash(phrase + str(particle * 3))) % 40 - 20) * 0.008 * size
            
            x = center[0] + field_radius * math.cos(base_angle) + uncertainty_x
            y = center[1] + field_radius * math.sin(base_angle) + uncertainty_y
            
            # Quantum energy visualization
            energy_level = (particle + numerology_value + field_layer) % 8
            
            if energy_level >= 6:  # High energy particles
                particle_size = max(2, 10 - field_layer)
                energy_color = (255, min(255, 200 + energy_level * 7), min(255, 100 + energy_level * 15), 200)
                
                # Create energy burst
                for burst in range(8):
                    burst_angle = base_angle + (burst * math.pi / 4)
                    burst_x = x + particle_size * 3 * math.cos(burst_angle)
                    burst_y = y + particle_size * 3 * math.sin(burst_angle)
                    
                    draw.line([x, y, burst_x, burst_y], fill=energy_color, width=2)
                
                safe_ellipse(draw, [x - particle_size, y - particle_size, x + particle_size, y + particle_size], fill=energy_color)
            
            elif energy_level >= 4:  # Medium energy
                particle_size = max(1, 7 - field_layer)
                energy_color = (min(255, 150 + energy_level * 12), 255, min(255, 180 + energy_level * 8), 180)
                safe_ellipse(draw, [x - particle_size, y - particle_size, x + particle_size, y + particle_size], fill=energy_color)
            
            else:  # Low energy field distortion
                distortion_size = max(1, 4 - field_layer)
                energy_color = (min(255, 100 + energy_level * 20), min(255, 100 + energy_level * 25), 255, 130)
                safe_ellipse(draw, [x - distortion_size, y - distortion_size, x + distortion_size, y + distortion_size], fill=energy_color)

def create_dimensional_portals(draw, center, size, numerology_value):
    """Create dimensional portal effects with safe coordinates"""
    portal_count = min(6, max(3, numerology_value // 2))
    
    for portal_idx in range(portal_count):
        # Position portals around the sigil
        portal_angle = (2 * math.pi * portal_idx) / portal_count + (numerology_value * 0.15)
        portal_distance = size * (0.5 + portal_idx * 0.08)
        
        portal_x = center[0] + portal_distance * math.cos(portal_angle)
        portal_y = center[1] + portal_distance * math.sin(portal_angle)
        
        # Create portal layers
        for layer in range(10):
            layer_radius = max(5, size * (0.12 - layer * 0.01))
            layer_alpha = max(30, 240 - layer * 20)
            
            # Portal color shifts through dimensions
            dimension_hue = (portal_idx * 60 + layer * 25 + numerology_value * 15) % 360
            
            portal_r = int(128 + 127 * math.sin(math.radians(dimension_hue)))
            portal_g = int(128 + 127 * math.sin(math.radians(dimension_hue + 120)))
            portal_b = int(128 + 127 * math.sin(math.radians(dimension_hue + 240)))
            
            portal_color = (portal_r, portal_g, portal_b, layer_alpha)
            
            # Draw portal ring
            draw.ellipse([portal_x - layer_radius, portal_y - layer_radius,
                         portal_x + layer_radius, portal_y + layer_radius], 
                        outline=portal_color, width=max(1, 5 - layer // 2))
            
            # Add dimensional sparks
            if layer % 2 == 0:
                spark_count = max(6, 15 - layer)
                for spark in range(spark_count):
                    spark_angle = (2 * math.pi * spark) / spark_count + layer * 0.6
                    spark_distance = layer_radius * 1.3
                    spark_x = portal_x + spark_distance * math.cos(spark_angle)
                    spark_y = portal_y + spark_distance * math.sin(spark_angle)
                    
                    spark_size = max(1, 3 + layer // 3)
                    spark_color = (255, portal_g, portal_b, layer_alpha)
                    
                    safe_ellipse(draw, [spark_x - spark_size, spark_y - spark_size, spark_x + spark_size, spark_y + spark_size], fill=spark_color)

def create_fractal_spirals(draw, center, size, numerology_value):
    """Create fractal spiral patterns with safe coordinates"""
    spiral_count = min(8, numerology_value // 2 + 3)
    
    for spiral_idx in range(spiral_count):
        spiral_start_angle = (spiral_idx * 360 / spiral_count) + (numerology_value * 12)
        spiral_direction = 1 if spiral_idx % 2 == 0 else -1
        
        # Create multi-level fractal spirals
        for fractal_level in range(4):
            spiral_radius = size * max(0.05, 0.12 + fractal_level * 0.08)
            spiral_width = max(1, 5 - fractal_level)
            
            points = []
            for angle_step in range(0, 900, 6):  # Multiple rotations
                current_angle = spiral_start_angle + (angle_step * spiral_direction)
                
                # Fractal modification to radius
                fractal_modifier = 1 + 0.25 * math.sin(math.radians(angle_step * (fractal_level + 1)))
                current_radius = spiral_radius * fractal_modifier
                
                x = center[0] + current_radius * math.cos(math.radians(current_angle))
                y = center[1] + current_radius * math.sin(math.radians(current_angle))
                
                points.append((x, y))
                
                # Increase radius for spiral effect
                spiral_radius += size * 0.0006
            
            # Draw fractal spiral
            if len(points) > 1:
                for i in range(len(points) - 1):
                    color_shift = (i + fractal_level * 40 + spiral_idx * 25) % 255
                    spiral_color = (
                        min(255, 150 + color_shift % 105),
                        min(255, 100 + (color_shift * 2) % 155),
                        255,
                        max(60, 150 - fractal_level * 25)
                    )
                    
                    draw.line([points[i], points[i + 1]], fill=spiral_color, width=spiral_width)

def draw_cosmic_constellations(draw, center, size, numerology_value, phrase):
    """Draw cosmic constellation patterns with safe coordinates"""
    constellation_count = min(8, len(phrase) // 2 + 3)
    
    for constellation_idx in range(constellation_count):
        # Create constellation anchor point
        constellation_angle = (2 * math.pi * constellation_idx) / constellation_count
        constellation_distance = size * (0.3 + (constellation_idx % 4) * 0.15)
        
        anchor_x = center[0] + constellation_distance * math.cos(constellation_angle)
        anchor_y = center[1] + constellation_distance * math.sin(constellation_angle)
        
        # Generate star pattern based on phrase hash
        star_count = min(12, (abs(hash(phrase + str(constellation_idx))) % 8) + 6)
        star_positions = []
        
        for star_idx in range(star_count):
            # Generate pseudo-random but deterministic star positions
            star_hash = abs(hash(phrase + str(constellation_idx) + str(star_idx)))
            
            local_angle = (star_hash % 360) * math.pi / 180
            local_distance = (star_hash % 40 + 15) * size * 0.003
            
            star_x = anchor_x + local_distance * math.cos(local_angle)
            star_y = anchor_y + local_distance * math.sin(local_angle)
            
            star_positions.append((star_x, star_y))
            
            # Draw star
            star_brightness = (star_hash % 4) + 2
            star_size = max(1, star_brightness)
            
            star_color = (
                min(255, 200 + (star_hash % 55)),
                min(255, 180 + ((star_hash >> 8) % 75)),
                255,
                min(255, 150 + star_brightness * 15)
            )
            
            # Draw star with radiating points
            for ray in range(8):
                ray_angle = ray * math.pi / 4
                ray_length = star_size * 4
                ray_x = star_x + ray_length * math.cos(ray_angle)
                ray_y = star_y + ray_length * math.sin(ray_angle)
                
                draw.line([star_x, star_y, ray_x, ray_y], fill=star_color, width=1)
            
            safe_ellipse(draw, [star_x - star_size, star_y - star_size, star_x + star_size, star_y + star_size], fill=star_color)
        
        # Connect stars in constellation pattern
        if len(star_positions) > 2:
            for i in range(len(star_positions)):
                next_star = (i + 2) % len(star_positions)  # Skip one star for interesting patterns
                
                connection_color = (
                    min(255, 100 + (constellation_idx * 25) % 155),
                    min(255, 150 + (constellation_idx * 15) % 105),
                    min(255, 200 + (constellation_idx * 35) % 55),
                    100
                )
                
                draw.line([star_positions[i], star_positions[next_star]], 
                         fill=connection_color, width=1)

def create_energy_vortex(draw, center, size, numerology_value):
    """Create swirling energy vortex overlay with safe coordinates"""
    vortex_layers = 6
    
    for layer in range(vortex_layers):
        layer_radius = size * max(0.1, 0.8 - layer * 0.1)
        rotation_offset = layer * 25 + numerology_value * 8
        
        # Create vortex arms
        arm_count = min(8, 3 + (numerology_value % 5))
        
        for arm in range(arm_count):
            arm_angle = (360 / arm_count * arm) + rotation_offset
            
            # Create curved vortex arm
            arm_points = []
            for curve_step in range(25):
                step_ratio = curve_step / 24.0
                
                # Logarithmic spiral for vortex effect
                current_radius = layer_radius * (1 - step_ratio * 0.7)
                current_angle = arm_angle + (step_ratio * 150 * (layer + 1))
                
                # Add turbulence
                turbulence = math.sin(step_ratio * math.pi * 5) * size * 0.015
                
                x = center[0] + (current_radius + turbulence) * math.cos(math.radians(current_angle))
                y = center[1] + (current_radius + turbulence) * math.sin(math.radians(current_angle))
                
                arm_points.append((x, y))
            
            # Draw vortex arm with gradient effect
            for i in range(len(arm_points) - 1):
                point_intensity = 1 - (i / len(arm_points))
                
                vortex_color = (
                    int(min(255, 255 * point_intensity)),
                    int(min(255, (150 + layer * 15) * point_intensity)),
                    int(min(255, (200 + numerology_value * 6) * point_intensity)),
                    int(min(255, (140 - layer * 12) * point_intensity))
                )
                
                line_width = max(1, int((7 - layer) * point_intensity))
                draw.line([arm_points[i], arm_points[i + 1]], fill=vortex_color, width=line_width)

def draw_central_mandala(draw, center, size, numerology_value):
    """Draw central mandala with safe coordinates"""
    mandala_radius = size // 5

    # Draw multiple concentric patterns
    for mandala_layer in range(5):
        layer_radius = max(10, mandala_radius * (1 - mandala_layer * 0.18))

        # Sacred number-based pattern
        pattern_points = min(24, numerology_value * 2 + mandala_layer * 3)
        layer_points = []

        for i in range(pattern_points):
            angle = (2 * math.pi * i) / pattern_points + (mandala_layer * math.pi / 10)
            x = center[0] + layer_radius * math.cos(angle)
            y = center[1] + layer_radius * math.sin(angle)
            layer_points.append((x, y))

        # Connect points based on sacred ratios
        connection_step = max(1, pattern_points // max(1, numerology_value))

        for i in range(pattern_points):
            start_point = layer_points[i]
            end_point = layer_points[(i + connection_step) % pattern_points]

            # Color based on sacred number relationships
            color_intensity = min(255, 150 + (i * numerology_value) % 105)
            line_color = (
                min(255, 255 - mandala_layer * 30),
                color_intensity,
                min(255, 200 + mandala_layer * 10),
                max(60, 200 - mandala_layer * 25)
            )

            line_width = max(1, 6 - mandala_layer)
            draw.line([start_point, end_point], fill=line_color, width=line_width)

        # Add energy nodes at intersection points
        for point in layer_points[::2]:  # Every other point
            node_size = max(1, 5 - mandala_layer)
            node_color = (255, 255, 255, max(100, 220 - mandala_layer * 30))

            safe_ellipse(draw, [point[0] - node_size, point[1] - node_size, point[0] + node_size, point[1] + node_size], fill=node_color)

    # Central power symbol based on numerology
    if numerology_value in [11, 22, 33]:  # Master numbers get special treatment
        # Draw powerful central star
        master_points = []
        for i in range(12):
            angle = (2 * math.pi * i) / 12
            radius = mandala_radius * 0.25
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
        central_size = max(5, mandala_radius * 0.15)
        safe_ellipse(draw, [center[0] - central_size, center[1] - central_size, center[0] + central_size, center[1] + central_size], fill=(255, 255, 255, 240))

def create_crystalline_matrix(draw, center, size, numerology_value):
    """Create crystalline energy matrix overlay"""
    matrix_density = min(50, numerology_value * 4)
    
    for crystal_idx in range(matrix_density):
        # Position crystals in geometric pattern
        ring_level = crystal_idx // 8
        ring_position = crystal_idx % 8
        
        ring_radius = size * (0.2 + ring_level * 0.15)
        crystal_angle = (2 * math.pi * ring_position) / 8 + (ring_level * 0.3)
        
        crystal_x = center[0] + ring_radius * math.cos(crystal_angle)
        crystal_y = center[1] + ring_radius * math.sin(crystal_angle)
        
        # Create crystalline structure
        crystal_size = max(3, size * (0.02 - ring_level * 0.003))
        
        # Crystal facets
        facet_count = 6
        crystal_points = []
        
        for facet in range(facet_count):
            facet_angle = crystal_angle + (facet * 2 * math.pi / facet_count)
            facet_x = crystal_x + crystal_size * math.cos(facet_angle)
            facet_y = crystal_y + crystal_size * math.sin(facet_angle)
            crystal_points.append((facet_x, facet_y))
        
        # Crystal color based on position and numerology
        crystal_hue = (crystal_idx * 30 + numerology_value * 45) % 360
        crystal_r = int(200 + 55 * math.sin(math.radians(crystal_hue)))
        crystal_g = int(200 + 55 * math.sin(math.radians(crystal_hue + 120)))
        crystal_b = int(200 + 55 * math.sin(math.radians(crystal_hue + 240)))
        crystal_alpha = max(100, 200 - ring_level * 20)
        
        crystal_color = (crystal_r, crystal_g, crystal_b, crystal_alpha)
        
        # Draw crystal
        if len(crystal_points) >= 3:
            draw.polygon(crystal_points, fill=crystal_color, outline=(255, 255, 255, 150))
        
        # Crystal energy emanation
        for emanation in range(4):
            emanation_angle = crystal_angle + (emanation * math.pi / 2)
            emanation_length = crystal_size * 2
            emanation_x = crystal_x + emanation_length * math.cos(emanation_angle)
            emanation_y = crystal_y + emanation_length * math.sin(emanation_angle)
            
            emanation_color = (crystal_r, crystal_g, crystal_b, crystal_alpha // 2)
            draw.line([crystal_x, crystal_y, emanation_x, emanation_y], fill=emanation_color, width=1)

def create_plasma_effects(draw, center, size, numerology_value, phrase):
    """Create plasma energy effects"""
    plasma_intensity = len(phrase) % 7 + 5
    phrase_energy = abs(hash(phrase)) % 1000
    
    for plasma_layer in range(plasma_intensity):
        plasma_radius = size * (0.7 - plasma_layer * 0.08)
        
        # Plasma tendrils
        tendril_count = min(16, numerology_value + plasma_layer * 2)
        
        for tendril in range(tendril_count):
            base_angle = (2 * math.pi * tendril) / tendril_count + (plasma_layer * 0.4)
            
            # Create plasma tendril path
            tendril_points = []
            current_radius = plasma_radius * 0.3
            
            for step in range(15):
                step_ratio = step / 14.0
                
                # Plasma distortion
                distortion = math.sin(step_ratio * math.pi * 3 + phrase_energy * 0.01) * size * 0.02
                
                current_angle = base_angle + (step_ratio * math.pi * 0.5)
                
                x = center[0] + (current_radius + distortion) * math.cos(current_angle)
                y = center[1] + (current_radius + distortion) * math.sin(current_angle)
                
                tendril_points.append((x, y))
                current_radius += size * 0.015
            
            # Draw plasma tendril
            for i in range(len(tendril_points) - 1):
                plasma_intensity_factor = 1 - (i / len(tendril_points))
                
                plasma_hue = (tendril * 25 + plasma_layer * 40 + phrase_energy) % 360
                plasma_r = int(255 * plasma_intensity_factor)
                plasma_g = int((150 + 50 * math.sin(math.radians(plasma_hue))) * plasma_intensity_factor)
                plasma_b = int((200 + 55 * math.cos(math.radians(plasma_hue))) * plasma_intensity_factor)
                plasma_alpha = int((180 - plasma_layer * 15) * plasma_intensity_factor)
                
                plasma_color = (plasma_r, plasma_g, plasma_b, plasma_alpha)
                
                tendril_width = max(1, int(4 * plasma_intensity_factor))
                draw.line([tendril_points[i], tendril_points[i + 1]], fill=plasma_color, width=tendril_width)

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
