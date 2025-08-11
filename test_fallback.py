#!/usr/bin/env python3

"""
Test script to verify that the fallback logic works for Google tools.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_google_api_key():
    """Check if Google API key is set."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print(f"✓ GOOGLE_API_KEY is set (length: {len(api_key)} chars)")
        return True
    else:
        print("⚠ GOOGLE_API_KEY not found in environment")
        print("Run: python setup_google_api.py to set it up")
        return False

from tradingagents.agents.utils.agent_utils import Toolkit
from tradingagents.default_config import DEFAULT_CONFIG

def test_toolkit_google_tools():
    """Test if Google tools are available in the toolkit."""
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "google"
    
    toolkit = Toolkit(config)
    
    print("Testing toolkit Google tools availability:")
    print(f"Has get_stock_news_google: {hasattr(toolkit, 'get_stock_news_google')}")
    print(f"Is get_stock_news_google callable: {hasattr(toolkit, 'get_stock_news_google') and callable(getattr(toolkit, 'get_stock_news_google'))}")
    
    print(f"Has get_fundamentals_google: {hasattr(toolkit, 'get_fundamentals_google')}")
    print(f"Is get_fundamentals_google callable: {hasattr(toolkit, 'get_fundamentals_google') and callable(getattr(toolkit, 'get_fundamentals_google'))}")
    
    print(f"Has get_global_news_google: {hasattr(toolkit, 'get_global_news_google')}")
    print(f"Is get_global_news_google callable: {hasattr(toolkit, 'get_global_news_google') and callable(getattr(toolkit, 'get_global_news_google'))}")
    
    # Test OpenAI fallbacks
    print(f"Has get_stock_news_openai: {hasattr(toolkit, 'get_stock_news_openai')}")
    print(f"Has get_fundamentals_openai: {hasattr(toolkit, 'get_fundamentals_openai')}")
    print(f"Has get_global_news_openai: {hasattr(toolkit, 'get_global_news_openai')}")

def test_social_media_analyst_logic():
    """Test the social media analyst tool selection logic."""
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "google"
    config["online_tools"] = True
    
    toolkit = Toolkit(config)
    
    print("\nTesting social media analyst tool selection logic:")
    
    # Simulate the logic from social_media_analyst.py
    if toolkit.config["online_tools"]:
        if toolkit.config.get("llm_provider", "openai").lower() == "google":
            if hasattr(toolkit, 'get_stock_news_google') and callable(getattr(toolkit, 'get_stock_news_google')):
                selected_tools = ["get_stock_news_google"]
                print("Selected Google tool: get_stock_news_google")
            else:
                print("Google news tool not properly registered, falling back to OpenAI tool")
                if hasattr(toolkit, 'get_stock_news_openai'):
                    selected_tools = ["get_stock_news_openai"]
                    print("Selected fallback tool: get_stock_news_openai")
                else:
                    selected_tools = ["get_reddit_stock_info"]
                    print("Selected fallback tool: get_reddit_stock_info")
        else:
            selected_tools = ["get_stock_news_openai"]
            print("Selected OpenAI tool: get_stock_news_openai")
    else:
        selected_tools = ["get_reddit_stock_info"]
        print("Selected offline tool: get_reddit_stock_info")
    
    print(f"Final tool selection: {selected_tools}")

if __name__ == "__main__":
    print("Checking Google API key setup...")
    check_google_api_key()
    print("\nRunning toolkit tests...")
    test_toolkit_google_tools()
    test_social_media_analyst_logic()
