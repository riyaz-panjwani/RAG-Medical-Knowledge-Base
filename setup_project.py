#!/usr/bin/env python3
"""
Setup script to initialize the RAG Medical Knowledge Base project.
"""

import os
import sys
from pathlib import Path
from src.utils import create_directories, validate_api_keys

def setup_project():
    """Initialize project directories and validate configuration."""
    print("🏥 Setting up Medical RAG Knowledge Base...")

    # Create required directories
    required_dirs = [
        "data/medical_pdfs",
        "data/processed",
        "models/embeddings_cache"
    ]

    print("\n📁 Creating directories...")
    create_directories(required_dirs)

    # Check environment variables
    print("\n🔑 Checking API configuration...")
    required_keys = ["OPENAI_API_KEY"]

    if not validate_api_keys(required_keys):
        print("\n⚠️  Missing required API keys!")
        print("Please set up your .env file:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your API keys to .env")
        print("\nRequired keys:")
        for key in required_keys:
            print(f"  - {key}")
        return False

    print("✅ API keys validated")

    # Installation instructions
    print("\n📦 Next steps:")
    print("  1. Install dependencies: pip install -r requirements.txt")
    print("  2. Add medical PDFs to: data/medical_pdfs/")
    print("  3. Run the Streamlit app: streamlit run app.py")

    print("\n🎉 Project setup complete!")
    return True


if __name__ == "__main__":
    success = setup_project()
    sys.exit(0 if success else 1)
