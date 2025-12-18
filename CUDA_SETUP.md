# GTX 3080 Setup Instructions

## Prompt for Claude Code on GTX 3080 Machine:

```
Clone the repo https://github.com/leighbrunner/ai-video-generator and set it up for CUDA/GPU acceleration on this machine with GTX 3080.

Requirements:
1. Modify the scripts to use CUDA instead of CPU/MPS
2. Install PyTorch with CUDA support (cu121)
3. Use float16 for faster generation
4. Add CUDA-specific optimizations
5. Test that GPU is being used

After setup, generate a high-quality video using text-to-video with this prompt:
"A majestic dragon with shimmering scales flying through dramatic storm clouds, lightning illuminating the scene, cinematic aerial shot, epic fantasy atmosphere, volumetric lighting, highly detailed"

Use settings: 50 steps, 49 frames, guidance 7.0
```

## What This Will Do:

The setup will:
- Install CUDA-enabled PyTorch (~2GB)
- Download CogVideoX-2B model (~5GB)
- Optimize scripts for GPU execution
- Generate a ~6 second video in 2-5 minutes (vs 30-60 minutes on CPU)

## Expected Performance:

| Generation Type | CPU (Mac) | GTX 3080 |
|----------------|-----------|----------|
| Text-to-video (49 frames) | 30-60 min | 2-5 min |
| Image-to-video (25 frames) | 10-30 min | 1-3 min |

## Manual Setup (if needed):

```bash
# Clone repo
git clone https://github.com/leighbrunner/ai-video-generator.git
cd ai-video-generator

# Create venv
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install CUDA PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install other dependencies
pip install diffusers transformers accelerate opencv-python imageio imageio-ffmpeg safetensors sentencepiece protobuf

# Verify CUDA
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0)}')"

# Generate video
python text_to_video.py "A majestic dragon flying through storm clouds" -o dragon.mp4 --steps 50
```
