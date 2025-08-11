#!/usr/bin/env python3

"""
Setup script to configure GOOGLE_API_KEY for testing.
"""

import os
import sys

def setup_google_api_key():
    """Set up Google API key for testing."""
    
    # Check if GOOGLE_API_KEY is already set
    if os.getenv("GOOGLE_API_KEY"):
        print("✓ GOOGLE_API_KEY is already set in environment")
        return True
    
    print("GOOGLE_API_KEY not found in environment variables.")
    print("\nTo set up the Google API key, you have a few options:")
    print("\n1. Set it as an environment variable:")
    print("   export GOOGLE_API_KEY='your-api-key-here'")
    print("\n2. Add it to your .bashrc or .zshrc:")
    print("   echo 'export GOOGLE_API_KEY=\"your-api-key-here\"' >> ~/.zshrc")
    print("\n3. Set it temporarily for this session:")
    
    api_key = input("\nEnter your Google API key (or press Enter to skip): ").strip()
    
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        print("✓ GOOGLE_API_KEY set for this session")
        return True
    else:
        print("⚠ Skipping Google API key setup")
        return False

def test_google_api_key():
    """Test if Google API key works."""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Try to create a simple Google LLM instance
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.1,
        )
        
        print("✓ Google API key appears to be working")
        return True
        
    except Exception as e:
        print(f"✗ Error with Google API key: {str(e)}")
        return False

if __name__ == "__main__":
    print("Setting up Google API Key...")
    
    if setup_google_api_key():
        print("\nTesting Google API key...")
        if test_google_api_key():
            print("\n✓ Google API setup completed successfully!")
        else:
            print("\n⚠ Google API key may have issues")
    else:
        print("\n⚠ Google API key not configured")
        print("You can run the trading agents with OpenAI provider instead, or set up Google API key later.")
