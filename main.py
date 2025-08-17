
from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from datetime import datetime
import string
import math
import io
import base64
import random
import numpy as np

app = Flask(__name__)


def create_sigil(phrase, vibe="mystical", size=400):
    """Create a highly varied sigil with dramatic vibe differences"""
    print(f"🎨 Creating sigil for: '{phrase}' with vibe: '{vibe}' at size: {size}")
    
    original_phrase = phrase
    phrase = phrase.upper()
    phrase = ''.join([c for c in phrase if c in string.ascii_uppercase])
    phrase = ''.join(sorted(set(phrase), key=phrase.index))

    if not phrase:
        return None, "Please enter text with at least one letter"

    print(f"📝 Processed phrase: '{phrase}'")

    # Calculate multiple seeds for maximum variation
    text_seed = abs(hash(original_phrase.lower())) % 2147483647
    vibe_seed = abs(hash(vibe)) % 2147483647
    combined_seed = abs(hash(original_phrase.lower() + vibe + str(len(original_phrase)))) % 2147483647
    
    print(f"🌱 Using seeds - Text: {text_seed}, Vibe: {vibe_seed}, Combined: {combined_seed}")

    # Create image
    img = Image.new('RGBA', (size, size), color=(0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    center = (size // 2, size // 2)

    # Generate vibe-specific sigil
    if vibe == 'mystical':
        create_mystical_sigil(draw, img, center, size, phrase, text_seed, combined_seed)
    elif vibe == 'cosmic':
        create_cosmic_sigil(draw, img, center, size, phrase, text_seed, combined_seed)
    elif vibe == 'elemental':
        create_elemental_sigil(draw, img, center, size, phrase, text_seed, combined_seed)
    elif vibe == 'crystal':
        create_crystal_sigil(draw, img, center, size, phrase, text_seed, combined_seed)
    elif vibe == 'shadow':
        create_shadow_sigil(draw, img, center, size, phrase, text_seed, combined_seed)
    elif vibe == 'light':
        create_light_sigil(draw, img, center, size, phrase, text_seed, combined_seed)
    else:
        create_mystical_sigil(draw, img, center, size, phrase, text_seed, combined_seed)

    print("🎨 Applying final enhancements...")
    img = apply_vibe_effects(img, vibe)

    print("💾 Converting to base64...")
    try:
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG', quality=95, optimize=True)
        img_buffer.seek(0)
        img_data = img_buffer.getvalue()
        img_base64 = base64.b64encode(img_data).decode()
        
        print(f"✅ Image created successfully: {len(img_base64)} characters")
        return img_base64, None
        
    except Exception as e:
        print(f"❌ Error converting image: {str(e)}")
        return None, f"Error creating image: {str(e)}"


def create_mystical_sigil(draw, img, center, size, phrase, text_seed, combined_seed):
    """Create flowing, ethereal mystical sigil"""
    random.seed(combined_seed)
    
    # Mystical colors - purples, magentas, ethereal blues
    colors = [(150, 60, 220), (255, 100, 255), (120, 200, 255), (200, 150, 255), (180, 120, 255)]
    
    # Create flowing energy streams
    for stream in range(8 + len(phrase)):
        random.seed(combined_seed + stream + text_seed)
        start_angle = random.uniform(0, 360)
        stream_length = random.randint(100, size//2)
        
        points = []
        current_x, current_y = center
        current_angle = start_angle
        
        for step in range(30):
            current_angle += random.uniform(-30, 30)
            step_size = stream_length / 30
            current_x += step_size * math.cos(math.radians(current_angle))
            current_y += step_size * math.sin(math.radians(current_angle))
            points.append((current_x, current_y))
        
        # Draw flowing line
        color = colors[stream % len(colors)]
        for i in range(len(points) - 1):
            try:
                draw.line([points[i], points[i + 1]], fill=(*color, 180), width=3)
            except:
                pass
    
    # Add mystical symbols
    create_mystical_symbols(draw, center, size, phrase, colors, text_seed)
    
    # Add ethereal particles
    for i in range(50 + ord(phrase[0]) if phrase else 50):
        random.seed(combined_seed + i)
        x = random.randint(0, size)
        y = random.randint(0, size)
        radius = random.randint(2, 8)
        color = colors[i % len(colors)]
        alpha = random.randint(60, 150)
        
        try:
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        fill=(*color, alpha))
        except:
            pass


def create_cosmic_sigil(draw, img, center, size, phrase, text_seed, combined_seed):
    """Create stellar, galactic cosmic sigil"""
    random.seed(combined_seed)
    
    # Cosmic colors - deep space blues, stellar whites, nebula colors
    colors = [(20, 20, 80), (100, 150, 255), (200, 100, 255), (255, 200, 100), (50, 255, 200)]
    
    # Create star field background
    for star in range(200 + len(phrase) * 10):
        random.seed(combined_seed + star + text_seed)
        x = random.randint(0, size)
        y = random.randint(0, size)
        brightness = random.randint(100, 255)
        star_size = random.randint(1, 4)
        
        try:
            draw.ellipse([x-star_size, y-star_size, x+star_size, y+star_size], 
                        fill=(brightness, brightness, brightness, 200))
        except:
            pass
    
    # Create galactic spiral
    for spiral in range(3):
        random.seed(combined_seed + spiral)
        start_radius = size // 8
        
        points = []
        for angle in range(0, 720, 5):
            radius = start_radius + (angle / 720) * (size // 3)
            actual_angle = angle + spiral * 120
            x = center[0] + radius * math.cos(math.radians(actual_angle))
            y = center[1] + radius * math.sin(math.radians(actual_angle))
            points.append((x, y))
        
        # Draw spiral arms
        color = colors[spiral % len(colors)]
        for i in range(len(points) - 1):
            try:
                draw.line([points[i], points[i + 1]], fill=(*color, 150), width=4)
            except:
                pass
    
    # Add constellation based on phrase
    create_constellation(draw, center, size, phrase, colors, text_seed)
    
    # Add nebula clouds
    create_nebula_effect(img, colors, combined_seed)


def create_elemental_sigil(draw, img, center, size, phrase, text_seed, combined_seed):
    """Create elemental sigil with earth, fire, water, air patterns"""
    random.seed(combined_seed)
    
    # Elemental colors
    colors = [(255, 100, 50), (50, 255, 100), (100, 150, 255), (200, 150, 100), (255, 200, 50)]
    
    # Determine dominant element from phrase
    element_value = sum(ord(c) for c in phrase) % 4
    
    if element_value == 0:  # Fire
        create_fire_pattern(draw, center, size, phrase, colors, text_seed)
    elif element_value == 1:  # Water
        create_water_pattern(draw, center, size, phrase, colors, text_seed)
    elif element_value == 2:  # Earth
        create_earth_pattern(draw, center, size, phrase, colors, text_seed)
    else:  # Air
        create_air_pattern(draw, center, size, phrase, colors, text_seed)
    
    # Add elemental symbols
    create_elemental_symbols(draw, center, size, phrase, colors, combined_seed)


def create_crystal_sigil(draw, img, center, size, phrase, text_seed, combined_seed):
    """Create geometric crystal sigil"""
    random.seed(combined_seed)
    
    # Crystal colors - clear, bright, geometric
    colors = [(200, 255, 255), (150, 200, 255), (255, 200, 255), (200, 255, 200), (255, 255, 200)]
    
    # Create crystal lattice structure
    lattice_points = []
    grid_size = 6 + len(phrase)
    
    for i in range(grid_size):
        for j in range(grid_size):
            x = (i / (grid_size - 1)) * size * 0.8 + size * 0.1
            y = (j / (grid_size - 1)) * size * 0.8 + size * 0.1
            lattice_points.append((x, y))
    
    # Connect lattice points in crystal patterns
    random.seed(text_seed)
    for i, point in enumerate(lattice_points):
        connections = random.randint(2, 5)
        for _ in range(connections):
            target_idx = random.randint(0, len(lattice_points) - 1)
            target_point = lattice_points[target_idx]
            
            color = colors[i % len(colors)]
            try:
                draw.line([point, target_point], fill=(*color, 120), width=2)
            except:
                pass
    
    # Add crystal facets
    create_crystal_facets(draw, center, size, phrase, colors, combined_seed)
    
    # Add geometric patterns
    create_geometric_patterns(draw, center, size, phrase, colors, text_seed)


def create_shadow_sigil(draw, img, center, size, phrase, text_seed, combined_seed):
    """Create dark, mysterious shadow sigil"""
    random.seed(combined_seed)
    
    # Shadow colors - deep purples, dark grays, mysterious blacks
    colors = [(80, 20, 80), (120, 60, 120), (60, 20, 60), (100, 40, 100), (40, 40, 80)]
    
    # Create shadow tendrils
    for tendril in range(12 + len(phrase)):
        random.seed(combined_seed + tendril + text_seed)
        start_angle = random.uniform(0, 360)
        
        points = []
        current_x, current_y = center
        
        for step in range(25):
            distance = step * (size // 50)
            angle_variation = random.uniform(-45, 45)
            actual_angle = start_angle + angle_variation
            
            x = current_x + distance * math.cos(math.radians(actual_angle))
            y = current_y + distance * math.sin(math.radians(actual_angle))
            points.append((x, y))
            
            current_x, current_y = x, y
        
        # Draw tendril with varying thickness
        color = colors[tendril % len(colors)]
        for i in range(len(points) - 1):
            thickness = max(1, 8 - i // 3)
            try:
                draw.line([points[i], points[i + 1]], fill=(*color, 160), width=thickness)
            except:
                pass
    
    # Add shadow runes
    create_shadow_runes(draw, center, size, phrase, colors, text_seed)
    
    # Add void spaces
    create_void_effect(draw, center, size, phrase, combined_seed)


def create_light_sigil(draw, img, center, size, phrase, text_seed, combined_seed):
    """Create radiant, healing light sigil"""
    random.seed(combined_seed)
    
    # Light colors - brilliant whites, golds, radiant colors
    colors = [(255, 255, 200), (255, 200, 150), (200, 255, 200), (255, 220, 255), (255, 255, 150)]
    
    # Create radial light beams
    num_beams = 16 + len(phrase)
    for beam in range(num_beams):
        angle = (360 / num_beams) * beam
        beam_length = size // 2 - 20
        
        # Create beam gradient
        for intensity in range(10):
            current_length = beam_length * (intensity + 1) / 10
            x = center[0] + current_length * math.cos(math.radians(angle))
            y = center[1] + current_length * math.sin(math.radians(angle))
            
            alpha = 200 - intensity * 15
            color = colors[beam % len(colors)]
            width = max(1, 6 - intensity // 2)
            
            try:
                draw.line([center, (x, y)], fill=(*color, alpha), width=width)
            except:
                pass
    
    # Add light orbs
    create_light_orbs(draw, center, size, phrase, colors, text_seed)
    
    # Add healing symbols
    create_healing_symbols(draw, center, size, phrase, colors, combined_seed)
    
    # Add radiance effect
    create_radiance_effect(img, center, size, colors)


# Helper functions for specific pattern creation
def create_mystical_symbols(draw, center, size, phrase, colors, seed):
    """Create flowing mystical symbols"""
    random.seed(seed)
    
    for i, letter in enumerate(phrase):
        angle = (360 / len(phrase)) * i
        distance = size // 4
        x = center[0] + distance * math.cos(math.radians(angle))
        y = center[1] + distance * math.sin(math.radians(angle))
        
        # Create mystical glyph
        glyph_size = 20 + ord(letter) % 15
        color = colors[i % len(colors)]
        
        # Draw complex mystical symbol
        for symbol_part in range(5):
            part_angle = angle + symbol_part * 72
            inner_x = x + glyph_size * math.cos(math.radians(part_angle))
            inner_y = y + glyph_size * math.sin(math.radians(part_angle))
            
            try:
                draw.line([(x, y), (inner_x, inner_y)], fill=(*color, 200), width=3)
                draw.ellipse([inner_x-3, inner_y-3, inner_x+3, inner_y+3], fill=(*color, 255))
            except:
                pass


def create_constellation(draw, center, size, phrase, colors, seed):
    """Create constellation pattern"""
    random.seed(seed)
    
    # Create star positions based on phrase
    star_positions = []
    for i, letter in enumerate(phrase):
        angle = (360 / len(phrase)) * i + ord(letter) * 10
        distance = (size // 6) + (ord(letter) % 100)
        x = center[0] + distance * math.cos(math.radians(angle))
        y = center[1] + distance * math.sin(math.radians(angle))
        star_positions.append((x, y))
    
    # Connect stars in constellation pattern
    for i in range(len(star_positions)):
        for j in range(i + 1, len(star_positions)):
            if (i + j) % 3 == 0:  # Connect every third combination
                color = colors[(i + j) % len(colors)]
                try:
                    draw.line([star_positions[i], star_positions[j]], 
                             fill=(*color, 120), width=2)
                except:
                    pass
        
        # Draw bright star
        pos = star_positions[i]
        color = colors[i % len(colors)]
        try:
            draw.ellipse([pos[0]-6, pos[1]-6, pos[0]+6, pos[1]+6], 
                        fill=(*color, 255))
        except:
            pass


def create_fire_pattern(draw, center, size, phrase, colors, seed):
    """Create fire elemental pattern"""
    random.seed(seed)
    
    # Create flame tongues
    for flame in range(8 + len(phrase)):
        base_x = center[0] + random.randint(-size//4, size//4)
        base_y = center[1] + size//3
        
        flame_height = random.randint(size//4, size//2)
        flame_points = []
        
        for height in range(0, flame_height, 10):
            flicker = random.randint(-20, 20)
            x = base_x + flicker
            y = base_y - height
            flame_points.append((x, y))
        
        # Draw flame
        color = colors[0]  # Fire color
        for i in range(len(flame_points) - 1):
            width = max(1, 8 - i)
            alpha = max(100, 255 - i * 10)
            try:
                draw.line([flame_points[i], flame_points[i + 1]], 
                         fill=(*color, alpha), width=width)
            except:
                pass


def create_water_pattern(draw, center, size, phrase, colors, seed):
    """Create water elemental pattern"""
    random.seed(seed)
    
    # Create flowing water waves
    for wave in range(6):
        y_offset = center[1] - size//3 + wave * (size//6)
        
        wave_points = []
        for x in range(0, size, 10):
            wave_height = 30 * math.sin((x + wave * 50) * 0.02)
            y = y_offset + wave_height
            wave_points.append((x, y))
        
        # Draw wave
        color = colors[2]  # Water color
        for i in range(len(wave_points) - 1):
            try:
                draw.line([wave_points[i], wave_points[i + 1]], 
                         fill=(*color, 150), width=3)
            except:
                pass


def create_earth_pattern(draw, center, size, phrase, colors, seed):
    """Create earth elemental pattern"""
    random.seed(seed)
    
    # Create rock formation pattern
    for rock in range(12 + len(phrase)):
        x = random.randint(size//6, size - size//6)
        y = random.randint(size//6, size - size//6)
        rock_size = random.randint(15, 40)
        
        # Draw rock as polygon
        points = []
        for angle in range(0, 360, 45):
            variation = random.randint(-5, 5)
            radius = rock_size + variation
            px = x + radius * math.cos(math.radians(angle))
            py = y + radius * math.sin(math.radians(angle))
            points.append((px, py))
        
        color = colors[3]  # Earth color
        try:
            draw.polygon(points, fill=(*color, 180))
        except:
            pass


def create_air_pattern(draw, center, size, phrase, colors, seed):
    """Create air elemental pattern"""
    random.seed(seed)
    
    # Create wind spirals
    for spiral in range(4):
        spiral_center_x = center[0] + random.randint(-size//4, size//4)
        spiral_center_y = center[1] + random.randint(-size//4, size//4)
        
        spiral_points = []
        for angle in range(0, 720, 15):
            radius = (angle / 720) * (size // 6)
            x = spiral_center_x + radius * math.cos(math.radians(angle))
            y = spiral_center_y + radius * math.sin(math.radians(angle))
            spiral_points.append((x, y))
        
        # Draw spiral
        color = colors[4]  # Air color
        for i in range(len(spiral_points) - 1):
            try:
                draw.line([spiral_points[i], spiral_points[i + 1]], 
                         fill=(*color, 130), width=2)
            except:
                pass


def create_elemental_symbols(draw, center, size, phrase, colors, seed):
    """Create elemental symbols"""
    symbols = ['▲', '▼', '◆', '○']  # Triangle up (fire), down (water), diamond (earth), circle (air)
    
    for i, symbol in enumerate(symbols):
        angle = i * 90
        distance = size // 3
        x = center[0] + distance * math.cos(math.radians(angle))
        y = center[1] + distance * math.sin(math.radians(angle))
        
        color = colors[i % len(colors)]
        
        # Draw elemental symbol as geometric shape
        if symbol == '▲':  # Fire triangle
            points = [(x, y-15), (x-13, y+10), (x+13, y+10)]
            try:
                draw.polygon(points, fill=(*color, 200))
            except:
                pass
        elif symbol == '▼':  # Water triangle
            points = [(x, y+15), (x-13, y-10), (x+13, y-10)]
            try:
                draw.polygon(points, fill=(*color, 200))
            except:
                pass
        elif symbol == '◆':  # Earth diamond
            points = [(x, y-15), (x+15, y), (x, y+15), (x-15, y)]
            try:
                draw.polygon(points, fill=(*color, 200))
            except:
                pass
        else:  # Air circle
            try:
                draw.ellipse([x-15, y-15, x+15, y+15], outline=(*color, 200), width=3)
            except:
                pass


def create_crystal_facets(draw, center, size, phrase, colors, seed):
    """Create crystal facet patterns"""
    random.seed(seed)
    
    for facet in range(6 + len(phrase)):
        # Create triangular facets
        angle = random.uniform(0, 360)
        distance = random.randint(size//6, size//3)
        
        facet_x = center[0] + distance * math.cos(math.radians(angle))
        facet_y = center[1] + distance * math.sin(math.radians(angle))
        
        facet_size = random.randint(20, 50)
        
        # Create facet as triangle
        points = []
        for i in range(3):
            point_angle = angle + i * 120
            px = facet_x + facet_size * math.cos(math.radians(point_angle))
            py = facet_y + facet_size * math.sin(math.radians(point_angle))
            points.append((px, py))
        
        color = colors[facet % len(colors)]
        try:
            draw.polygon(points, fill=(*color, 150), outline=(*color, 255))
        except:
            pass


def create_geometric_patterns(draw, center, size, phrase, colors, seed):
    """Create geometric patterns"""
    random.seed(seed)
    
    # Create geometric grid
    for i in range(5):
        for j in range(5):
            x = size * 0.2 + i * size * 0.15
            y = size * 0.2 + j * size * 0.15
            
            pattern_type = (i + j + ord(phrase[0]) if phrase else 0) % 4
            color = colors[(i + j) % len(colors)]
            
            if pattern_type == 0:  # Square
                try:
                    draw.rectangle([x-10, y-10, x+10, y+10], outline=(*color, 200), width=2)
                except:
                    pass
            elif pattern_type == 1:  # Circle
                try:
                    draw.ellipse([x-10, y-10, x+10, y+10], outline=(*color, 200), width=2)
                except:
                    pass
            elif pattern_type == 2:  # Triangle
                points = [(x, y-12), (x-10, y+8), (x+10, y+8)]
                try:
                    draw.polygon(points, outline=(*color, 200))
                except:
                    pass
            else:  # Diamond
                points = [(x, y-10), (x+10, y), (x, y+10), (x-10, y)]
                try:
                    draw.polygon(points, outline=(*color, 200))
                except:
                    pass


def create_shadow_runes(draw, center, size, phrase, colors, seed):
    """Create dark runic symbols"""
    random.seed(seed)
    
    for i, letter in enumerate(phrase):
        angle = (360 / len(phrase)) * i + 45
        distance = size // 5
        x = center[0] + distance * math.cos(math.radians(angle))
        y = center[1] + distance * math.sin(math.radians(angle))
        
        # Create complex rune based on letter
        rune_complexity = ord(letter) % 5 + 3
        color = colors[i % len(colors)]
        
        for rune_line in range(rune_complexity):
            line_angle = angle + rune_line * 45
            line_length = 15 + (ord(letter) % 10)
            
            start_x = x + (line_length // 2) * math.cos(math.radians(line_angle))
            start_y = y + (line_length // 2) * math.sin(math.radians(line_angle))
            end_x = x - (line_length // 2) * math.cos(math.radians(line_angle))
            end_y = y - (line_length // 2) * math.sin(math.radians(line_angle))
            
            try:
                draw.line([(start_x, start_y), (end_x, end_y)], 
                         fill=(*color, 220), width=3)
            except:
                pass


def create_void_effect(draw, center, size, phrase, seed):
    """Create void spaces in shadow sigil"""
    random.seed(seed)
    
    for void in range(3 + len(phrase)):
        void_x = random.randint(size//4, size - size//4)
        void_y = random.randint(size//4, size - size//4)
        void_radius = random.randint(10, 30)
        
        # Create void as black circle with dark outline
        try:
            draw.ellipse([void_x-void_radius, void_y-void_radius, 
                         void_x+void_radius, void_y+void_radius], 
                        fill=(0, 0, 0, 255), outline=(40, 40, 40, 200))
        except:
            pass


def create_light_orbs(draw, center, size, phrase, colors, seed):
    """Create radiant light orbs"""
    random.seed(seed)
    
    for orb in range(8 + len(phrase)):
        orb_x = random.randint(size//6, size - size//6)
        orb_y = random.randint(size//6, size - size//6)
        orb_radius = random.randint(8, 25)
        
        color = colors[orb % len(colors)]
        
        # Create orb with gradient effect
        for radius_step in range(orb_radius, 0, -2):
            alpha = int(255 * (radius_step / orb_radius) * 0.6)
            try:
                draw.ellipse([orb_x-radius_step, orb_y-radius_step, 
                             orb_x+radius_step, orb_y+radius_step], 
                            fill=(*color, alpha))
            except:
                pass


def create_healing_symbols(draw, center, size, phrase, colors, seed):
    """Create healing light symbols"""
    random.seed(seed)
    
    # Create cross/plus symbols for healing
    for i in range(4 + len(phrase)):
        angle = (360 / (4 + len(phrase))) * i
        distance = size // 4
        x = center[0] + distance * math.cos(math.radians(angle))
        y = center[1] + distance * math.sin(math.radians(angle))
        
        color = colors[i % len(colors)]
        cross_size = 15
        
        # Draw healing cross
        try:
            # Vertical line
            draw.line([(x, y-cross_size), (x, y+cross_size)], 
                     fill=(*color, 255), width=4)
            # Horizontal line
            draw.line([(x-cross_size, y), (x+cross_size, y)], 
                     fill=(*color, 255), width=4)
        except:
            pass


def create_radiance_effect(img, center, size, colors):
    """Create radiance effect for light sigil"""
    # Create radial gradient overlay
    for y in range(size):
        for x in range(size):
            distance = math.sqrt((x - center[0])**2 + (y - center[1])**2)
            max_distance = size / 2
            
            if distance < max_distance:
                intensity = 1 - (distance / max_distance)
                current_pixel = img.getpixel((x, y))
                
                # Add golden radiance
                if len(current_pixel) == 4:  # RGBA
                    r, g, b, a = current_pixel
                    radiance_boost = int(intensity * 30)
                    new_r = min(255, r + radiance_boost)
                    new_g = min(255, g + radiance_boost)
                    new_b = min(255, b + radiance_boost // 2)
                    img.putpixel((x, y), (new_r, new_g, new_b, a))


def create_nebula_effect(img, colors, seed):
    """Create nebula cloud effect for cosmic sigil"""
    random.seed(seed)
    
    # Create cloudy nebula regions
    for cloud in range(5):
        cloud_x = random.randint(0, img.width)
        cloud_y = random.randint(0, img.height)
        cloud_size = random.randint(50, 120)
        color = colors[cloud % len(colors)]
        
        for radius in range(cloud_size, 0, -5):
            alpha = int(60 * (radius / cloud_size))
            
            # Create soft circular gradient
            for angle in range(0, 360, 10):
                x = cloud_x + radius * math.cos(math.radians(angle))
                y = cloud_y + radius * math.sin(math.radians(angle))
                
                if 0 <= x < img.width and 0 <= y < img.height:
                    current_pixel = img.getpixel((int(x), int(y)))
                    if len(current_pixel) == 4:
                        r, g, b, a = current_pixel
                        blend_r = min(255, r + color[0] * alpha // 255)
                        blend_g = min(255, g + color[1] * alpha // 255)
                        blend_b = min(255, b + color[2] * alpha // 255)
                        img.putpixel((int(x), int(y)), (blend_r, blend_g, blend_b, a))


def apply_vibe_effects(img, vibe):
    """Apply final vibe-specific effects"""
    try:
        if vibe == 'shadow':
            # Very dark and mysterious
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.6)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.8)
        elif vibe == 'light':
            # Very bright and radiant
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.4)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.3)
        elif vibe == 'cosmic':
            # Deep space contrast
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.5)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.6)
        elif vibe == 'crystal':
            # Sharp and brilliant
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(2.0)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.2)
        elif vibe == 'elemental':
            # Natural and vivid
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.5)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.3)
        else:  # mystical
            # Ethereal and flowing
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.4)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.1)
    except Exception as e:
        print(f"Post-processing warning: {e}")
    
    return img


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint to verify server is working"""
    return jsonify({
        'status': 'ok',
        'message': 'Server is working',
        'available_vibes': ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light']
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'server': 'online',
        'timestamp': str(datetime.now())
    })

@app.route('/status', methods=['GET'])
def status():
    """Status endpoint with detailed information"""
    return jsonify({
        'status': 'operational',
        'server': 'Flask Sigil Generator',
        'version': '4.0',
        'features': ['Dramatically different vibes', 'Unique patterns per input', 'Fixed download'],
        'available_vibes': ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light'],
        'endpoints': ['/generate', '/test', '/health', '/status']
    })


@app.route('/generate', methods=['POST'])
def generate():
    try:
        print("=== GENERATE REQUEST RECEIVED ===")
        
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Request must be JSON'}), 400
            
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
            
        phrase = data.get('phrase', '').strip()
        vibe = data.get('vibe', 'mystical').strip().lower()

        print(f"Received phrase: '{phrase}' with vibe: '{vibe}'")

        if not phrase:
            return jsonify({'success': False, 'error': 'Please enter your intent or desire'})
            
        if len(phrase) > 200:
            return jsonify({'success': False, 'error': 'Phrase too long (max 200 characters)'})

        valid_vibes = ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light']
        if vibe not in valid_vibes:
            vibe = 'mystical'

        print(f"✅ GENERATING SIGIL: '{phrase}' with vibe: '{vibe}'")
        
        try:
            img_base64, error = create_sigil(phrase, vibe, size=400)
            
            if error:
                return jsonify({'success': False, 'error': error})

            if not img_base64:
                return jsonify({'success': False, 'error': 'Failed to generate sigil image'})
                
            print(f"✅ SIGIL GENERATED SUCCESSFULLY")
                
        except Exception as generation_error:
            print(f"GENERATION ERROR: {str(generation_error)}")
            return jsonify({'success': False, 'error': 'Sigil generation failed. Please try again.'})

        response_data = {
            'success': True,
            'image': f'data:image/png;base64,{img_base64}',
            'phrase': phrase,
            'vibe': vibe,
            'timestamp': str(datetime.now())
        }
        
        return jsonify(response_data)
    
    except Exception as e:
        print(f"CRITICAL ERROR in generate endpoint: {str(e)}")
        return jsonify({'success': False, 'error': f'Server error: Please try again'}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
