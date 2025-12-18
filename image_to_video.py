#!/usr/bin/env python3
"""
Image-to-Video Generation Script
Animates still images into videos using Stable Video Diffusion
"""

import torch
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import load_image, export_to_video
from PIL import Image
import argparse
import os
from datetime import datetime


def resize_image(image: Image.Image, max_size: int = 1024) -> Image.Image:
    """
    Resize image to fit within max_size while maintaining aspect ratio
    Model works best with dimensions that are multiples of 64
    """
    width, height = image.size

    # Calculate new dimensions
    if width > height:
        if width > max_size:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_width = width
            new_height = height
    else:
        if height > max_size:
            new_height = max_size
            new_width = int(width * (max_size / height))
        else:
            new_width = width
            new_height = height

    # Round to nearest multiple of 64
    new_width = (new_width // 64) * 64
    new_height = (new_height // 64) * 64

    return image.resize((new_width, new_height), Image.LANCZOS)


def generate_video(
    image_path: str,
    output_path: str = None,
    num_inference_steps: int = 25,
    num_frames: int = 25,
    fps: int = 7,
    motion_bucket_id: int = 127,
    noise_aug_strength: float = 0.02,
):
    """
    Generate a video from an input image

    Args:
        image_path: Path to the input image
        output_path: Where to save the video (optional, will auto-generate if not provided)
        num_inference_steps: Number of denoising steps (higher = better quality but slower)
        num_frames: Number of frames to generate (14-25 recommended)
        fps: Frames per second for the output video
        motion_bucket_id: Controls amount of motion (higher = more motion, range: 1-255)
        noise_aug_strength: Amount of noise augmentation (range: 0.0-1.0)
    """

    print(f"🎬 Generating video from image: {image_path}")
    print(f"⚙️  Settings: {num_frames} frames @ {fps} FPS, {num_inference_steps} steps")
    print(f"📊 Motion level: {motion_bucket_id}/255, Noise: {noise_aug_strength}")

    # Use CPU for stability with large video models
    # MPS has memory issues with these large models
    device = "cpu"
    print("⚙️  Using CPU (stable for large models)")

    # Load the input image
    print("📸 Loading input image...")
    if image_path.startswith("http"):
        image = load_image(image_path)
    else:
        image = Image.open(image_path).convert("RGB")

    # Resize image to optimal dimensions
    image = resize_image(image)
    print(f"📐 Image size: {image.size[0]}x{image.size[1]}")

    # Load the model
    print("📥 Loading Stable Video Diffusion model...")
    print("⏳ This may take a few minutes on first run...")

    pipe = StableVideoDiffusionPipeline.from_pretrained(
        "stabilityai/stable-video-diffusion-img2vid-xt",
        torch_dtype=torch.float32,
    )

    # Move to device
    pipe = pipe.to(device)

    # Enable memory optimizations
    pipe.enable_attention_slicing()

    print("🎨 Generating video...")

    # Generate the video
    frames = pipe(
        image=image,
        num_inference_steps=num_inference_steps,
        num_frames=num_frames,
        motion_bucket_id=motion_bucket_id,
        noise_aug_strength=noise_aug_strength,
        decode_chunk_size=8,
    ).frames[0]

    # Generate output filename if not provided
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        input_name = os.path.splitext(os.path.basename(image_path))[0]
        output_path = f"output_img2video_{input_name}_{timestamp}.mp4"

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    # Export to video
    print(f"💾 Saving video to: {output_path}")
    export_to_video(frames, output_path, fps=fps)

    print(f"✅ Video generation complete!")
    print(f"📹 Output: {output_path}")

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate videos from images")
    parser.add_argument(
        "image",
        type=str,
        help="Path to input image (local path or URL)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output video file path (default: auto-generated)"
    )
    parser.add_argument(
        "-s", "--steps",
        type=int,
        default=25,
        help="Number of inference steps (default: 25)"
    )
    parser.add_argument(
        "-f", "--frames",
        type=int,
        default=25,
        help="Number of frames (default: 25, range: 14-25)"
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=7,
        help="Frames per second (default: 7)"
    )
    parser.add_argument(
        "-m", "--motion",
        type=int,
        default=127,
        help="Motion amount (default: 127, range: 1-255)"
    )
    parser.add_argument(
        "-n", "--noise",
        type=float,
        default=0.02,
        help="Noise augmentation strength (default: 0.02, range: 0.0-1.0)"
    )

    args = parser.parse_args()

    # Validate inputs
    if args.frames < 14 or args.frames > 25:
        print("⚠️  Warning: num_frames should be between 14-25 for best results")

    if args.motion < 1 or args.motion > 255:
        parser.error("motion must be between 1 and 255")

    if args.noise < 0.0 or args.noise > 1.0:
        parser.error("noise must be between 0.0 and 1.0")

    generate_video(
        image_path=args.image,
        output_path=args.output,
        num_inference_steps=args.steps,
        num_frames=args.frames,
        fps=args.fps,
        motion_bucket_id=args.motion,
        noise_aug_strength=args.noise,
    )


if __name__ == "__main__":
    main()
