#!/usr/bin/env python3
"""
🎨 AI Image Generator - All-in-One Script
Generate stunning images from text descriptions using Hugging Face API
No API key required! Just run this file.
"""

import requests
from PIL import Image
from io import BytesIO
import os
import sys
from datetime import datetime
import argparse

# ==============================================================================
# CORE IMAGE GENERATOR CLASS
# ==============================================================================

class AIImageGenerator:
    """AI Image Generator using Hugging Face's free inference API"""
    
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
        self.headers = {"Accept": "image/png"}
        
    def generate_image(self, prompt, output_path="generated_image.png"):
        """Generate an image from text description"""
        try:
            print(f"🎨 Generating image for: '{prompt}'")
            print("⏳ This may take 10-30 seconds on first run...\n")
            
            payload = {"inputs": prompt}
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                image_data = Image.open(BytesIO(response.content))
                image_data.save(output_path)
                print(f"✅ Image generated successfully!")
                print(f"📁 Saved to: {output_path}\n")
                return True
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}\n")
                return False
                
        except requests.exceptions.Timeout:
            print("❌ Request timed out. The API might be busy. Try again in a moment.\n")
            return False
        except Exception as e:
            print(f"❌ Error generating image: {str(e)}\n")
            return False
    
    def batch_generate(self, prompts, output_dir="generated_images"):
        """Generate multiple images from a list of prompts"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"🎨 Batch generating {len(prompts)} images...\n")
        
        for i, prompt in enumerate(prompts, 1):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{output_dir}/image_{i}_{timestamp}.png"
            print(f"[{i}/{len(prompts)}] ", end="")
            self.generate_image(prompt, filename)

# ==============================================================================
# WEB INTERFACE (FLASK)
# ==============================================================================

def create_flask_app():
    """Create Flask web application"""
    try:
        from flask import Flask, render_template, request, jsonify
    except ImportError:
        print("❌ Flask not installed. Install with: pip install flask")
        return None
    
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    os.makedirs('static/uploads', exist_ok=True)
    
    generator = AIImageGenerator()
    
    @app.route('/')
    def index():
        return render_template_string(HTML_TEMPLATE)
    
    @app.route('/generate', methods=['POST'])
    def generate():
        data = request.json
        prompt = data.get('prompt', '').strip()
        
        if not prompt:
            return jsonify({'success': False, 'error': 'Prompt cannot be empty'}), 400
        
        if len(prompt) > 500:
            return jsonify({'success': False, 'error': 'Prompt too long (max 500 characters)'}), 400
        
        try:
            import uuid
            unique_id = str(uuid.uuid4())[:8]
            output_path = f'static/uploads/{unique_id}.png'
            success = generator.generate_image(prompt, output_path)
            
            if success:
                return jsonify({'success': True, 'image_url': f'/{output_path}', 'prompt': prompt})
            else:
                return jsonify({'success': False, 'error': 'Failed to generate image'}), 500
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    return app

def run_web_interface():
    """Run the Flask web server"""
    app = create_flask_app()
    if app:
        print("\n🚀 Starting AI Image Generator Web Interface")
        print("📱 Open your browser at: http://localhost:5000")
        print("🛑 Press Ctrl+C to stop\n")
        try:
            app.run(debug=True, port=5000, use_reloader=False)
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down...")

# ==============================================================================
# HTML TEMPLATE FOR WEB INTERFACE
# ==============================================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Image Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            max-width: 800px;
            width: 100%;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            text-align: center;
            font-size: 2.5em;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 0.95em;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 10px;
            color: #555;
            font-weight: 600;
        }
        
        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 1em;
            font-family: inherit;
            resize: vertical;
            min-height: 100px;
            transition: border-color 0.3s;
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        button:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 30px 0;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .result {
            display: none;
            margin-top: 40px;
            text-align: center;
        }
        
        .result img {
            max-width: 100%;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            margin-bottom: 15px;
        }
        
        .prompt-display {
            color: #666;
            font-style: italic;
            margin-bottom: 15px;
        }
        
        .error {
            background-color: #fee;
            border-left: 4px solid #f66;
            color: #c33;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            display: none;
        }
        
        .success {
            background-color: #efe;
            border-left: 4px solid #6f6;
            color: #3c3;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 AI Image Generator</h1>
        <p class="subtitle">Generate stunning images from text descriptions</p>
        
        <div class="error" id="error"></div>
        <div class="success" id="success"></div>
        
        <div class="input-group">
            <label for="prompt">Describe your image:</label>
            <textarea id="prompt" placeholder="Example: A majestic dragon flying over a mystical mountain landscape at sunset"></textarea>
        </div>
        
        <button id="generateBtn" onclick="generateImage()">Generate Image</button>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Creating your masterpiece... This may take a moment ✨</p>
        </div>
        
        <div class="result" id="result">
            <p class="prompt-display">Prompt: <strong id="resultPrompt"></strong></p>
            <img id="resultImage" alt="Generated image">
        </div>
    </div>
    
    <script>
        async function generateImage() {
            const prompt = document.getElementById('prompt').value.trim();
            const generateBtn = document.getElementById('generateBtn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const errorDiv = document.getElementById('error');
            const successDiv = document.getElementById('success');
            
            errorDiv.style.display = 'none';
            successDiv.style.display = 'none';
            result.style.display = 'none';
            
            if (!prompt) {
                errorDiv.textContent = '⚠️ Please enter a description!';
                errorDiv.style.display = 'block';
                return;
            }
            
            if (prompt.length > 500) {
                errorDiv.textContent = '⚠️ Description too long (max 500 characters)';
                errorDiv.style.display = 'block';
                return;
            }
            
            generateBtn.disabled = true;
            loading.style.display = 'block';
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({prompt: prompt})
                });
                
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('resultImage').src = data.image_url;
                    document.getElementById('resultPrompt').textContent = data.prompt;
                    result.style.display = 'block';
                    successDiv.textContent = '✅ Image generated successfully!';
                    successDiv.style.display = 'block';
                } else {
                    throw new Error(data.error || 'Failed to generate image');
                }
            } catch (error) {
                errorDiv.textContent = '❌ Error: ' + error.message;
                errorDiv.style.display = 'block';
            } finally {
                generateBtn.disabled = false;
                loading.style.display = 'none';
            }
        }
        
        document.getElementById('prompt').addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                generateImage();
            }
        });
    </script>
</body>
</html>
"""

