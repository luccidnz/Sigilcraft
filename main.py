
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
    """Create a sigil image with proper vibe differentiation and return it as base64 encoded string"""
    print(f"🎨 Creating sigil for: '{phrase}' with vibe: '{vibe}' at size: {size}")
    
    original_phrase = phrase
    phrase = phrase.upper()
    phrase = ''.join([c for c in phrase if c in string.ascii_uppercase])
    phrase = ''.join(sorted(set(phrase), key=phrase.index))

    if not phrase:
        return None, "Please enter text with at least one letter"

    print(f"📝 Processed phrase: '{phrase}'")

    # Calculate numerological value
    numerology_value = calculate_numerology(original_phrase)
    print(f"🔢 Numerology value: {numerology_value}")

    # Create vibe-specific seed for different results per vibe
    phrase_seed = abs(hash(original_phrase.lower() + vibe)) % 2147483647
    random.seed(phrase_seed)
    print(f"🌱 Using vibe-specific seed: {phrase_seed} for vibe: {vibe}")

    # Create optimized image size for performance
    img_size = size
    print(f"🖼️ Creating image: {img_size}x{img_size}")
    img = Image.new('RGBA', (img_size, img_size), color=(0, 0, 0, 255))
    draw = ImageDraw.Draw(img)

    center = (img_size // 2, img_size // 2)
    effective_size = img_size // 2

    # Get vibe-specific colors
    vibe_colors = get_vibe_colors(vibe)
    base_colors = get_numerology_colors(numerology_value)
    
    print(f"🎨 Using vibe colors: {vibe_colors}")

    print("🎭 Creating background...")
    create_background(img, draw, center, effective_size, vibe_colors, base_colors, phrase_seed)

    print("⚡ Adding energy fields...")
    create_energy_fields(draw, center, effective_size, vibe_colors, phrase_seed)

    print("📐 Adding sacred geometry...")
    create_sacred_geometry(draw, center, effective_size, vibe_colors, numerology_value, phrase_seed)

    print("🌀 Creating spirals...")
    create_spirals(draw, center, effective_size, vibe_colors, phrase_seed)

    print("⭕ Drawing mystical circles...")
    draw_mystical_circles(draw, center, effective_size, vibe_colors, numerology_value)

    print("🕉️ Creating central mandala...")
    draw_central_mandala(draw, center, effective_size, vibe_colors, numerology_value, phrase_seed)

    print("🔤 Drawing letters...")
    draw_letters(draw, center, effective_size, phrase, vibe_colors)

    print("🎨 Applying post-processing...")
    img = apply_post_processing(img, vibe)

    print("💾 Converting to base64...")
    try:
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG', quality=85, optimize=True)
        img_buffer.seek(0)
        img_data = img_buffer.getvalue()
        img_base64 = base64.b64encode(img_data).decode()
        
        print(f"✅ Image created successfully: {len(img_base64)} characters")
        return img_base64, None
        
    except Exception as e:
        print(f"❌ Error converting image: {str(e)}")
        return None, f"Error creating image: {str(e)}"


def calculate_numerology(text):
    text = text.upper()
    total = 0
    for char in text:
        if 'A' <= char <= 'Z':
            total += ord(char) - ord('A') + 1
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(digit) for digit in str(total))
    return total


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
    """Get distinctly different color palette based on selected vibe"""
    vibe_palettes = {
        'mystical': [(150, 60, 220), (255, 100, 255), (120, 200, 255), (200, 150, 255)],
        'cosmic': [(20, 20, 80), (100, 150, 255), (200, 100, 255), (255, 200, 100), (50, 255, 200)],
        'elemental': [(255, 100, 50), (50, 255, 100), (100, 150, 255), (200, 150, 100), (255, 200, 50)],
        'crystal': [(200, 255, 255), (150, 200, 255), (255, 200, 255), (200, 255, 200), (255, 255, 200)],
        'shadow': [(80, 20, 80), (120, 60, 120), (60, 20, 60), (100, 40, 100), (40, 40, 80)],
        'light': [(255, 255, 200), (255, 200, 150), (200, 255, 200), (255, 220, 255), (255, 255, 150)]
    }
    return vibe_palettes.get(vibe, vibe_palettes['mystical'])


