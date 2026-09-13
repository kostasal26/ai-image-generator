import requests
from PIL import Image
from io import BytesIO
import os
from datetime import datetime

class AIImageGenerator:
    """
    AI Image Generator using Hugging Face's free inference API
    No API key required - uses free tier access
    """
    
    def __init__(self):
        # Using Hugging Face's free inference API (no key needed)
        self.api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
        self.headers = {"Accept": "image/png"}
        # Alternative models you can use:
        # - stabilityai/stable-diffusion-2-1
        # - runwayml/stable-diffusion-v1-5
        # - Lykon/DreamShaper
        
    def generate_image(self, prompt, output_path="generated_image.png"):
        """
        Generate an image from text description
        
        Args:
            prompt (str): Description of the image to generate
            output_path (str): Where to save the generated image
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"🎨 Generating image for: '{prompt}'")
            print("⏳ This may take 10-30 seconds on first run...")
            
            payload = {"inputs": prompt}
            
            # Make request to Hugging Face API
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=60)
            
            # Check if request was successful
            if response.status_code == 200:
                # Save the image
                image_data = Image.open(BytesIO(response.content))
                image_data.save(output_path)
                print(f"✅ Image generated successfully!")
                print(f"📁 Saved to: {output_path}")
                return True
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            print("❌ Request timed out. The API might be busy. Try again in a moment.")
            return False
        except Exception as e:
            print(f"❌ Error generating image: {str(e)}")
            return False
    
    def batch_generate(self, prompts, output_dir="generated_images"):
        """
        Generate multiple images from a list of prompts
        
        Args:
            prompts (list): List of text descriptions
            output_dir (str): Directory to save all images
        """
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"🎨 Batch generating {len(prompts)} images...\n")
        
        for i, prompt in enumerate(prompts, 1):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{output_dir}/image_{i}_{timestamp}.png"
            print(f"[{i}/{len(prompts)}] ", end="")
            self.generate_image(prompt, filename)
            print()


if __name__ == "__main__":
    # Example usage
    generator = AIImageGenerator()
    
    # Single image generation
    prompt = "A serene landscape with mountains, lake, and sunset"
    generator.generate_image(prompt, "my_generated_image.png")