# ==============================================================================
# COMMAND LINE INTERFACE
# ==============================================================================

def run_cli():
    """Run command line interface"""
    parser = argparse.ArgumentParser(
        description="🎨 AI Image Generator - Generate images from text descriptions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python all_in_one.py "a futuristic city with flying cars"
  python all_in_one.py "a golden retriever playing in the snow" -o my_dog.png
  python all_in_one.py "magical forest" --batch 5
  python all_in_one.py --web
        """
    )
    
    parser.add_argument("prompt", nargs='?', type=str, help="Description of the image to generate")
    parser.add_argument("-o", "--output", type=str, default="generated_image.png", help="Output file path")
    parser.add_argument("--batch", type=int, help="Generate N variations of the same prompt")
    parser.add_argument("--web", action='store_true', help="Run web interface")
    
    args = parser.parse_args()
    
    if args.web:
        run_web_interface()
    elif not args.prompt:
        parser.print_help()
    else:
        generator = AIImageGenerator()
        if args.batch:
            prompts = [args.prompt] * args.batch
            generator.batch_generate(prompts)
        else:
            generator.generate_image(args.prompt, args.output)

# ==============================================================================
# INTERACTIVE MENU
# ==============================================================================

def run_interactive_menu():
    """Run interactive menu for user selection"""
    print("\n" + "="*60)
    print("🎨 AI IMAGE GENERATOR - ALL IN ONE".center(60))
    print("="*60)
    print("\n Choose an option:\n")
    print("  1️⃣  Generate a single image (enter prompt)")
    print("  2️⃣  Generate multiple images (batch)")
    print("  3️⃣  Open web interface")
    print("  4️⃣  Exit")
    print("\n" + "="*60 + "\n")
    
    generator = AIImageGenerator()
    
    while True:
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            prompt = input("\n📝 Enter image description: ").strip()
            if prompt:
                output = input("📁 Enter output filename (default: generated_image.png): ").strip() or "generated_image.png"
                generator.generate_image(prompt, output)
        
        elif choice == "2":
            try:
                count = int(input("\n📊 How many images? "))
                prompts = []
                for i in range(count):
                    prompt = input(f"  Prompt {i+1}/{count}: ").strip()
                    if prompt:
                        prompts.append(prompt)
                if prompts:
                    output_dir = input("📁 Output directory (default: batch_output): ").strip() or "batch_output"
                    generator.batch_generate(prompts, output_dir)
            except ValueError:
                print("❌ Please enter a valid number.\n")
        
        elif choice == "3":
            run_web_interface()
        
        elif choice == "4":
            print("\n👋 Thanks for using AI Image Generator!\n")
            break
        
        else:
            print("❌ Invalid choice. Please try again.\n")

# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    # Install required packages
    try:
        import requests
        from PIL import Image
    except ImportError:
        print("📦 Installing required packages...")
        os.system("pip install requests pillow")
    
    # Check command line arguments
    if len(sys.argv) > 1:
        # CLI mode
        run_cli()
    else:
        # Interactive menu mode
        run_interactive_menu()