def create_background(img, draw, center, size, vibe_colors, base_colors, seed):
    """Create background with vibe-specific patterns"""
    random.seed(seed)
    
    # Create gradient background based on vibe
    for y in range(size * 2):
        for x in range(size * 2):
            # Distance from center
            dist = math.sqrt((x - center[0])**2 + (y - center[1])**2)
            
            # Vibe-specific noise pattern
            noise_freq = 0.01 + (seed % 100) * 0.0001
            noise1 = math.sin(x * noise_freq) * math.cos(y * noise_freq)
            noise2 = math.sin(dist * noise_freq * 0.5)
            
            # Select vibe color based on position
            color_index = int((noise1 + noise2 + 2) * len(vibe_colors) / 4) % len(vibe_colors)
            vibe_color = vibe_colors[color_index]
            
            # Mix with base color
            intensity = max(0.2, 0.8 - dist / (size * 1.5))
            
            r = int(vibe_color[0] * intensity + base_colors[0] * (1 - intensity) * 0.3)
            g = int(vibe_color[1] * intensity + base_colors[1] * (1 - intensity) * 0.3)
            b = int(vibe_color[2] * intensity + base_colors[2] * (1 - intensity) * 0.3)
            
            # Clamp values
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            img.putpixel((x, y), (r, g, b, 255))


def create_energy_fields(draw, center, size, vibe_colors, seed):
    """Create energy field patterns specific to each vibe"""
    random.seed(seed)
    
    field_count = 8 + (seed % 6)
    
    for field in range(field_count):
        radius = size * (0.3 + field * 0.08)
        particles = 20 + field * 4
        
        for particle in range(particles):
            angle = (2 * math.pi * particle) / particles + field * 0.5
            
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            
            # Vibe-specific particle behavior
            color_index = (field + particle) % len(vibe_colors)
            color = vibe_colors[color_index]
            
            particle_size = max(2, 8 - field)
            alpha = max(80, 200 - field * 20)
            
            particle_color = (*color, alpha)
            
            try:
                draw.ellipse([x - particle_size, y - particle_size, 
                            x + particle_size, y + particle_size], 
                           fill=particle_color)
            except:
                pass


def create_sacred_geometry(draw, center, size, vibe_colors, numerology_value, seed):
    """Create sacred geometry patterns"""
    random.seed(seed)
    
    geometry_layers = min(6, 3 + (seed % 4))
    
    for layer in range(geometry_layers):
        layer_radius = size * (0.6 - layer * 0.08)
        pattern_count = 6 + layer * 3
        
        for i in range(pattern_count):
            angle = (2 * math.pi * i) / pattern_count + layer * 0.4
            
            x = center[0] + layer_radius * math.cos(angle)
            y = center[1] + layer_radius * math.sin(angle)
            
            color_index = (layer + i) % len(vibe_colors)
            color = vibe_colors[color_index]
            
            if numerology_value % 3 == 0:  # Triangles
                size_factor = max(8, 20 - layer * 2)
                points = []
                for tri in range(3):
                    tri_angle = angle + (tri * 2 * math.pi / 3)
                    tri_x = x + size_factor * math.cos(tri_angle)
                    tri_y = y + size_factor * math.sin(tri_angle)
                    points.append((tri_x, tri_y))
                
                try:
                    draw.polygon(points, fill=(*color, 150))
                except:
                    pass
                    
            elif numerology_value % 4 == 0:  # Squares
                size_factor = max(6, 16 - layer * 2)
                try:
                    draw.rectangle([x - size_factor, y - size_factor,
                                  x + size_factor, y + size_factor],
                                 fill=(*color, 150))
                except:
                    pass
            else:  # Circles
                size_factor = max(4, 12 - layer)
                try:
                    draw.ellipse([x - size_factor, y - size_factor,
                                x + size_factor, y + size_factor],
                               fill=(*color, 150))
                except:
                    pass


