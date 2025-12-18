#!/usr/bin/env python3
"""
Text-to-Video Generation Script
Generates videos from text prompts using CogVideoX model
"""

import torch
from diffusers import CogVideoXPipeline
from diffusers.utils import export_to_video
import argparse
import os
from datetime import datetime

# Force CPU only to avoid MPS compatibility issues
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"


def generate_video(
    prompt: str,
    output_path: str = None,
    num_inference_steps: int = 50,
    guidance_scale: float = 6.0,
    num_frames: int = 49,
    fps: int = 8,
):
    """
    Generate a video from a text prompt

    Args:
        prompt: Text description of the video to generate
        output_path: Where to save the video (optional, will auto-generate if not provided)
        num_inference_steps: Number of denoising steps (higher = better quality but slower)
        guidance_scale: How closely to follow the prompt (higher = more faithful to prompt)
        num_frames: Number of frames to generate
        fps: Frames per second for the output video
    """

    print(f"🎬 Generating video from prompt: '{prompt}'")
    print(f"⚙️  Settings: {num_frames} frames @ {fps} FPS, {num_inference_steps} steps")

    # Force CPU only (CogVideoX has MPS compatibility issues)
    torch.set_default_device("cpu")
    device = "cpu"
    torch_dtype = torch.float32
    print("⚙️  Using CPU (stable for large models)")
    print("⏳ This will take 15-45 minutes depending on settings...")

    # Load the model
    print("📥 Loading CogVideoX-2B model...")

    pipe = CogVideoXPipeline.from_pretrained(
        "THUDM/CogVideoX-2b",
        torch_dtype=torch_dtype,
        device_map=None,  # Prevent auto device mapping
    )

    # Move to CPU explicitly
    pipe = pipe.to("cpu")

    print("🎨 Generating video...")

    # Generate the video
    video_frames = pipe(
        prompt=prompt,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        num_frames=num_frames,
    ).frames[0]

    # Generate output filename if not provided
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"output_text2video_{timestamp}.mp4"

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    # Export to video
    print(f"💾 Saving video to: {output_path}")
    export_to_video(video_frames, output_path, fps=fps)

    print(f"✅ Video generation complete!")
    print(f"📹 Output: {output_path}")

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate videos from text prompts")
    parser.add_argument(
        "prompt",
        type=str,
        help="Text description of the video to generate"
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
        default=50,
        help="Number of inference steps (default: 50)"
    )
    parser.add_argument(
        "-g", "--guidance",
        type=float,
        default=6.0,
        help="Guidance scale (default: 6.0)"
    )
    parser.add_argument(
        "-f", "--frames",
        type=int,
        default=49,
        help="Number of frames (default: 49)"
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=8,
        help="Frames per second (default: 8)"
    )

    args = parser.parse_args()

    generate_video(
        prompt=args.prompt,
        output_path=args.output,
        num_inference_steps=args.steps,
        guidance_scale=args.guidance,
        num_frames=args.frames,
        fps=args.fps,
    )


if __name__ == "__main__":
    main()
