"""Test Hugging Face Image Generation - Simple Direct Approach"""
import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()

def test_image_generation():
    """Test generating an ocean image with Hugging Face"""
    
    # Get token from environment
    token = os.getenv('HUGGINGFACE_TOKEN')
    
    if not token:
        print("❌ ERROR: HUGGINGFACE_TOKEN not found in .env file")
        return
    
    print("🔑 Hugging Face token found!")
    print(f"🎨 Generating ocean image...")
    
    # Use Hugging Face Inference API directly (simpler approach)
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    payload = {
        "inputs": "Beautiful ocean with waves at sunset, ultra realistic, cinematic lighting"
    }
    
    try:
        print(f"📡 Sending request to Hugging Face API...")
        print(f"⏳ This may take 30-90 seconds on first use (free tier)...")
        print(f"💡 If you get 503, wait 20 seconds and run again...")
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        
        if response.status_code == 200:
            # Save the image
            output_dir = Path("data/test_images")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = output_dir / "ocean_test.png"
            
            # Convert bytes to PIL Image and save
            image = Image.open(BytesIO(response.content))
            image.save(output_path)
            
            print(f"✅ SUCCESS! Image generated and saved to: {output_path}")
            print(f"📊 Image size: {image.size}")
            print(f"🖼️  Open the file to view your ocean image!")
            
        elif response.status_code == 503:
            print("⏳ Model is loading... This is normal on first use.")
            print("💡 Wait 20-30 seconds and run the script again.")
            try:
                error_data = response.json()
                print(f"📝 Response: {error_data}")
                if 'estimated_time' in error_data:
                    print(f"⏱️  Estimated wait time: {error_data['estimated_time']} seconds")
            except:
                print(f"📝 Response: {response.text}")
            
        elif response.status_code == 401:
            print("❌ ERROR: Invalid or expired token")
            print("💡 Go to https://huggingface.co/settings/tokens")
            print("   1. Create new token with 'Read' permission")
            print("   2. Copy it and update HUGGINGFACE_TOKEN in .env")
            
        else:
            print(f"❌ ERROR: Status code {response.status_code}")
            print(f"📝 Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏱️  Request timed out after 120 seconds.")
        print("💡 The model might still be loading. Try again in a moment.")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print(f"💡 Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 HUGGING FACE IMAGE GENERATION TEST")
    print("=" * 60)
    print()
    test_image_generation()
    print()
    print("=" * 60)