def create_spirals(draw, center, size, vibe_colors, seed):
    """Create spiral energy patterns"""
    random.seed(seed)
    
    spiral_count = 3 + (seed % 3)
    
    for spiral_idx in range(spiral_count):
        direction = 1 if spiral_idx % 2 == 0 else -1
        start_angle = spiral_idx * 120
        
        spiral_points = []
        current_radius = size * 0.1
        
        for step in range(0, 720, 12):  # Reduced steps for performance
            angle = start_angle + (step * direction)
            
            x = center[0] + current_radius * math.cos(math.radians(angle))
            y = center[1] + current_radius * math.sin(math.radians(angle))
            
            spiral_points.append((x, y))
            current_radius += size * 0.004
            
            if current_radius > size * 0.8:
                break
        
        # Draw spiral
        color_index = spiral_idx % len(vibe_colors)
        color = vibe_colors[color_index]
        
        for i in range(len(spiral_points) - 1):
            try:
                draw.line([spiral_points[i], spiral_points[i + 1]], 
                         fill=(*color, 180), width=3)
            except:
                pass


def draw_mystical_circles(draw, center, size, vibe_colors, numerology_value):
    """Draw mystical circles with vibe-specific styling"""
    circle_count = min(12, max(6, numerology_value * 2))
    
    for circle_idx in range(circle_count):
        radius = size * (0.9 - circle_idx * 0.06)
        if radius <= 4:
            break
            
        color_index = circle_idx % len(vibe_colors)
        color = vibe_colors[color_index]
        
        thickness = max(1, 6 - circle_idx // 2)
        alpha = max(60, 180 - circle_idx * 12)
        
        try:
            draw.ellipse([center[0] - radius, center[1] - radius,
                        center[0] + radius, center[1] + radius],
                       outline=(*color, alpha), width=thickness)
        except:
            pass


def draw_central_mandala(draw, center, size, vibe_colors, numerology_value, seed):
    """Draw central mandala pattern"""
    random.seed(seed)
    
    mandala_radius = size // 3
    pattern_points = 8 + numerology_value
    
    # Create mandala points
    mandala_points = []
    for i in range(pattern_points):
        angle = (2 * math.pi * i) / pattern_points
        x = center[0] + mandala_radius * math.cos(angle)
        y = center[1] + mandala_radius * math.sin(angle)
        mandala_points.append((x, y))
    
    # Connect points in patterns
    connection_step = max(1, pattern_points // numerology_value)
    
    for i in range(pattern_points):
        start_point = mandala_points[i]
        end_point = mandala_points[(i + connection_step) % pattern_points]
        
        color_index = i % len(vibe_colors)
        color = vibe_colors[color_index]
        
        try:
            draw.line([start_point, end_point], fill=(*color, 200), width=2)
        except:
            pass
        
        # Add nodes at connection points
        try:
            draw.ellipse([start_point[0] - 4, start_point[1] - 4,
                        start_point[0] + 4, start_point[1] + 4],
                       fill=(*color, 255))
        except:
            pass


def draw_letters(draw, center, size, phrase, vibe_colors):
    """Draw letters with vibe-specific styling"""
    try:
        font = ImageFont.truetype("arial.ttf", max(16, size // 15))
    except:
        font = ImageFont.load_default()

    radius = size * 0.35
    angle_step = 360 / len(phrase)
    points = []

    for i, letter in enumerate(phrase):
        angle = math.radians(i * angle_step - 90)
        
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)

        # Get text size for centering
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        letter_x = x - text_width // 2
        letter_y = y - text_height // 2

        # Vibe-specific letter color
        color_index = i % len(vibe_colors)
        color = vibe_colors[color_index]

        # Glow effect
        for glow in range(3, 0, -1):
            glow_alpha = 60 - glow * 15
            glow_color = (*color, glow_alpha)
            
            for dx in range(-glow, glow + 1):
                for dy in range(-glow, glow + 1):
                    if dx != 0 or dy != 0:
                        try:
                            draw.text((letter_x + dx, letter_y + dy), 
                                    letter, font=font, fill=glow_color)
                        except:
                            pass

        # Main letter
        try:
            draw.text((letter_x, letter_y), letter, font=font, 
                     fill=(*color, 255))
        except:
            pass
        
        points.append((x, y))

    # Connect letters
    if len(points) > 1:
        for i in range(len(points)):
            start_point = points[i]
            end_point = points[(i + 1) % len(points)]
            
            color_index = i % len(vibe_colors)
            color = vibe_colors[color_index]
            
            try:
                draw.line([start_point, end_point], fill=(*color, 150), width=2)
            except:
                pass


def apply_post_processing(img, vibe):
    """Apply vibe-specific post-processing effects"""
    try:
        if vibe == 'shadow':
            # Darker, more mysterious
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.8)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.4)
        elif vibe == 'light':
            # Brighter, more radiant
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.3)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.2)
        elif vibe == 'cosmic':
            # Enhanced contrast and saturation
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.3)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.4)
        elif vibe == 'crystal':
            # Sharp and clear
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.5)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.1)
        else:
            # Standard enhancement
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.2)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.3)
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
        'version': '3.1',
        'features': ['Fast rendering', 'Vibe differentiation', 'Optimized performance'],
        'available_vibes': ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light'],
        'endpoints': ['/generate', '/test', '/health', '/status']
    })


