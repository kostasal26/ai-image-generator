#!/usr/bin/env python3
"""
Command Line Interface for AI Image Generator
Usage: python cli.py "your image description here"
"""

import sys
import argparse
from image_generator import AIImageGenerator

def main():
    parser = argparse.ArgumentParser(
        description="Generate AI images from text descriptions using Hugging Face API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py "a futuristic city with flying cars"
  python cli.py "a golden retriever playing in the snow" -o my_dog.png
  python cli.py "magical forest" --batch 5
        """
    )
    
    parser.add_argument(
        "prompt",
        type=str,
        help="Description of the image to generate"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="generated_image.png",
        help="Output file path (default: generated_image.png)"
    )
    
    parser.add_argument(
        "--batch",
        type=int,
        help="Generate N variations of the same prompt"
    )
    
    args = parser.parse_args()
    
    generator = AIImageGenerator()
    
    if args.batch:
        # Generate multiple variations
        prompts = [args.prompt] * args.batch
        generator.batch_generate(prompts)
    else:
        # Generate single image
        generator.generate_image(args.prompt, args.output)

if __name__ == "__main__":
    main()
