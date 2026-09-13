#!/usr/bin/env python3
"""
Example: Batch image generation
Generates multiple images from different prompts
"""

from image_generator import AIImageGenerator

# Initialize generator
generator = AIImageGenerator()

# List of prompts to generate
prompts = [
    "A serene Japanese garden with cherry blossoms",
    "A futuristic cyberpunk city with neon lights",
    "An underwater coral palace with bioluminescent creatures",
    "A steampunk robot in a Victorian factory",
    "A magical forest with floating islands and waterfalls",
]

print("🎨 Starting batch image generation...\n")
print(f"📊 Total images to generate: {len(prompts)}\n")

# Generate all images
generator.batch_generate(prompts, output_dir="batch_output")

print("\n✅ Batch generation complete!")
print("📁 All images saved to 'batch_output' directory")
