#!/usr/bin/env python3
"""
Quick test to verify the video generation setup is working
"""

import sys
import torch


def test_imports():
    """Test that all required libraries are installed"""
    print("🔍 Testing imports...")

    try:
        import diffusers
        print(f"✅ diffusers: {diffusers.__version__}")
    except ImportError as e:
        print(f"❌ diffusers: {e}")
        return False

    try:
        import transformers
        print(f"✅ transformers: {transformers.__version__}")
    except ImportError as e:
        print(f"❌ transformers: {e}")
        return False

    try:
        import accelerate
        print(f"✅ accelerate: {accelerate.__version__}")
    except ImportError as e:
        print(f"❌ accelerate: {e}")
        return False

    try:
        import cv2
        print(f"✅ opencv-python: {cv2.__version__}")
    except ImportError as e:
        print(f"❌ opencv-python: {e}")
        return False

    try:
        import imageio
        print(f"✅ imageio: {imageio.__version__}")
    except ImportError as e:
        print(f"❌ imageio: {e}")
        return False

    return True


def test_pytorch():
    """Test PyTorch and device availability"""
    print("\n🔍 Testing PyTorch...")

    print(f"✅ PyTorch: {torch.__version__}")

    # Test MPS availability
    if torch.backends.mps.is_available():
        print("✅ MPS (Apple Silicon acceleration): Available")
        print("   Your videos will generate faster using Metal Performance Shaders!")
    else:
        print("⚠️  MPS: Not available (will use CPU)")
        print("   Videos will generate slower. Consider using an Apple Silicon Mac for better performance.")

    # Test basic torch operations
    try:
        device = "mps" if torch.backends.mps.is_available() else "cpu"
        test_tensor = torch.randn(2, 2).to(device)
        print(f"✅ Torch operations on {device}: Working")
    except Exception as e:
        print(f"❌ Torch operations: {e}")
        return False

    return True


def test_scripts():
    """Test that the generation scripts exist and are readable"""
    print("\n🔍 Testing scripts...")

    import os

    scripts = ["text_to_video.py", "image_to_video.py"]

    for script in scripts:
        if os.path.exists(script):
            print(f"✅ {script}: Found")
        else:
            print(f"❌ {script}: Not found")
            return False

    return True


def main():
    print("=" * 60)
    print("AI Video Generation Setup Test")
    print("=" * 60)
    print()

    all_passed = True

    # Test imports
    if not test_imports():
        all_passed = False

    # Test PyTorch
    if not test_pytorch():
        all_passed = False

    # Test scripts
    if not test_scripts():
        all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed! Your setup is ready to generate videos.")
        print()
        print("Try these commands:")
        print('  python text_to_video.py "A cat playing piano"')
        print('  python image_to_video.py path/to/image.jpg')
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()
