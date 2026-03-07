#!/usr/bin/env python3
"""Test Gemini client initialization"""
import os
import sys

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("GEMINI CLIENT DEBUG TEST")
print("=" * 60)

# Check environment variables
print("\n1. Environment Variables:")
print(f"   GEMINI_API_KEY: {'SET' if os.getenv('GEMINI_API_KEY') else 'NOT SET'}")
print(f"   GEMINI_MODEL: {os.getenv('GEMINI_MODEL', 'NOT SET')}")
print(f"   USE_GEMINI: {os.getenv('USE_GEMINI', 'NOT SET')}")

# Check if package is installed
print("\n2. Package Import Test:")
try:
    import google.generativeai as genai
    print("   ✓ google.generativeai imported successfully")
    print(f"   Package version: {genai.__version__ if hasattr(genai, '__version__') else 'unknown'}")
except ImportError as e:
    print(f"   ✗ Failed to import: {e}")
    sys.exit(1)

# Test configuration
print("\n3. Configuration Test:")
api_key = os.getenv('GEMINI_API_KEY', '')
if not api_key:
    print("   ✗ GEMINI_API_KEY is empty")
    sys.exit(1)

print(f"   API Key: {api_key[:10]}...{api_key[-4:]}")

try:
    genai.configure(api_key=api_key)
    print("   ✓ genai.configure() succeeded")
except Exception as e:
    print(f"   ✗ genai.configure() failed: {e}")
    sys.exit(1)

# Test model initialization
print("\n4. Model Initialization Test:")
model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
print(f"   Model: {model_name}")

try:
    model = genai.GenerativeModel(model_name)
    print(f"   ✓ GenerativeModel created: {type(model)}")
except Exception as e:
    print(f"   ✗ GenerativeModel failed: {e}")
    print("\n   Trying alternative model: gemini-1.5-flash")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        print(f"   ✓ Alternative model works: gemini-1.5-flash")
    except Exception as e2:
        print(f"   ✗ Alternative model also failed: {e2}")
        sys.exit(1)

# Test content generation
print("\n5. Content Generation Test:")
try:
    response = model.generate_content("Say 'Hello, Ashoka!' in one sentence.")
    print(f"   ✓ generate_content() succeeded")
    print(f"   Response: {response.text[:100]}")
except Exception as e:
    print(f"   ✗ generate_content() failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED - Gemini client is working!")
print("=" * 60)
