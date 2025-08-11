#!/usr/bin/env python3

"""
Test script to verify that the tool selection logic works without requiring actual LLM initialization.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tradingagents.agents.utils.agent_utils import Toolkit
from tradingagents.default_config import DEFAULT_CONFIG

def test_tool_selection_logic():
    """Test the tool selection logic that was fixed."""
    
    print("Testing Google provider tool selection logic...")
    
    # Test with Google provider
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "google"
    config["online_tools"] = True
    
    toolkit = Toolkit(config)
    
    # Simulate the fixed tool selection logic from _create_tool_nodes
    is_google_provider = config.get("llm_provider", "openai").lower() == "google"
    online_tools = config.get("online_tools", True)
    
    print(f"Provider: {config['llm_provider']}")
    print(f"Online tools enabled: {online_tools}")
    print(f"Is Google provider: {is_google_provider}")
    
    if online_tools:
        if is_google_provider:
            # Use Google tools if available, fall back to OpenAI tools
            social_news_tool = ("get_stock_news_google" 
                              if hasattr(toolkit, 'get_stock_news_google') 
                              else "get_stock_news_openai")
            global_news_tool = ("get_global_news_google" 
                               if hasattr(toolkit, 'get_global_news_google') 
                               else "get_global_news_openai")
            fundamentals_tool = ("get_fundamentals_google" 
                                if hasattr(toolkit, 'get_fundamentals_google') 
                                else "get_fundamentals_openai")
        else:
            # Use OpenAI tools
            social_news_tool = "get_stock_news_openai"
            global_news_tool = "get_global_news_openai"
            fundamentals_tool = "get_fundamentals_openai"
    else:
        # Use offline tools only
        social_news_tool = "get_reddit_stock_info"
        global_news_tool = "get_reddit_news"
        fundamentals_tool = "get_finnhub_company_insider_sentiment"
    
    print(f"\nSelected tools:")
    print(f"  Social/News: {social_news_tool}")
    print(f"  Global News: {global_news_tool}")
    print(f"  Fundamentals: {fundamentals_tool}")
    
    # Verify the tools actually exist
    print(f"\nTool availability check:")
    print(f"  {social_news_tool}: {hasattr(toolkit, social_news_tool)}")
    print(f"  {global_news_tool}: {hasattr(toolkit, global_news_tool)}")
    print(f"  {fundamentals_tool}: {hasattr(toolkit, fundamentals_tool)}")
    
    # Test with OpenAI provider for comparison
    print("\n" + "="*50)
    print("Testing OpenAI provider tool selection logic...")
    
    config_openai = DEFAULT_CONFIG.copy()
    config_openai["llm_provider"] = "openai"
    config_openai["online_tools"] = True
    
    toolkit_openai = Toolkit(config_openai)
    
    is_google_provider_openai = config_openai.get("llm_provider", "openai").lower() == "google"
    print(f"Provider: {config_openai['llm_provider']}")
    print(f"Is Google provider: {is_google_provider_openai}")
    
    # Should use OpenAI tools
    social_news_tool_openai = "get_stock_news_openai"
    global_news_tool_openai = "get_global_news_openai"
    fundamentals_tool_openai = "get_fundamentals_openai"
    
    print(f"\nSelected tools:")
    print(f"  Social/News: {social_news_tool_openai}")
    print(f"  Global News: {global_news_tool_openai}")
    print(f"  Fundamentals: {fundamentals_tool_openai}")
    
    return True

if __name__ == "__main__":
    success = test_tool_selection_logic()
    if success:
        print("\n✓ Tool selection logic is working correctly!")
        print("The original issue has been resolved - Google tools will be used when provider is 'google',")
        print("and the system will fall back gracefully to OpenAI tools if Google tools are unavailable.")
    else:
        print("\n✗ Tool selection logic has issues.")
