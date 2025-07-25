
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
    phrase = phrase.upper()
    phrase = ''.join([c for c in phrase if c in string.ascii_uppercase])
    phrase = ''.join(sorted(set(phrase), key=phrase.index))
    
    if not phrase:
        return None, "Please enter text with at least one letter"

    # Create image with anti-aliasing
    img = Image.new('RGBA', (size * 2, size * 2), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center = (size, size)  # Center for 2x size
    
    # Create gradient background
    for y in range(size * 2):
        for x in range(size * 2):
            # Distance from center for radial gradient
            dist = math.sqrt((x - center[0])**2 + (y - center[1])**2)
            max_dist = math.sqrt(2) * size
            
            # Multi-layered gradient
            gradient_factor = 1 - (dist / max_dist)
            
            # Create mystical purple-blue gradient
            r = int(20 + gradient_factor * 40 + 30 * math.sin(dist * 0.01))
            g = int(10 + gradient_factor * 60 + 40 * math.sin(dist * 0.008 + 1))
            b = int(40 + gradient_factor * 100 + 50 * math.sin(dist * 0.012 + 2))
            
            # Add some sparkle effect
            noise = hash((x, y)) % 256
            if noise > 250:
                r = min(255, r + 100)
                g = min(255, g + 100)
                b = min(255, b + 100)
            
            img.putpixel((x, y), (r, g, b, 255))
    
    # Draw outer mystical circle
    outer_radius = size * 0.9
    for thickness in range(8):
        circle_radius = outer_radius - thickness * 3
        alpha = 255 - thickness * 30
        color = (200 + thickness * 5, 150 + thickness * 10, 255, alpha)
        
        # Draw circle outline
        draw.ellipse([
            center[0] - circle_radius, center[1] - circle_radius,
            center[0] + circle_radius, center[1] + circle_radius
        ], outline=color, width=2)
    
    # Draw geometric patterns
    num_triangles = 12
    for i in range(num_triangles):
        angle = (2 * math.pi * i) / num_triangles
        triangle_radius = size * 0.7
        
        # Calculate triangle points
        x1 = center[0] + triangle_radius * math.cos(angle)
        y1 = center[1] + triangle_radius * math.sin(angle)
        x2 = center[0] + triangle_radius * 0.8 * math.cos(angle + 0.2)
        y2 = center[1] + triangle_radius * 0.8 * math.sin(angle + 0.2)
        x3 = center[0] + triangle_radius * 0.8 * math.cos(angle - 0.2)
        y3 = center[1] + triangle_radius * 0.8 * math.sin(angle - 0.2)
        
        color_intensity = 100 + (i * 10) % 155
        triangle_color = (color_intensity, color_intensity + 50, 255, 120)
        
        draw.polygon([(x1, y1), (x2, y2), (x3, y3)], fill=triangle_color)

    # Create multiple concentric circles with letter positioning
    try:
        font_size = max(30, size//10)
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Position letters in multiple rings
    num_letters = len(phrase)
    rings = min(3, max(1, num_letters // 4 + 1))
    letters_per_ring = num_letters // rings
    remaining_letters = num_letters % rings
    
    letter_index = 0
    connection_points = []
    
    for ring in range(rings):
        ring_radius = size * (0.3 + 0.15 * ring)
        letters_in_this_ring = letters_per_ring + (1 if ring < remaining_letters else 0)
        
        if letters_in_this_ring == 0:
            continue
            
        angle_step = 360 / letters_in_this_ring
        ring_points = []
        
        for i in range(letters_in_this_ring):
            if letter_index >= num_letters:
                break
                
            letter = phrase[letter_index]
            angle = math.radians(i * angle_step - 90)
            x = center[0] + ring_radius * math.cos(angle)
            y = center[1] + ring_radius * math.sin(angle)
            
            # Create glowing effect for letters
            glow_colors = [
                (255, 100, 100, 180),  # Red glow
                (100, 255, 100, 180),  # Green glow
                (100, 100, 255, 180),  # Blue glow
                (255, 255, 100, 180),  # Yellow glow
                (255, 100, 255, 180),  # Magenta glow
                (100, 255, 255, 180),  # Cyan glow
            ]
            
            glow_color = glow_colors[letter_index % len(glow_colors)]
            
            # Draw letter glow
            for glow_offset in range(8, 0, -1):
                glow_alpha = 30 - glow_offset * 3
                glow_size = font_size + glow_offset * 2
                try:
                    glow_font = ImageFont.truetype("arial.ttf", glow_size)
                except:
                    glow_font = font
                    
                bbox = draw.textbbox((0, 0), letter, font=glow_font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                glow_x = x - text_width//2
                glow_y = y - text_height//2
                
                # Create temporary image for glow
                glow_img = Image.new('RGBA', (text_width + 20, text_height + 20), (0, 0, 0, 0))
                glow_draw = ImageDraw.Draw(glow_img)
                glow_draw.text((10, 10), letter, font=glow_font, fill=(*glow_color[:3], glow_alpha))
                
                img.paste(glow_img, (int(glow_x - 10), int(glow_y - 10)), glow_img)
            
            # Draw main letter
            bbox = draw.textbbox((0, 0), letter, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            letter_x = x - text_width//2
            letter_y = y - text_height//2
            
            draw.text((letter_x, letter_y), letter, font=font, fill=(255, 255, 255, 255))
            
            ring_points.append((x, y))
            connection_points.append((x, y))
            letter_index += 1
        
        # Connect letters within the ring
        if len(ring_points) > 1:
            ring_color = glow_colors[ring % len(glow_colors)]
            for i in range(len(ring_points)):
                start_point = ring_points[i]
                end_point = ring_points[(i + 1) % len(ring_points)]
                draw.line([start_point, end_point], fill=ring_color, width=3)
    
    # Create mystical connections between rings
    if len(connection_points) > 2:
        # Draw complex geometric patterns connecting all points
        center_point = (center[0], center[1])
        
        # Star pattern from center
        for point in connection_points[::2]:  # Every other point
            connection_color = (255, 200, 100, 200)
            draw.line([center_point, point], fill=connection_color, width=2)
        
        # Pentagram-like connections
        num_points = len(connection_points)
        for i in range(num_points):
            start_idx = i
            end_idx = (i + num_points // 3) % num_points
            
            start_point = connection_points[start_idx]
            end_point = connection_points[end_idx]
            
            connection_color = (150, 255, 200, 150)
            draw.line([start_point, end_point], fill=connection_color, width=2)
    
    # Add central mystical symbol
    symbol_size = size // 8
    symbol_points = []
    for i in range(8):
        angle = (2 * math.pi * i) / 8
        x = center[0] + symbol_size * math.cos(angle)
        y = center[1] + symbol_size * math.sin(angle)
        symbol_points.append((x, y))
    
    # Draw octagram (8-pointed star)
    for i in range(0, 8, 2):
        start_point = symbol_points[i]
        end_point = symbol_points[(i + 4) % 8]
        draw.line([start_point, end_point], fill=(255, 255, 255, 200), width=4)
    
    # Resize back to original size with high-quality resampling
    img = img.resize((size, size), Image.LANCZOS)
    
    # Convert to base64
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    
    return img_base64, None

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
