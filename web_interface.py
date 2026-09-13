#!/usr/bin/env python3
"""
Web Interface for AI Image Generator
Usage: python web_interface.py
Then open http://localhost:5000 in your browser
"""

from flask import Flask, render_template, request, jsonify
from image_generator import AIImageGenerator
import os
import uuid

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Create uploads directory
os.makedirs('static/uploads', exist_ok=True)

generator = AIImageGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '').strip()
    
    if not prompt:
        return jsonify({'success': False, 'error': 'Prompt cannot be empty'}), 400
    
    if len(prompt) > 500:
        return jsonify({'success': False, 'error': 'Prompt too long (max 500 characters)'}), 400
    
    try:
        # Generate unique filename
        unique_id = str(uuid.uuid4())[:8]
        output_path = f'static/uploads/{unique_id}.png'
        
        # Generate image
        success = generator.generate_image(prompt, output_path)
        
        if success:
            return jsonify({
                'success': True,
                'image_url': f'/{output_path}',
                'prompt': prompt
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to generate image'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting AI Image Generator Web Interface")
    print("📱 Open your browser at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop\n")
    app.run(debug=True, port=5000)
