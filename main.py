import os

os.system("pip install flask pillow")
from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import string
import math
import io
import base64
import random
import numpy as np

app = Flask(__name__)


def create_sigil(phrase, vibe="mystical", size=800):
    """Create a 3D sigil image and return it as base64 encoded string"""
    original_phrase = phrase
    phrase = phrase.upper()
    phrase = ''.join([c for c in phrase if c in string.ascii_uppercase])
    phrase = ''.join(sorted(set(phrase), key=phrase.index))

    if not phrase:
        return None, "Please enter text with at least one letter"

    # Calculate numerological value
    numerology_value = calculate_numerology(original_phrase)

    # Create unique seed based on entire phrase for consistent but unique randomness
    phrase_seed = abs(hash(original_phrase.lower())) % 2147483647
    random.seed(phrase_seed)

    # Create high-resolution image for 3D effects
    img = Image.new('RGBA', (size * 2, size * 2), color=(0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    center = (size, size)  # Center for 2x size

    # Create 3D depth layers and lighting system
    create_3d_background_layers(img, draw, center, size, numerology_value,
                                original_phrase, vibe)

    # Add 3D quantum energy fields with depth
    create_3d_quantum_fields(draw, center, size, numerology_value,
                             original_phrase)

    # Create 3D dimensional portals with perspective
    create_3d_dimensional_portals(draw, center, size, numerology_value)

    # Create 3D sacred geometry with depth and shadows
    create_3d_sacred_geometry(draw, center, size, numerology_value)

    # Add 3D chaos grid for raw energy with depth
    create_3d_chaos_grid(draw, center, size, original_phrase)

    # Add multi-dimensional 3D spiral energy flows
    create_3d_spiral_energy(draw, center, size, 1)  # Clockwise
    create_3d_spiral_energy(draw, center, size, -1)  # Counter-clockwise
    create_3d_fractal_spirals(draw, center, size, numerology_value)

    # Add enhanced 3D mystical circles with depth
    draw_3d_mystical_circles(draw, center, size, numerology_value)

    # Add 3D cosmic constellation patterns with perspective
    draw_3d_cosmic_constellations(draw, center, size, numerology_value,
                                  original_phrase)

    # Add central 3D mystical mandala with depth and lighting
    draw_3d_central_mandala(draw, center, size, numerology_value)

    # Add 3D energy vortex with perspective
    create_3d_energy_vortex(draw, center, size, numerology_value)

    # Add 3D crystalline matrix with depth and refraction
    create_3d_crystalline_matrix(draw, center, size, numerology_value)

    # Add 3D plasma energy effects with volume
    create_3d_plasma_effects(draw, center, size, numerology_value,
                             original_phrase)

    # Add atmospheric 3D lighting effects
    create_3d_atmospheric_lighting(draw, center, size, numerology_value)

    # Drawing the letters with 3D styling and depth
    draw_3d_letters(draw, center, size, phrase, numerology_value)

    # Apply 3D post-processing effects
    img = apply_3d_post_processing(img, size, numerology_value)

    # Crop the image
    cropped_img = img.crop((0, 0, size * 2, size * 2))

    # Convert to base64
    img_buffer = io.BytesIO()
    cropped_img.save(img_buffer, format='PNG', quality=95)
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


def create_3d_background_layers(img,
                                draw,
                                center,
                                size,
                                numerology_value,
                                original_phrase,
                                vibe="mystical"):
    """Create multi-layered 3D background with depth and atmospheric perspective"""
    phrase_seed = abs(hash(original_phrase.lower())) % 2147483647
    random.seed(phrase_seed)

    # 3D depth layers - far to near
    depth_layers = 8

    for depth in range(depth_layers):
        depth_factor = 1.0 - (depth / depth_layers)  # Far layers are smaller
        layer_opacity = int(
            255 *
            (0.3 + depth_factor * 0.7))  # Far layers are more transparent

        # Create perspective-corrected coordinates
        layer_size = int(size * 2 * (0.5 + depth_factor * 0.5))
        layer_offset_x = center[0] - layer_size // 2
        layer_offset_y = center[1] - layer_size // 2

        # 3D fractal noise with depth
        for y in range(max(0, layer_offset_y),
                       min(size * 2, layer_offset_y + layer_size)):
            for x in range(max(0, layer_offset_x),
                           min(size * 2, layer_offset_x + layer_size)):
                # 3D coordinate system
                x_3d = (x - center[0]) * (1.0 + depth * 0.1)
                y_3d = (y - center[1]) * (1.0 + depth * 0.1)
                z_3d = depth * size * 0.1

                dist_3d = math.sqrt(x_3d**2 + y_3d**2 + z_3d**2)

                # Multi-frequency 3D noise
                freq_base = 0.003 + (phrase_seed % 50) * 0.0001
                freq1 = freq_base * (1 + depth * 0.2)
                freq2 = freq_base * 2 * (1 + depth * 0.15)
                freq3 = freq_base * 0.5 * (1 + depth * 0.3)

                # 3D fractal calculations
                fractal_3d_1 = math.sin(x_3d * freq1) * math.cos(
                    y_3d * freq1) * math.sin(z_3d * freq1 * 0.1)
                fractal_3d_2 = math.sin(x_3d * freq2 + y_3d *
                                        freq2) * math.cos(z_3d * freq2 * 0.1)
                fractal_3d_3 = math.sin(dist_3d * freq3) * math.cos(
                    z_3d * freq3 * 0.2)

                # 3D lighting simulation
                light_source = (center[0] + size * 0.3, center[1] - size * 0.3,
                                size * 0.5)
                light_dist = math.sqrt((x - light_source[0])**2 +
                                       (y - light_source[1])**2 + z_3d**2)
                light_intensity = max(0.2,
                                      1.0 / (1.0 + light_dist / (size * 2)))

                # 3D atmospheric scattering
                atmospheric_factor = max(0.3, 1.0 - (z_3d / (size * 0.8)))

                # Color calculation with 3D depth
                base_colors = get_numerology_colors(numerology_value)
                vibe_colors = get_vibe_colors(vibe)
                vibe_color = vibe_colors[depth % len(vibe_colors)]

                total_r = (
                    base_colors[0] + vibe_color[0]
                ) * 0.5 * depth_factor + 180 * fractal_3d_1 * light_intensity * atmospheric_factor
                total_g = (
                    base_colors[1] + vibe_color[1]
                ) * 0.5 * depth_factor + 200 * fractal_3d_2 * light_intensity * atmospheric_factor
                total_b = (
                    base_colors[2] + vibe_color[2]
                ) * 0.5 * depth_factor + 220 * fractal_3d_3 * light_intensity * atmospheric_factor

                # Apply depth fog
                fog_factor = max(0.1, atmospheric_factor)
                total_r = total_r * fog_factor + (255 - total_r) * (
                    1 - fog_factor) * 0.3
                total_g = total_g * fog_factor + (255 - total_g) * (
                    1 - fog_factor) * 0.3
                total_b = total_b * fog_factor + (255 - total_b) * (
                    1 - fog_factor) * 0.3

                # Clamp colors
                r = max(0, min(255, int(total_r)))
                g = max(0, min(255, int(total_g)))
                b = max(0, min(255, int(total_b)))
                alpha = max(50, min(255, layer_opacity))

                # Blend with existing pixel
                current_pixel = img.getpixel((x, y))
                new_r = int(current_pixel[0] * (1 - alpha / 255) + r *
                            (alpha / 255))
                new_g = int(current_pixel[1] * (1 - alpha / 255) + g *
                            (alpha / 255))
                new_b = int(current_pixel[2] * (1 - alpha / 255) + b *
                            (alpha / 255))

                img.putpixel((x, y), (new_r, new_g, new_b, 255))


def get_numerology_colors(numerology_value):
    """Get base colors for numerological value"""
    numerology_colors = {
        1: (150, 60, 220),
        2: (220, 80, 255),
        3: (120, 255, 140),
        4: (255, 200, 80),
        5: (200, 255, 120),
        6: (80, 255, 220),
        7: (255, 80, 200),
        8: (200, 80, 255),
        9: (255, 200, 255),
        11: (255, 240, 255),
        22: (255, 255, 200),
        33: (200, 255, 255)
    }
    return numerology_colors.get(numerology_value, (150, 60, 220))


def get_vibe_colors(vibe):
    """Get color palette based on selected vibe"""
    vibe_palettes = {
        'mystical': [(150, 60, 220), (255, 100, 255), (120, 200, 255)],
        'cosmic': [(20, 20, 80), (100, 150, 255), (200, 100, 255),
                   (255, 200, 100)],
        'elemental': [(255, 100, 50), (50, 255, 100), (100, 150, 255),
                      (200, 150, 100)],
        'crystal': [(200, 255, 255), (150, 200, 255), (255, 200, 255),
                    (200, 255, 200)],
        'shadow': [(80, 20, 80), (120, 60, 120), (60, 20, 60), (100, 40, 100)],
        'light': [(255, 255, 200), (255, 200, 150), (200, 255, 200),
                  (255, 220, 255)]
    }
    return vibe_palettes.get(vibe, vibe_palettes['mystical'])


def create_3d_quantum_fields(draw, center, size, numerology_value, phrase):
    """Create 3D quantum energy fields with depth and particle effects"""
    phrase_hash = abs(hash(phrase)) % 1000000
    field_layers = min(12, (phrase_hash % 8) + 6)

    for field_layer in range(field_layers):
        # 3D positioning with perspective
        layer_depth = field_layer / field_layers
        perspective_scale = 0.4 + layer_depth * 0.6
        field_radius = size * (0.9 - field_layer * 0.06) * perspective_scale

        # 3D particle distribution
        particle_count = min(150, (phrase_hash % 60) + 30 + field_layer * 12)

        for particle in range(particle_count):
            # 3D spherical coordinates
            theta = (2 * math.pi *
                     particle) / particle_count + field_layer * 0.3
            phi = math.pi * (particle % 7) / 6  # Vertical distribution

            # 3D to 2D projection
            x_3d = field_radius * math.sin(phi) * math.cos(theta)
            y_3d = field_radius * math.sin(phi) * math.sin(theta)
            z_3d = field_radius * math.cos(phi)

            # Perspective projection
            perspective_factor = 1.0 / (1.0 + z_3d / (size * 0.5))
            x = center[0] + x_3d * perspective_factor
            y = center[1] + y_3d * perspective_factor

            # 3D lighting on particles
            light_angle = math.atan2(y_3d, x_3d)
            light_intensity = max(
                0.3, 0.7 + 0.3 * math.cos(light_angle - math.pi / 4))

            # Particle energy with 3D depth
            energy_level = (particle + numerology_value + field_layer) % 10
            particle_size = max(
                1,
                int((12 - field_layer) * perspective_factor * light_intensity))

            if energy_level >= 7:  # High energy 3D particles
                # Create 3D energy burst with depth
                burst_count = 12
                for burst in range(burst_count):
                    burst_angle_h = theta + (burst * 2 * math.pi / burst_count)
                    burst_angle_v = phi + (burst * math.pi / (burst_count * 2))

                    burst_x = x + particle_size * 4 * math.cos(
                        burst_angle_h) * perspective_factor
                    burst_y = y + particle_size * 4 * math.sin(
                        burst_angle_h) * math.sin(
                            burst_angle_v) * perspective_factor

                    energy_color = (int(255 * light_intensity),
                                    int(
                                        min(255, (220 + energy_level * 5) *
                                            light_intensity)),
                                    int(
                                        min(255, (120 + energy_level * 15) *
                                            light_intensity)),
                                    int(200 * perspective_factor))

                    draw.line([x, y, burst_x, burst_y],
                              fill=energy_color,
                              width=max(1, int(3 * perspective_factor)))

                particle_color = (int(255 * light_intensity),
                                  int(
                                      min(255, 200 + energy_level * 7) *
                                      light_intensity),
                                  int(
                                      min(255, 100 + energy_level * 15) *
                                      light_intensity),
                                  int(220 * perspective_factor))
                safe_ellipse(draw, [
                    x - particle_size, y - particle_size, x + particle_size,
                    y + particle_size
                ],
                             fill=particle_color)

            elif energy_level >= 4:  # Medium energy 3D particles
                particle_color = (int(
                    min(255, 170 + energy_level * 12) * light_intensity),
                                  int(255 * light_intensity),
                                  int(
                                      min(255, 200 + energy_level * 8) *
                                      light_intensity),
                                  int(180 * perspective_factor))

                # Add 3D glow effect
                glow_size = particle_size + 2
                glow_color = tuple(
                    list(particle_color[:3]) + [int(particle_color[3] * 0.5)])
                safe_ellipse(draw, [
                    x - glow_size, y - glow_size, x + glow_size, y + glow_size
                ],
                             fill=glow_color)
                safe_ellipse(draw, [
                    x - particle_size, y - particle_size, x + particle_size,
                    y + particle_size
                ],
                             fill=particle_color)


def create_3d_sacred_geometry(draw, center, size, numerology_value):
    """Create 3D sacred geometric patterns with depth, shadows and perspective"""
    phrase_hash = random.randint(1, 1000000)
    pattern_layers = min(8, 2 + (phrase_hash % 6) + (numerology_value // 3))

    for layer in range(pattern_layers):
        # 3D layer positioning with perspective
        layer_depth = layer / pattern_layers
        perspective_scale = 0.3 + layer_depth * 0.7
        layer_radius = size * (0.85 - layer * 0.08) * perspective_scale

        # Shadow offset based on 3D positioning
        shadow_offset_x = int(layer_depth * size * 0.02)
        shadow_offset_y = int(layer_depth * size * 0.02)

        pattern_count = min(
            48, 8 + (phrase_hash % 20) + layer * ((phrase_hash >> 8) % 6))

        for i in range(pattern_count):
            angle = (2 * math.pi * i) / pattern_count + (layer * math.pi / 10)

            # 3D sacred shapes with perspective
            shape_size = size * max(0.03,
                                    (0.18 - layer * 0.02) * perspective_scale)

            # Base position with 3D perspective
            base_x = center[0] + layer_radius * math.cos(angle)
            base_y = center[1] + layer_radius * math.sin(angle)

            # Draw shadow first for 3D depth
            shadow_color = (0, 0, 0, int(80 * perspective_scale))

            if numerology_value % 3 == 0:  # 3D Trinity patterns
                # 3D triangular pyramid projection
                for tri_point in range(3):
                    tri_angle = angle + (tri_point * 2 * math.pi / 3)
                    height_factor = math.sin(
                        tri_point * math.pi / 3) * perspective_scale

                    x1 = base_x + shape_size * math.cos(
                        tri_angle) + shadow_offset_x
                    y1 = base_y + shape_size * math.sin(
                        tri_angle) + shadow_offset_y
                    x2 = base_x + shape_size * 0.6 * math.cos(
                        tri_angle + 2.1) * height_factor + shadow_offset_x
                    y2 = base_y + shape_size * 0.6 * math.sin(
                        tri_angle + 2.1) * height_factor + shadow_offset_y
                    x3 = base_x + shape_size * 0.6 * math.cos(
                        tri_angle - 2.1) * height_factor + shadow_offset_x
                    y3 = base_y + shape_size * 0.6 * math.sin(
                        tri_angle - 2.1) * height_factor + shadow_offset_y

                    # Draw shadow
                    draw.polygon([(x1, y1), (x2, y2), (x3, y3)],
                                 fill=shadow_color)

                    # Draw 3D triangle with lighting
                    light_intensity = max(0.4, 0.7 + 0.3 * math.cos(tri_angle))
                    color_shift = (layer * 50 + i * 20) % 255
                    tri_color = (int((170 + color_shift % 85) *
                                     light_intensity * perspective_scale),
                                 int((120 + (color_shift * 2) % 135) *
                                     light_intensity * perspective_scale),
                                 int(255 * light_intensity *
                                     perspective_scale),
                                 int(
                                     min(255, 120 + layer * 15) *
                                     perspective_scale))

                    # Offset for 3D effect
                    x1 -= shadow_offset_x
                    y1 -= shadow_offset_y
                    x2 -= shadow_offset_x
                    y2 -= shadow_offset_y
                    x3 -= shadow_offset_x
                    y3 -= shadow_offset_y

                    draw.polygon([(x1, y1), (x2, y2), (x3, y3)],
                                 fill=tri_color)

            elif numerology_value % 4 == 0:  # 3D Cube/Diamond patterns
                # 3D diamond with perspective distortion
                diamond_points = []
                for dp in range(4):
                    dp_angle = angle + (dp * math.pi / 2)
                    depth_distortion = math.sin(dp_angle) * 0.3 + 0.7
                    dp_x = base_x + shape_size * math.cos(
                        dp_angle) * depth_distortion
                    dp_y = base_y + shape_size * math.sin(
                        dp_angle) * depth_distortion
                    diamond_points.append((dp_x, dp_y))

                # Shadow
                shadow_points = [(x + shadow_offset_x, y + shadow_offset_y)
                                 for x, y in diamond_points]
                draw.polygon(shadow_points, fill=shadow_color)

                # 3D diamond with lighting
                face_angle = angle + math.pi / 4
                light_intensity = max(0.3, 0.8 + 0.2 * math.cos(face_angle))
                color_shift = (layer * 60 + i * 25) % 255
                diamond_color = (int(255 * light_intensity *
                                     perspective_scale),
                                 int((170 + color_shift % 85) *
                                     light_intensity * perspective_scale),
                                 int((120 + (color_shift * 2) % 135) *
                                     light_intensity * perspective_scale),
                                 int(
                                     min(255, 130 + layer * 12) *
                                     perspective_scale))
                draw.polygon(diamond_points, fill=diamond_color)


def create_3d_dimensional_portals(draw, center, size, numerology_value):
    """Create 3D dimensional portals with depth and perspective warping"""
    phrase_hash = random.randint(1, 1000000)
    portal_count = min(10, max(3, (phrase_hash % 8) + 3))

    for portal_idx in range(portal_count):
        # 3D portal positioning
        angle_offset = (phrase_hash % 628) * 0.01
        portal_angle = (2 * math.pi * portal_idx) / portal_count + angle_offset
        distance_variation = 0.35 + (phrase_hash % 50) * 0.01
        portal_distance = size * (distance_variation + portal_idx *
                                  (0.08 + (phrase_hash % 25) * 0.001))

        portal_x = center[0] + portal_distance * math.cos(portal_angle)
        portal_y = center[1] + portal_distance * math.sin(portal_angle)

        # 3D portal depth layers
        depth_layers = 15
        for layer in range(depth_layers):
            layer_depth = layer / depth_layers
            perspective_factor = 0.2 + layer_depth * 0.8

            layer_radius = max(
                3,
                size * (0.15 - layer * 0.008) * perspective_factor)
            layer_alpha = max(20, int((250 - layer * 15) * perspective_factor))

            # 3D portal rotation and warping
            warp_factor = math.sin(layer_depth * math.pi) * 0.3

            # Portal color shifts through 3D dimensions
            dimension_hue = (portal_idx * 60 + layer * 20 +
                             numerology_value * 12) % 360
            depth_modifier = layer_depth * 50

            portal_r = int(
                (128 +
                 127 * math.sin(math.radians(dimension_hue + depth_modifier)))
                * perspective_factor)
            portal_g = int((128 + 127 * math.sin(
                math.radians(dimension_hue + 120 + depth_modifier))) *
                           perspective_factor)
            portal_b = int((128 + 127 * math.sin(
                math.radians(dimension_hue + 240 + depth_modifier))) *
                           perspective_factor)

            portal_color = (portal_r, portal_g, portal_b, layer_alpha)

            # 3D warped ellipse with perspective distortion
            warp_x = portal_x + warp_factor * size * 0.1 * math.cos(
                layer * 0.5)
            warp_y = portal_y + warp_factor * size * 0.1 * math.sin(
                layer * 0.5)

            # Draw 3D portal ring with depth
            ring_thickness = max(1, int((8 - layer // 2) * perspective_factor))
            draw.ellipse([
                warp_x - layer_radius, warp_y - layer_radius,
                warp_x + layer_radius, warp_y + layer_radius
            ],
                         outline=portal_color,
                         width=ring_thickness)

            # Add 3D dimensional energy streams
            if layer % 3 == 0:
                stream_count = max(8, 20 - layer)
                for stream in range(stream_count):
                    stream_angle = (2 * math.pi *
                                    stream) / stream_count + layer * 0.8
                    stream_distance = layer_radius * (1.4 + warp_factor)

                    # 3D stream positioning
                    stream_x = warp_x + stream_distance * math.cos(
                        stream_angle)
                    stream_y = warp_y + stream_distance * math.sin(
                        stream_angle)

                    # Stream extends into 3D space
                    stream_length = size * 0.08 * perspective_factor
                    stream_end_x = stream_x + stream_length * math.cos(
                        stream_angle + layer_depth)
                    stream_end_y = stream_y + stream_length * math.sin(
                        stream_angle + layer_depth)

                    stream_color = (255, portal_g, portal_b, layer_alpha)
                    stream_width = max(1, int(4 * perspective_factor))

                    draw.line([stream_x, stream_y, stream_end_x, stream_end_y],
                              fill=stream_color,
                              width=stream_width)


def create_3d_spiral_energy(draw, center, size, direction=1):
    """Create 3D spiral energy with depth and volumetric effects"""
    spiral_layers = 5

    for spiral_layer in range(spiral_layers):
        layer_depth = spiral_layer / spiral_layers
        perspective_scale = 0.3 + layer_depth * 0.7

        spiral_radius = size * 0.12 * perspective_scale
        num_spirals = 4
        spiral_width = max(1, int(5 * perspective_scale))

        for i in range(num_spirals):
            start_angle = i * 45 + spiral_layer * 30
            end_angle = 1080 + i * 45 + spiral_layer * 30  # 3 full rotations
            current_radius = spiral_radius

            spiral_points = []

            for angle in range(start_angle, end_angle, 6):
                # 3D spiral calculations
                angle_3d = math.radians(angle) * direction
                height_3d = (angle - start_angle) * 0.001 * size

                # Perspective projection
                perspective_factor = 1.0 / (1.0 + height_3d / (size * 0.3))

                x = center[0] + current_radius * math.cos(
                    angle_3d) * perspective_factor
                y = center[1] + current_radius * math.sin(
                    angle_3d) * perspective_factor

                spiral_points.append((x, y))

                # 3D lighting based on height and angle
                light_factor = max(0.3, 0.7 + 0.3 * math.sin(angle_3d))

                spiral_color = (int(
                    (170 + (angle % 85)) * light_factor * perspective_factor),
                                int(((angle % 155) + 100) * light_factor *
                                    perspective_factor),
                                int(255 * light_factor * perspective_factor),
                                int(140 * perspective_factor))

                # Draw volumetric spiral segment
                if len(spiral_points) > 1:
                    segment_width = max(1, int(spiral_width * light_factor))
                    draw.line([spiral_points[-2], spiral_points[-1]],
                              fill=spiral_color,
                              width=segment_width)

                # Add 3D energy particles along spiral
                if angle % 45 == 0:
                    particle_size = max(
                        1, int(4 * perspective_factor * light_factor))
                    safe_ellipse(draw, [
                        x - particle_size, y - particle_size,
                        x + particle_size, y + particle_size
                    ],
                                 fill=spiral_color)

                current_radius += size * 0.0012


def draw_3d_letters(draw, center, size, phrase, numerology_value):
    """Draw letters with 3D depth, shadows and perspective"""
    try:
        font = ImageFont.truetype("arial.ttf", max(16, size // 20))
    except:
        font = ImageFont.load_default()

    radius = size * 0.42
    angle_step = 360 / len(phrase)
    points = []

    for i, letter in enumerate(phrase):
        angle = math.radians(i * angle_step - 90)

        # 3D positioning with slight depth variation
        depth_offset = math.sin(i * math.pi / 3) * size * 0.02
        perspective_factor = 1.0 + depth_offset / (size * 2)

        x = center[0] + radius * math.cos(angle) * perspective_factor
        y = center[1] + radius * math.sin(angle) * perspective_factor

        # Get text size for better centering
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        letter_x = x - text_width // 2
        letter_y = y - text_height // 2

        # 3D shadow effect
        shadow_offset = max(2, int(depth_offset * 0.5))
        shadow_color = (0, 0, 0, 120)
        draw.text((letter_x + shadow_offset, letter_y + shadow_offset),
                  letter,
                  font=font,
                  fill=shadow_color)

        # 3D glow effect with multiple layers
        for glow_layer in range(5, 0, -1):
            glow_alpha = max(20, 80 - glow_layer * 12)
            glow_intensity = 6 - glow_layer
            glow_color = (255, 255, 255, glow_alpha)

            for dx in range(-glow_layer, glow_layer + 1):
                for dy in range(-glow_layer, glow_layer + 1):
                    if dx != 0 or dy != 0:
                        draw.text((letter_x + dx, letter_y + dy),
                                  letter,
                                  font=font,
                                  fill=glow_color)

        # Main letter with 3D lighting
        light_factor = max(0.7, 0.9 + 0.1 * math.cos(angle))
        letter_color = (int(255 * light_factor), int(255 * light_factor),
                        int(255 * light_factor), 255)
        draw.text((letter_x, letter_y), letter, font=font, fill=letter_color)
        points.append((x, y))

    # Enhanced 3D connecting lines with energy flow
    if len(points) > 1:
        for i in range(len(points)):
            start_point = points[i]
            end_point = points[(i + 1) % len(points)]

            # Multiple 3D line layers for depth
            for line_layer in range(5):
                layer_depth = line_layer / 5
                line_width = max(1, 8 - line_layer * 2)
                line_alpha = 255 - line_layer * 45

                # 3D line color with lighting
                light_pos = (start_point[0] + end_point[0]) / 2
                light_intensity = max(0.5,
                                      0.8 + 0.2 * math.sin(light_pos * 0.01))

                line_color = (int((255 - line_layer * 30) * light_intensity),
                              int((120 + line_layer * 25) * light_intensity),
                              int((150 + line_layer * 20) * light_intensity),
                              line_alpha)

                # Slight offset for 3D depth
                offset = line_layer * 2
                offset_start = (start_point[0] + offset,
                                start_point[1] + offset)
                offset_end = (end_point[0] + offset, end_point[1] + offset)

                draw.line([offset_start, offset_end],
                          fill=line_color,
                          width=line_width)


def draw_3d_mystical_circles(draw, center, size, numerology_value):
    """Draw 3D mystical circles with depth and atmospheric perspective"""
    circle_count = min(20, max(8, numerology_value * 3))
    outer_radius = size * 0.95

    for circle_idx in range(circle_count):
        # 3D depth positioning
        depth_factor = circle_idx / circle_count
        perspective_scale = 0.4 + depth_factor * 0.6

        circle_radius = (outer_radius - (circle_idx *
                                         (size * 0.04))) * perspective_scale
        if circle_radius <= 8:
            break

        # 3D atmospheric effects
        atmospheric_alpha = max(
            40, int((250 - circle_idx * 10) * perspective_scale))

        # 3D lighting on circles
        base_hue = (numerology_value * 25 + circle_idx * 35) % 360
        light_angle = circle_idx * 0.3
        light_intensity = max(0.4, 0.8 + 0.2 * math.cos(light_angle))

        r = int((150 + 100 * math.sin(math.radians(base_hue))) *
                light_intensity * perspective_scale)
        g = int((150 + 100 * math.sin(math.radians(base_hue + 120))) *
                light_intensity * perspective_scale)
        b = int((150 + 100 * math.sin(math.radians(base_hue + 240))) *
                light_intensity * perspective_scale)

        color = (r, g, b, atmospheric_alpha)

        # 3D circle with depth shadows
        shadow_offset = max(1, int(circle_idx * 0.5))
        shadow_color = (0, 0, 0, int(60 * perspective_scale))

        # Draw shadow
        draw.ellipse([
            center[0] - circle_radius + shadow_offset,
            center[1] - circle_radius + shadow_offset,
            center[0] + circle_radius + shadow_offset,
            center[1] + circle_radius + shadow_offset
        ],
                     outline=shadow_color,
                     width=max(1, 6 - circle_idx // 3))

        # Draw main circle
        thickness = max(1, int((7 - circle_idx // 2) * perspective_scale))
        draw.ellipse([
            center[0] - circle_radius, center[1] - circle_radius,
            center[0] + circle_radius, center[1] + circle_radius
        ],
                     outline=color,
                     width=thickness)

        # Add 3D energy nodes with depth
        if circle_idx % 2 == 0:
            node_count = min(48, numerology_value * 3 + circle_idx)
            for node in range(node_count):
                node_angle = (2 * math.pi *
                              node) / node_count + circle_idx * 0.2

                # 3D node positioning
                node_height = math.sin(node_angle * 3) * circle_radius * 0.1
                node_perspective = 1.0 / (1.0 + abs(node_height) /
                                          (size * 0.2))

                node_x = center[0] + circle_radius * math.cos(
                    node_angle) * node_perspective
                node_y = center[1] + circle_radius * math.sin(
                    node_angle) * node_perspective

                node_size = max(1, int(
                    (7 - circle_idx // 2) * node_perspective))
                node_light = max(0.5, 0.9 + 0.1 * math.cos(node_angle))

                node_color = (int(255 * node_light * node_perspective),
                              int(
                                  max(120, 255 - circle_idx * 12) *
                                  node_light * node_perspective),
                              int(
                                  max(80, 150 + circle_idx * 8) * node_light *
                                  node_perspective),
                              int(atmospheric_alpha * node_perspective))

                safe_ellipse(draw, [
                    node_x - node_size, node_y - node_size, node_x + node_size,
                    node_y + node_size
                ],
                             fill=node_color)


def draw_3d_central_mandala(draw, center, size, numerology_value):
    """Draw 3D central mandala with depth layers and perspective"""
    phrase_hash = random.randint(1, 1000000)
    mandala_base_radius = size // (3 + (phrase_hash % 2))
    mandala_layers = min(12, 4 + (phrase_hash % 6))

    for mandala_layer in range(mandala_layers):
        # 3D layer depth
        layer_depth = mandala_layer / mandala_layers
        perspective_scale = 0.2 + layer_depth * 0.8
        layer_radius = max(
            8,
            int(mandala_base_radius * (1 - mandala_layer * 0.08) *
                perspective_scale))

        # 3D shadow for depth
        shadow_offset = max(1, int(layer_depth * 4))

        # Sacred geometry with 3D perspective
        base_points = 8 + (phrase_hash % 16)
        pattern_points = min(
            60, base_points + numerology_value + mandala_layer *
            ((phrase_hash >> 12) % 6))
        layer_points = []

        for i in range(pattern_points):
            angle = (2 * math.pi * i) / pattern_points + (mandala_layer *
                                                          math.pi / 12)

            # 3D height variation
            height_variation = math.sin(i * math.pi / 6) * layer_radius * 0.2
            point_perspective = 1.0 / (1.0 + abs(height_variation) /
                                       (size * 0.15))

            x = center[0] + layer_radius * math.cos(angle) * point_perspective
            y = center[1] + layer_radius * math.sin(angle) * point_perspective
            layer_points.append((x, y))

        # 3D connections with depth
        connection_step = max(1, pattern_points // max(1, numerology_value))

        for i in range(pattern_points):
            start_point = layer_points[i]
            end_point = layer_points[(i + connection_step) % pattern_points]

            # 3D lighting calculation
            connection_angle = math.atan2(end_point[1] - start_point[1],
                                          end_point[0] - start_point[0])
            light_intensity = max(0.4, 0.8 + 0.2 * math.cos(connection_angle))

            # Shadow line
            shadow_start = (start_point[0] + shadow_offset,
                            start_point[1] + shadow_offset)
            shadow_end = (end_point[0] + shadow_offset,
                          end_point[1] + shadow_offset)
            shadow_color = (0, 0, 0, int(80 * perspective_scale))
            draw.line([shadow_start, shadow_end],
                      fill=shadow_color,
                      width=max(1, 8 - mandala_layer))

            # Main 3D line with lighting
            color_intensity = min(
                255,
                int((170 + (i * numerology_value) % 85) * light_intensity *
                    perspective_scale))
            line_color = (int(
                min(255, 255 - mandala_layer * 20) * light_intensity *
                perspective_scale), color_intensity,
                          int(
                              min(255, 220 + mandala_layer * 8) *
                              light_intensity * perspective_scale),
                          int(
                              max(80, 220 - mandala_layer * 18) *
                              perspective_scale))

            line_width = max(1, int((8 - mandala_layer) * perspective_scale))
            draw.line([start_point, end_point],
                      fill=line_color,
                      width=line_width)

        # 3D energy nodes at intersections
        for point in layer_points[::3]:
            node_size = max(1, int((6 - mandala_layer) * perspective_scale))

            # Node shadow
            shadow_node = (point[0] + shadow_offset, point[1] + shadow_offset)
            draw.ellipse([
                shadow_node[0] - node_size, shadow_node[1] - node_size,
                shadow_node[0] + node_size, shadow_node[1] + node_size
            ],
                         fill=(0, 0, 0, int(60 * perspective_scale)))

            # Main node with 3D lighting
            node_color = (255, 255, 255,
                          int(
                              max(120, 240 - mandala_layer * 20) *
                              perspective_scale))
            safe_ellipse(draw, [
                point[0] - node_size, point[1] - node_size,
                point[0] + node_size, point[1] + node_size
            ],
                         fill=node_color)


def create_3d_chaos_grid(draw, center, size, phrase):
    """Create 3D chaos grid with depth and perspective distortion"""
    grid_density = 0.08
    chaos_intensity = 1.2
    phrase_hash = abs(hash(phrase)) % 1000000

    grid_count = int(size * grid_density)

    for i in range(grid_count):
        # 3D positioning with depth layers
        depth_layer = i % 5
        depth_factor = depth_layer / 5
        perspective_scale = 0.3 + depth_factor * 0.7

        # Grid position with 3D chaos
        x_base = (phrase_hash %
                  size) + (i * (phrase_hash % 9 - 4)) * chaos_intensity
        y_base = ((phrase_hash >> 16) % size) + (i * (
            (phrase_hash >> 8) % 9 - 4)) * chaos_intensity

        # Apply 3D perspective distortion
        x = (x_base * perspective_scale %
             size) + size * (1 - perspective_scale) / 2
        y = (y_base * perspective_scale %
             size) + size * (1 - perspective_scale) / 2

        # 3D line properties
        line_length = size * 0.12 * perspective_scale
        angle_3d = (phrase_hash % 360) + i * (
            (phrase_hash >> 24) % 40 - 20) + depth_layer * 15

        # 3D endpoint calculation
        end_x = x + line_length * math.cos(math.radians(angle_3d))
        end_y = y + line_length * math.sin(math.radians(angle_3d))

        # 3D lighting and depth coloring
        light_angle = math.radians(angle_3d + 45)
        light_intensity = max(0.3, 0.8 + 0.2 * math.cos(light_angle))

        line_color = (int(
            ((phrase_hash % 155) + 100) * light_intensity * perspective_scale),
                      int((((phrase_hash >> 8) % 155) + 100) *
                          light_intensity * perspective_scale),
                      int((((phrase_hash >> 16) % 155) + 100) *
                          light_intensity * perspective_scale),
                      int(120 * perspective_scale))

        # Draw 3D chaos line with width based on depth
        line_width = max(1, int(4 * perspective_scale))
        draw.line([x, y, end_x, end_y], fill=line_color, width=line_width)

        # Add 3D energy burst at endpoints
        if i % 8 == 0:
            burst_size = max(2, int(6 * perspective_scale))
            burst_color = tuple(
                list(line_color[:3]) + [int(line_color[3] * 1.5)])
            safe_ellipse(draw, [
                end_x - burst_size, end_y - burst_size, end_x + burst_size,
                end_y + burst_size
            ],
                         fill=burst_color)


def create_3d_fractal_spirals(draw, center, size, numerology_value):
    """Create 3D fractal spirals with depth and volumetric rendering"""
    phrase_hash = random.randint(1, 1000000)
    spiral_count = min(15, (phrase_hash % 8) + 4)

    for spiral_idx in range(spiral_count):
        # 3D spiral positioning
        spiral_depth = spiral_idx / spiral_count
        perspective_scale = 0.25 + spiral_depth * 0.75

        angle_distribution = 300 + (phrase_hash % 120)
        spiral_start_angle = (spiral_idx * angle_distribution /
                              spiral_count) + ((phrase_hash >> 8) % 360)
        spiral_direction = 1 if (phrase_hash + spiral_idx) % 3 != 0 else -1

        # Multi-level 3D fractal spirals
        for fractal_level in range(6):
            level_depth = fractal_level / 6
            level_perspective = perspective_scale * (0.4 + level_depth * 0.6)

            spiral_radius = size * max(
                0.04, (0.15 + fractal_level * 0.06) * level_perspective)
            spiral_width = max(1, int((7 - fractal_level) * level_perspective))

            spiral_points = []
            for angle_step in range(0, 1200,
                                    8):  # Extended rotation for 3D effect
                current_angle = spiral_start_angle + (angle_step *
                                                      spiral_direction)

                # 3D fractal modification
                height_3d = angle_step * 0.002 * size
                fractal_modifier = 1 + 0.4 * math.sin(
                    math.radians(angle_step * (fractal_level + 1)))
                current_radius = spiral_radius * fractal_modifier

                # 3D perspective projection
                perspective_factor = 1.0 / (1.0 + height_3d / (size * 0.4))

                x = center[0] + current_radius * math.cos(
                    math.radians(current_angle)) * perspective_factor
                y = center[1] + current_radius * math.sin(
                    math.radians(current_angle)) * perspective_factor

                spiral_points.append((x, y))

                # Increase radius for spiral effect
                spiral_radius += size * 0.0008

            # Draw 3D fractal spiral with depth shading
            if len(spiral_points) > 1:
                for i in range(len(spiral_points) - 1):
                    segment_depth = i / len(spiral_points)
                    depth_shading = max(0.3, 1.0 - segment_depth * 0.7)

                    color_shift = (i + fractal_level * 50 +
                                   spiral_idx * 30) % 255
                    spiral_color = (int(
                        min(255, (170 + color_shift % 85) * depth_shading *
                            level_perspective)),
                                    int(
                                        min(255,
                                            (120 + (color_shift * 2) % 135) *
                                            depth_shading *
                                            level_perspective)),
                                    int(255 * depth_shading *
                                        level_perspective),
                                    int(
                                        max(80, 170 - fractal_level * 20) *
                                        level_perspective))

                    segment_width = max(1, int(spiral_width * depth_shading))
                    draw.line([spiral_points[i], spiral_points[i + 1]],
                              fill=spiral_color,
                              width=segment_width)


def draw_3d_cosmic_constellations(draw, center, size, numerology_value,
                                  phrase):
    """Draw 3D cosmic constellations with depth and stellar parallax"""
    phrase_hash = abs(hash(phrase)) % 1000000
    constellation_count = min(15, (phrase_hash % 10) + 4)

    for constellation_idx in range(constellation_count):
        # 3D constellation positioning with depth layers
        constellation_depth = (constellation_idx % 4) / 4
        perspective_scale = 0.3 + constellation_depth * 0.7

        angle_spread = 280 + (phrase_hash % 160)
        constellation_angle = (angle_spread * constellation_idx /
                               constellation_count) * (math.pi / 180)
        distance_base = 0.3 + (phrase_hash % 40) * 0.008
        distance_increment = 0.12 + ((phrase_hash >> 8) % 25) * 0.004
        constellation_distance = size * (
            distance_base +
            (constellation_idx % 6) * distance_increment) * perspective_scale

        # 3D anchor point with depth
        anchor_x = center[0] + constellation_distance * math.cos(
            constellation_angle)
        anchor_y = center[1] + constellation_distance * math.sin(
            constellation_angle)

        # Generate 3D star pattern
        star_count = min(16,
                         (abs(hash(phrase + str(constellation_idx))) % 10) + 8)
        star_positions_3d = []

        for star_idx in range(star_count):
            star_hash = abs(
                hash(phrase + str(constellation_idx) + str(star_idx)))

            # 3D star positioning
            local_angle = (star_hash % 360) * math.pi / 180
            local_distance = (star_hash % 50 +
                              20) * size * 0.004 * perspective_scale
            star_depth = ((star_hash >> 16) % 100 - 50) * size * 0.001

            # 3D to 2D projection with parallax
            parallax_factor = 1.0 / (1.0 + abs(star_depth) / (size * 0.3))
            star_x = anchor_x + local_distance * math.cos(
                local_angle) * parallax_factor
            star_y = anchor_y + local_distance * math.sin(
                local_angle) * parallax_factor

            star_positions_3d.append(
                (star_x, star_y, star_depth, parallax_factor))

            # 3D star rendering with depth-based brightness
            star_brightness = max(2,
                                  int((star_hash % 6) + 4) * parallax_factor)
            star_size = max(1, int(star_brightness * perspective_scale))

            # 3D lighting on star
            light_distance = math.sqrt((star_x - center[0])**2 +
                                       (star_y - center[1])**2)
            light_intensity = max(0.4, 1.0 - light_distance / (size * 1.5))

            star_color = (int(
                min(255, (220 + (star_hash % 35)) * light_intensity *
                    parallax_factor)),
                          int(
                              min(255, (200 + ((star_hash >> 8) % 55)) *
                                  light_intensity * parallax_factor)),
                          int(255 * light_intensity * parallax_factor),
                          int(
                              min(255, (170 + star_brightness * 12) *
                                  parallax_factor)))

            # Draw 3D star with depth-based ray effects
            ray_count = max(6, 12 - int(constellation_depth * 6))
            for ray in range(ray_count):
                ray_angle = ray * 2 * math.pi / ray_count
                ray_length = star_size * (5 + star_depth * 0.01)
                ray_x = star_x + ray_length * math.cos(
                    ray_angle) * parallax_factor
                ray_y = star_y + ray_length * math.sin(
                    ray_angle) * parallax_factor

                ray_color = tuple(
                    list(star_color[:3]) + [int(star_color[3] * 0.7)])
                draw.line([star_x, star_y, ray_x, ray_y],
                          fill=ray_color,
                          width=1)

            safe_ellipse(draw, [
                star_x - star_size, star_y - star_size, star_x + star_size,
                star_y + star_size
            ],
                         fill=star_color)

        # Connect stars in 3D constellation pattern
        if len(star_positions_3d) > 3:
            for i in range(len(star_positions_3d)):
                # Connect to next star with depth consideration
                next_star = (i + 2) % len(star_positions_3d)
                star1 = star_positions_3d[i]
                star2 = star_positions_3d[next_star]

                # 3D connection with depth-based opacity
                depth_diff = abs(star1[2] - star2[2])
                connection_opacity = max(60, int(140 - depth_diff * 0.5))

                connection_color = (
                    int(
                        min(255, 120 + (constellation_idx * 30) % 135) *
                        perspective_scale),
                    int(
                        min(255, 170 + (constellation_idx * 18) % 85) *
                        perspective_scale),
                    int(
                        min(255, 220 + (constellation_idx * 42) % 35) *
                        perspective_scale), connection_opacity)

                # Draw 3D connection with perspective width
                connection_width = max(1, int(2 * min(star1[3], star2[3])))
                draw.line([(star1[0], star1[1]), (star2[0], star2[1])],
                          fill=connection_color,
                          width=connection_width)


def create_3d_energy_vortex(draw, center, size, numerology_value):
    """Create 3D swirling energy vortex with depth and perspective"""
    vortex_layers = 10

    for layer in range(vortex_layers):
        # 3D layer depth and perspective
        layer_depth = layer / vortex_layers
        perspective_scale = 0.2 + layer_depth * 0.8
        layer_radius = size * max(0.08,
                                  (0.85 - layer * 0.08) * perspective_scale)

        # 3D rotation with depth
        rotation_offset = layer * 20 + numerology_value * 6 + layer_depth * 360

        # 3D atmospheric effects
        atmosphere_alpha = max(40, int((200 - layer * 15) * perspective_scale))

        # Create 3D vortex arms
        arm_count = min(10, 4 + (numerology_value % 6))

        for arm in range(arm_count):
            arm_angle = (360 / arm_count * arm) + rotation_offset

            # Create 3D curved vortex arm with depth
            arm_points_3d = []
            for curve_step in range(30):
                step_ratio = curve_step / 29.0

                # 3D logarithmic spiral with height
                current_radius = layer_radius * (1 - step_ratio * 0.8)
                current_angle = arm_angle + (step_ratio * 180 * (layer + 1))
                height_3d = step_ratio * size * 0.1

                # 3D perspective projection
                perspective_factor = 1.0 / (1.0 + height_3d / (size * 0.6))

                # Add 3D turbulence
                turbulence_x = math.sin(step_ratio * math.pi * 6 +
                                        layer) * size * 0.02
                turbulence_y = math.cos(step_ratio * math.pi * 4 +
                                        layer) * size * 0.02

                x = center[0] + (current_radius + turbulence_x) * math.cos(
                    math.radians(current_angle)) * perspective_factor
                y = center[1] + (current_radius + turbulence_y) * math.sin(
                    math.radians(current_angle)) * perspective_factor

                arm_points_3d.append((x, y, height_3d, perspective_factor))

            # Draw 3D vortex arm with depth gradient
            for i in range(len(arm_points_3d) - 1):
                point1 = arm_points_3d[i]
                point2 = arm_points_3d[i + 1]

                # 3D depth-based intensity
                depth_intensity = max(
                    0.3, 1.0 - (point1[2] + point2[2]) / (size * 0.2))
                point_intensity = 1 - (i / len(arm_points_3d))
                combined_intensity = depth_intensity * point_intensity

                # 3D lighting calculation
                segment_angle = math.atan2(point2[1] - point1[1],
                                           point2[0] - point1[0])
                light_factor = max(0.4, 0.8 + 0.2 * math.cos(segment_angle))

                vortex_color = (int(
                    min(255, 255 * combined_intensity * light_factor)),
                                int(
                                    min(255, (170 + layer * 12) *
                                        combined_intensity * light_factor)),
                                int(
                                    min(255, (200 + numerology_value * 8) *
                                        combined_intensity * light_factor)),
                                int(atmosphere_alpha * combined_intensity))

                # 3D line width based on perspective and depth
                line_width = max(
                    1,
                    int((9 - layer) * combined_intensity *
                        min(point1[3], point2[3])))
                draw.line([(point1[0], point1[1]), (point2[0], point2[1])],
                          fill=vortex_color,
                          width=line_width)


def create_3d_crystalline_matrix(draw, center, size, numerology_value):
    """Create 3D crystalline energy matrix with depth and refraction effects"""
    crystal_layers = 6

    for crystal_layer in range(crystal_layers):
        layer_depth = crystal_layer / crystal_layers
        perspective_scale = 0.3 + layer_depth * 0.7

        crystals_per_layer = min(80, numerology_value * 6 + crystal_layer * 8)

        for crystal_idx in range(crystals_per_layer):
            # 3D crystal positioning
            ring_level = crystal_idx // 12
            ring_position = crystal_idx % 12

            ring_radius = size * (0.25 + ring_level * 0.12 +
                                  crystal_layer * 0.05) * perspective_scale
            crystal_angle = (2 * math.pi * ring_position) / 12 + (
                ring_level * 0.25) + (crystal_layer * 0.4)

            # 3D height variation
            crystal_height = math.sin(crystal_angle * 3 +
                                      crystal_layer) * size * 0.05
            height_perspective = 1.0 / (1.0 + abs(crystal_height) /
                                        (size * 0.3))

            crystal_x = center[0] + ring_radius * math.cos(
                crystal_angle) * height_perspective
            crystal_y = center[1] + ring_radius * math.sin(
                crystal_angle) * height_perspective

            # 3D crystal structure with depth
            crystal_size = max(
                2,
                int(size * (0.025 - ring_level * 0.002) * perspective_scale *
                    height_perspective))

            # 3D crystal facets with perspective
            facet_count = 8
            crystal_points = []

            for facet in range(facet_count):
                facet_angle = crystal_angle + (facet * 2 * math.pi /
                                               facet_count)
                # 3D facet positioning with depth distortion
                facet_depth_factor = math.cos(facet_angle) * 0.3 + 0.7
                facet_x = crystal_x + crystal_size * math.cos(
                    facet_angle) * facet_depth_factor
                facet_y = crystal_y + crystal_size * math.sin(
                    facet_angle) * facet_depth_factor
                crystal_points.append((facet_x, facet_y))

            # 3D crystal color with depth and refraction
            crystal_hue = (crystal_idx * 25 + numerology_value * 35 +
                           crystal_layer * 45) % 360
            depth_modifier = layer_depth * 80
            refraction_factor = max(0.5, height_perspective)

            crystal_r = int(
                (220 +
                 35 * math.sin(math.radians(crystal_hue + depth_modifier))) *
                refraction_factor * perspective_scale)
            crystal_g = int(
                (220 + 35 *
                 math.sin(math.radians(crystal_hue + 120 + depth_modifier))) *
                refraction_factor * perspective_scale)
            crystal_b = int(
                (220 + 35 *
                 math.sin(math.radians(crystal_hue + 240 + depth_modifier))) *
                refraction_factor * perspective_scale)
            crystal_alpha = int(
                max(120, 220 - ring_level * 15) * perspective_scale)

            crystal_color = (crystal_r, crystal_g, crystal_b, crystal_alpha)

            # Draw 3D crystal with depth shadow
            shadow_offset = max(1, int(layer_depth * 3))
            shadow_points = [(x + shadow_offset, y + shadow_offset)
                             for x, y in crystal_points]
            shadow_color = (0, 0, 0, int(60 * perspective_scale))

            if len(shadow_points) >= 3:
                draw.polygon(shadow_points, fill=shadow_color)
            if len(crystal_points) >= 3:
                draw.polygon(crystal_points,
                             fill=crystal_color,
                             outline=(255, 255, 255,
                                      int(180 * perspective_scale)))

            # 3D crystal energy emanation with depth
            for emanation in range(6):
                emanation_angle = crystal_angle + (emanation * math.pi / 3)
                emanation_length = crystal_size * (3 + layer_depth * 2)

                # 3D emanation with perspective
                emanation_x = crystal_x + emanation_length * math.cos(
                    emanation_angle) * height_perspective
                emanation_y = crystal_y + emanation_length * math.sin(
                    emanation_angle) * height_perspective

                emanation_color = (crystal_r, crystal_g, crystal_b,
                                   int(crystal_alpha * 0.6))
                emanation_width = max(
                    1, int(2 * perspective_scale * height_perspective))

                draw.line([crystal_x, crystal_y, emanation_x, emanation_y],
                          fill=emanation_color,
                          width=emanation_width)


def create_3d_plasma_effects(draw, center, size, numerology_value, phrase):
    """Create 3D plasma energy effects with volumetric rendering"""
    plasma_layers = 8
    phrase_energy = abs(hash(phrase)) % 1000

    for plasma_layer in range(plasma_layers):
        layer_depth = plasma_layer / plasma_layers
        perspective_scale = 0.25 + layer_depth * 0.75
        plasma_radius = size * (0.75 - plasma_layer * 0.06) * perspective_scale

        # 3D plasma intensity based on depth
        layer_intensity = max(0.4, 1.0 - layer_depth * 0.6)
        layer_alpha = int(200 * layer_intensity * perspective_scale)

        # 3D plasma tendrils with depth
        tendril_count = min(20, numerology_value + plasma_layer * 2)

        for tendril in range(tendril_count):
            base_angle = (2 * math.pi * tendril) / tendril_count + (
                plasma_layer * 0.3)

            # Create 3D plasma tendril path with height variation
            tendril_points_3d = []
            current_radius = plasma_radius * 0.25

            for step in range(20):
                step_ratio = step / 19.0

                # 3D plasma distortion with depth
                height_3d = step_ratio * size * 0.08
                distortion_3d = math.sin(step_ratio * math.pi * 4 +
                                         phrase_energy * 0.01 +
                                         plasma_layer) * size * 0.025

                # 3D angle progression
                current_angle = base_angle + (step_ratio * math.pi * 0.8) + (
                    layer_depth * math.pi * 0.3)

                # 3D perspective projection
                perspective_factor = 1.0 / (1.0 + height_3d / (size * 0.4))

                x = center[0] + (current_radius + distortion_3d) * math.cos(
                    current_angle) * perspective_factor
                y = center[1] + (current_radius + distortion_3d) * math.sin(
                    current_angle) * perspective_factor

                tendril_points_3d.append((x, y, height_3d, perspective_factor))
                current_radius += size * 0.018

            # Draw 3D plasma tendril with depth effects
            for i in range(len(tendril_points_3d) - 1):
                point1 = tendril_points_3d[i]
                point2 = tendril_points_3d[i + 1]

                # 3D plasma intensity based on depth and position
                depth_intensity = max(
                    0.3, 1.0 - (point1[2] + point2[2]) / (size * 0.16))
                plasma_intensity_factor = depth_intensity * (
                    1 - (i / len(tendril_points_3d)))

                # 3D plasma lighting
                segment_center_x = (point1[0] + point2[0]) / 2
                segment_center_y = (point1[1] + point2[1]) / 2
                light_distance = math.sqrt((segment_center_x - center[0])**2 +
                                           (segment_center_y - center[1])**2)
                light_factor = max(0.4, 1.0 - light_distance / (size * 1.2))

                # 3D plasma color with depth and energy
                plasma_hue = (tendril * 30 + plasma_layer * 50 +
                              phrase_energy + i * 8) % 360
                plasma_r = int(255 * plasma_intensity_factor * light_factor)
                plasma_g = int(
                    (170 + 60 * math.sin(math.radians(plasma_hue))) *
                    plasma_intensity_factor * light_factor)
                plasma_b = int(
                    (220 + 35 * math.cos(math.radians(plasma_hue))) *
                    plasma_intensity_factor * light_factor)
                plasma_alpha = int(layer_alpha * plasma_intensity_factor)

                plasma_color = (plasma_r, plasma_g, plasma_b, plasma_alpha)

                # 3D tendril width based on perspective and intensity
                tendril_width = max(
                    1,
                    int(6 * plasma_intensity_factor *
                        min(point1[3], point2[3])))
                draw.line([(point1[0], point1[1]), (point2[0], point2[1])],
                          fill=plasma_color,
                          width=tendril_width)


def create_3d_atmospheric_lighting(draw, center, size, numerology_value):
    """Create 3D atmospheric lighting effects with depth"""
    # 3D light sources with depth
    light_sources = [
        (center[0] + size * 0.4, center[1] - size * 0.3,
         size * 0.6),  # Primary light
        (center[0] - size * 0.3, center[1] + size * 0.4,
         size * 0.4),  # Secondary light
        (center[0], center[1], size * 0.8)  # Central ambient light
    ]

    for light_idx, (light_x, light_y, light_z) in enumerate(light_sources):
        light_intensity = 0.8 - light_idx * 0.2
        light_radius = size * (0.6 - light_idx * 0.15)

        # 3D atmospheric light rays
        ray_count = min(36, 12 + numerology_value * 2)

        for ray in range(ray_count):
            ray_angle = (2 * math.pi * ray) / ray_count + light_idx * 0.5

            # 3D ray path with atmospheric scattering
            ray_points = []
            for step in range(15):
                step_ratio = step / 14.0

                # 3D ray progression with scattering
                current_distance = light_radius * step_ratio
                height_3d = light_z * step_ratio * 0.3

                # Atmospheric scattering effect
                scattering = math.sin(step_ratio * math.pi) * size * 0.02

                # 3D perspective projection
                perspective_factor = 1.0 / (1.0 + height_3d / (size * 0.8))

                x = light_x + (current_distance + scattering
                               ) * math.cos(ray_angle) * perspective_factor
                y = light_y + (current_distance + scattering
                               ) * math.sin(ray_angle) * perspective_factor

                ray_points.append((x, y, perspective_factor))

            # Draw 3D atmospheric ray
            for i in range(len(ray_points) - 1):
                point1 = ray_points[i]
                point2 = ray_points[i + 1]

                # 3D atmospheric intensity
                atmospheric_intensity = light_intensity * (
                    1 - (i / len(ray_points))) * min(point1[2], point2[2])

                if atmospheric_intensity > 0.1:
                    ray_color = (int(255 * atmospheric_intensity),
                                 int(200 * atmospheric_intensity),
                                 int(150 * atmospheric_intensity),
                                 int(60 * atmospheric_intensity))

                    ray_width = max(1, int(3 * atmospheric_intensity))
                    draw.line([(point1[0], point1[1]), (point2[0], point2[1])],
                              fill=ray_color,
                              width=ray_width)


def apply_3d_post_processing(img, size, numerology_value):
    """Apply 3D post-processing effects for enhanced depth and beauty"""
    # Convert to enhance-able format
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.3)  # Increase contrast for depth

    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.4)  # Boost color saturation

    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)  # Slight brightness increase

    # Apply subtle blur for atmospheric depth (very light)
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

    # Enhance sharpness for crisp 3D details
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.2)

    return img


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    phrase = data.get('phrase', '')
    vibe = data.get('vibe', 'mystical')

    if not phrase.strip():
        return jsonify({'error': 'Please enter your intent or desire'})

    img_base64, error = create_sigil(phrase.strip(), vibe)

    if error:
        return jsonify({'error': error})

    return jsonify({'image': f'data:image/png;base64,{img_base64}'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
