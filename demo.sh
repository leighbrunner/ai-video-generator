#!/bin/bash
# Demo script to test video generation

echo "🎬 AI Video Generation Demo"
echo "============================"
echo ""

# Activate virtual environment
source venv/bin/activate

echo "Choose a demo:"
echo "1. Text-to-Video: Generate a video of a cat in a cozy room"
echo "2. Image-to-Video: Animate a sample image (requires image path)"
echo "3. Both demos"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🎨 Generating text-to-video..."
        python text_to_video.py "A fluffy cat sitting by a window in a cozy room, warm lighting, peaceful atmosphere" -o demo_text2video.mp4 --steps 30
        ;;
    2)
        read -p "Enter path to image: " image_path
        echo ""
        echo "🎨 Generating image-to-video..."
        python image_to_video.py "$image_path" -o demo_img2video.mp4 --steps 20
        ;;
    3)
        echo ""
        echo "🎨 Generating text-to-video..."
        python text_to_video.py "A fluffy cat sitting by a window in a cozy room, warm lighting, peaceful atmosphere" -o demo_text2video.mp4 --steps 30

        read -p "Enter path to image for image-to-video: " image_path
        echo ""
        echo "🎨 Generating image-to-video..."
        python image_to_video.py "$image_path" -o demo_img2video.mp4 --steps 20
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "✅ Demo complete! Check the output files in this directory."
