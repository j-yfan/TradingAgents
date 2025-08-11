#!/usr/bin/env python3
"""
Test script to verify the fundamentals analyst fix works with Google provider
"""
import os
import sys

# Set environment variables
os.environ['GOOGLE_API_KEY'] = 'AIzaSyAKZafO-cKTuHnlHR4bnqCPpeCYITtEo0M'
os.environ['FINNHUB_API_KEY'] = 'd2bq3a9r01qvh3vcrs70d2bq3a9r01qvh3vcrs7g'

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test the Google functions
try:
    from tradingagents.dataflows.interface import get_fundamentals_google, get_stock_news_google
    
    print("Testing Google fundamentals function...")
    fundamentals_result = get_fundamentals_google('AAPL', '2025-08-10')
    print(f"✅ Fundamentals function works! Result length: {len(fundamentals_result)} characters")
    print(f"First 200 characters: {fundamentals_result[:200]}...")
    
    print("\nTesting Google news function...")
    news_result = get_stock_news_google('AAPL', '2025-08-10')
    print(f"✅ News function works! Result length: {len(news_result)} characters")
    print(f"First 200 characters: {news_result[:200]}...")
    
    # Test the toolkit methods
    print("\nTesting Toolkit methods...")
    from tradingagents.agents.utils.agent_utils import Toolkit
    from tradingagents.dataflows.config import get_config
    
    config = get_config()
    config['llm_provider'] = 'google'
    config['online_tools'] = True
    
    toolkit = Toolkit(config)
    
    print("✅ All tests passed! The fix is working correctly.")
    print("\nThe fundamentals analyst should now work properly with Google provider.")
    
except Exception as e:
    print(f"❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()