@app.route('/generate', methods=['POST'])
def generate():
    try:
        print("=== GENERATE REQUEST RECEIVED ===")
        
        # Validate request
        if not request.is_json:
            print("ERROR: Request is not JSON")
            return jsonify({
                'success': False,
                'error': 'Request must be JSON'
            }), 400
            
        data = request.json
        if not data:
            print("ERROR: No data provided")
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
            
        phrase = data.get('phrase', '').strip()
        vibe = data.get('vibe', 'mystical').strip().lower()

        print(f"Received phrase: '{phrase}'")
        print(f"Received vibe: '{vibe}'")

        # Validate phrase
        if not phrase:
            print("ERROR: No phrase provided")
            return jsonify({
                'success': False,
                'error': 'Please enter your intent or desire'
            })
            
        if len(phrase) > 200:
            print(f"ERROR: Phrase too long ({len(phrase)} characters)")
            return jsonify({
                'success': False,
                'error': 'Phrase too long (max 200 characters)'
            })

        # Validate vibe
        valid_vibes = ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light']
        if vibe not in valid_vibes:
            print(f"WARNING: Invalid vibe '{vibe}', defaulting to 'mystical'")
            vibe = 'mystical'

        print(f"✅ GENERATING SIGIL: '{phrase}' with vibe: '{vibe}'")
        print("🎨 Starting optimized image generation...")
        
        # Generate sigil with optimized performance
        try:
            img_base64, error = create_sigil(phrase, vibe, size=400)  # Optimized size
            
            if error:
                print(f"ERROR: Sigil creation failed: {error}")
                return jsonify({
                    'success': False,
                    'error': error
                })

            if not img_base64:
                print("ERROR: No image data generated")
                return jsonify({
                    'success': False,
                    'error': 'Failed to generate sigil image'
                })
                
            print(f"✅ IMAGE GENERATED: {len(img_base64)} bytes")
                
        except MemoryError as me:
            print(f"MEMORY ERROR: {str(me)}")
            return jsonify({
                'success': False,
                'error': 'Insufficient memory to generate sigil. Please try a shorter phrase.'
            })
            
        except Exception as generation_error:
            print(f"GENERATION ERROR: {str(generation_error)}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': 'Sigil generation failed. Please try again.'
            })

        print("✅ SIGIL GENERATED SUCCESSFULLY")
        
        # Return response with success flag
        response_data = {
            'success': True,
            'image': f'data:image/png;base64,{img_base64}',
            'phrase': phrase,
            'vibe': vibe,
            'timestamp': str(datetime.now())
        }
        
        print("✅ RESPONSE PREPARED, SENDING...")
        print(f"📊 Response size: ~{len(str(response_data))} characters")
        return jsonify(response_data)
    
    except Exception as e:
        print(f"CRITICAL ERROR in generate endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Server error: Please try again'
        }), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
