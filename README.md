# AI Video Generation Studio 🎬

A complete toolkit for generating videos using state-of-the-art AI models. Supports both text-to-video and image-to-video generation, optimized for Apple Silicon (M1/M2/M3/M4) with MPS acceleration.

## Features

- **Text-to-Video**: Generate videos from text descriptions using CogVideoX-2B
- **Image-to-Video**: Animate still images using Stable Video Diffusion
- **Apple Silicon Optimized**: Automatic MPS acceleration for faster generation
- **Easy to Use**: Simple command-line interface with sensible defaults
- **Flexible**: Customizable parameters for fine-tuning output

## Installation

### Prerequisites

- Python 3.12+
- macOS with Apple Silicon (M1/M2/M3/M4) recommended
- ~10GB free disk space for models
- 16GB+ RAM recommended

### Setup

1. **Clone or navigate to this directory**

2. **Create and activate virtual environment** (already done):
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies** (already done):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Text-to-Video Generation

Generate videos from text prompts using the CogVideoX model:

```bash
python text_to_video.py "A cat playing piano in a jazz club, cinematic lighting"
```

#### Examples:

```bash
# Basic usage
python text_to_video.py "A serene lake at sunset with mountains in the background"

# Custom output path
python text_to_video.py "A futuristic city with flying cars" -o videos/city.mp4

# High quality (more steps)
python text_to_video.py "A dragon flying through clouds" --steps 100

# More frames for longer video
python text_to_video.py "Ocean waves crashing on rocks" --frames 73 --fps 24

# Adjust guidance for prompt adherence
python text_to_video.py "A robot dancing" --guidance 8.0
```

#### Options:

- `-o, --output`: Output file path (default: auto-generated timestamp)
- `-s, --steps`: Number of inference steps (default: 50, higher = better quality)
- `-g, --guidance`: Guidance scale (default: 6.0, higher = more prompt adherence)
- `-f, --frames`: Number of frames (default: 49)
- `--fps`: Frames per second (default: 8)

### Image-to-Video Generation

Animate still images using Stable Video Diffusion:

```bash
python image_to_video.py path/to/your/image.jpg
```

#### Examples:

```bash
# Basic usage
python image_to_video.py photo.jpg

# From URL
python image_to_video.py "https://example.com/image.jpg"

# Custom output
python image_to_video.py photo.jpg -o animated_photo.mp4

# More motion
python image_to_video.py photo.jpg --motion 200

# Longer video with higher FPS
python image_to_video.py photo.jpg --frames 25 --fps 15

# Fine-tune noise level
python image_to_video.py photo.jpg --noise 0.05
```

#### Options:

- `-o, --output`: Output file path (default: auto-generated)
- `-s, --steps`: Number of inference steps (default: 25)
- `-f, --frames`: Number of frames (default: 25, range: 14-25)
- `--fps`: Frames per second (default: 7)
- `-m, --motion`: Motion amount (default: 127, range: 1-255, higher = more motion)
- `-n, --noise`: Noise augmentation (default: 0.02, range: 0.0-1.0)

## Models Used

### CogVideoX-2B (Text-to-Video)
- **Model**: THUDM/CogVideoX-2b
- **Size**: ~5GB
- **Quality**: High-quality text-to-video generation
- **Speed**: ~2-5 minutes per video on Apple Silicon (depending on settings)

### Stable Video Diffusion (Image-to-Video)
- **Model**: stabilityai/stable-video-diffusion-img2vid-xt
- **Size**: ~4GB
- **Quality**: Smooth, high-quality image animation
- **Speed**: ~1-3 minutes per video on Apple Silicon

## Tips for Best Results

### Text-to-Video:
- Be descriptive and specific in your prompts
- Include style keywords like "cinematic", "realistic", "artistic"
- Mention lighting, camera angles, and mood
- Keep prompts focused on one main subject/action
- Use 50-100 steps for best quality
- Higher guidance scale (7-9) for more prompt adherence

### Image-to-Video:
- Use high-quality input images (1024px recommended)
- Images with clear subjects work best
- Adjust motion parameter: 50-100 for subtle, 150-255 for dramatic
- Lower noise (0.01-0.02) for smoother motion
- 14-18 frames for subtle animation, 20-25 for more movement

## Performance Notes

- **First Run**: Models will be downloaded automatically (~9GB total)
- **Apple Silicon (M1/M2/M3)**: 2-5 minutes per video with MPS acceleration
- **Intel Mac**: 10-30+ minutes per video using CPU
- **Memory**: 8GB+ RAM recommended, 16GB+ for best performance

## Troubleshooting

### Out of Memory
- Reduce number of frames
- Lower inference steps
- Close other applications
- For text-to-video: reduce to 25 frames
- For image-to-video: reduce to 14 frames

### Slow Generation
- Ensure virtual environment is activated
- Check that MPS is being used (look for "Using MPS" message)
- Reduce inference steps for faster (but lower quality) output
- First run is slower due to model compilation

### Model Download Issues
- Ensure stable internet connection
- Models auto-download on first use (~9GB)
- Check available disk space (need ~15GB free)

## Advanced Usage

### Python API

You can import and use the functions in your own scripts:

```python
from text_to_video import generate_video as text_to_video
from image_to_video import generate_video as image_to_video

# Generate from text
video_path = text_to_video(
    prompt="A beautiful sunset over mountains",
    num_inference_steps=50,
    guidance_scale=7.0
)

# Generate from image
video_path = image_to_video(
    image_path="photo.jpg",
    motion_bucket_id=150,
    num_frames=25
)
```

## License

This project uses open-source models:
- CogVideoX: Apache 2.0 License
- Stable Video Diffusion: Stability AI License

## Credits

- **CogVideoX**: Tsinghua University (THUDM)
- **Stable Video Diffusion**: Stability AI
- **Diffusers Library**: Hugging Face

## Support

For issues or questions:
1. Check the troubleshooting section
2. Ensure all dependencies are installed
3. Verify Python version (3.12+)
4. Check available disk space and memory

---

**Ready to create amazing AI videos!** 🚀

Start with simple prompts and experiment with different settings to find what works best for your use case.
