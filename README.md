# 🎨 AI Image Generator

Generate stunning AI images from text descriptions using Hugging Face's free inference API. **No API key required!**

## ✨ Features

- 🎨 **Text-to-Image Generation** - Describe any image, and AI will create it
- 🚀 **Three Ways to Use**: Python script, CLI, or Web interface
- 🆓 **Free** - Uses Hugging Face's free tier (no sign-up needed!)
- ⚡ **Fast** - Generate images in seconds
- 📁 **Batch Processing** - Generate multiple images at once
- 🌐 **Web UI** - Beautiful web interface included

## 📋 Requirements

- Python 3.7+
- Internet connection
- ~100MB disk space

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/kostasal26/ai-image-generator.git
cd ai-image-generator

# Install dependencies
pip install -r requirements.txt
```

## 💻 Usage

### Option 1: Web Interface (Easiest)

```bash
pip install flask
python web_interface.py
```

Then open **http://localhost:5000** in your browser!

### Option 2: Command Line (CLI)

```bash
# Generate a single image
python cli.py "a futuristic city with flying cars"

# Save to specific location
python cli.py "a golden retriever in the snow" -o my_dog.png

# Generate 5 variations
python cli.py "magical forest" --batch 5
```

### Option 3: Python Script

```python
from image_generator import AIImageGenerator

generator = AIImageGenerator()

# Single image
generator.generate_image("a serene landscape with mountains and lake", "output.png")

# Batch generation
prompts = [
    "futuristic robot",
    "underwater city",
    "floating islands"
]
generator.batch_generate(prompts, output_dir="my_images")
```

## 📖 Examples

### Amazing Prompts to Try:

```
"A serene Japanese garden with cherry blossoms and a wooden bridge"
"A steampunk airship flying through clouds at sunset"
"A cozy cyberpunk cafe with neon signs and rain"
"An underwater coral city with bioluminescent creatures"
"A dragon made of stained glass"
"A library in a magical forest with floating books"
"An alien marketplace with exotic creatures trading items"
```

## 🔧 How It Works

1. **Text Processing** - Your description is sent to Hugging Face API
2. **AI Model** - Uses Stable Diffusion v1.5 to generate image
3. **Image Creation** - AI renders a unique image based on your prompt
4. **Delivery** - Image is downloaded and saved to your computer

## ⚙️ Configuration

Edit `image_generator.py` to use different models:

```python
# Available models:
# "runwayml/stable-diffusion-v1-5"        (default - fastest)
# "stabilityai/stable-diffusion-2-1"      (higher quality)
# "Lykon/DreamShaper"                     (artistic)

self.api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
```

## ⏱️ Generation Time

- **First run**: 30-60 seconds (model loads)
- **Subsequent runs**: 10-30 seconds
- Time depends on API server load

## 🎯 Tips for Better Results

✅ **Good prompts:**
- "A painting of a sunset over mountains"
- "Photography of a futuristic city, 8k, detailed"
- "A steampunk robot in the style of Victorian era"

❌ **Avoid:**
- Very short descriptions ("car")
- Conflicting descriptions ("bright and dark")
- Prompts longer than 500 characters

## 🆓 No API Key?

Yes! This project uses:
- **Hugging Face's free inference API** (no sign-up required)
- **Open-source Stable Diffusion model** (free to use)
- **No hidden costs** - completely free

## 📊 Limitations

- API server load may cause slower response times
- Rate limited to ~10-15 requests per minute per IP
- Generated images are public (use responsibly)
- NSFW content is filtered

## 🚀 Advanced Usage

### Running as a Background Service

```bash
# Unix/Linux/Mac
nohup python web_interface.py > output.log 2>&1 &

# Windows
start python web_interface.py
```

### Docker Support

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "web_interface.py"]
```

```bash
docker build -t ai-image-gen .
docker run -p 5000:5000 ai-image-gen
```

## 🐛 Troubleshooting

**Q: "API is overloaded" error?**
A: The free API has limits. Wait a minute and try again.

**Q: Generated images are blank/black?**
A: Try a more descriptive prompt. Be more specific!

**Q: Very slow generation?**
A: First run is slow (model loading). Subsequent runs are faster. If consistently slow, the API server is busy.

**Q: "ModuleNotFoundError"?**
A: Run `pip install -r requirements.txt`

## 📚 Learn More

- [Hugging Face Models](https://huggingface.co/models)
- [Stable Diffusion Documentation](https://huggingface.co/docs/diffusers/using-diffusers/conditional_image_generation)
- [Prompt Engineering Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)

## 📄 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Found a bug? Have an idea? Create an issue or pull request!

## ⭐ Show Your Support

If you like this project, please star it! ⭐

---

**Made with ❤️ by kostasal26**

*Generate amazing images with AI - no API key required!*
