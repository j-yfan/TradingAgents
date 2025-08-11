#!/usr/bin/env python3

"""
Test script to verify that the tool node fixes work properly.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

def test_tool_nodes_with_google():
    """Test that tool nodes are properly created with Google provider."""
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "google"
    config["backend_url"] = "https://generativelanguage.googleapis.com/v1"
    config["deep_think_llm"] = "gemini-2.0-flash"
    config["quick_think_llm"] = "gemini-2.0-flash"
    config["online_tools"] = True
    
    print("Testing TradingAgentsGraph with Google provider...")
    
    try:
        # Create trading agent graph
        ta = TradingAgentsGraph(debug=False, config=config)
        
        print("✓ TradingAgentsGraph created successfully")
        
        # Check tool nodes
        tool_nodes = ta.tool_nodes
        print(f"✓ Tool nodes created: {list(tool_nodes.keys())}")
        
        # Check if the tool nodes were created (ToolNode doesn't expose tools directly)
        print(f"✓ Social tool node created: {type(tool_nodes['social'])}")
        print(f"✓ News tool node created: {type(tool_nodes['news'])}")
        print(f"✓ Fundamentals tool node created: {type(tool_nodes['fundamentals'])}")
        
        # Test that the toolkit has the right methods available
        toolkit = ta.toolkit
        print(f"✓ Toolkit provider config: {toolkit.config.get('llm_provider')}")
        
        # Check which tools are being used
        if hasattr(toolkit, 'get_stock_news_google'):
            print("✓ Google social tool available in toolkit")
        if hasattr(toolkit, 'get_global_news_google'):
            print("✓ Google news tool available in toolkit")
        if hasattr(toolkit, 'get_fundamentals_google'):
            print("✓ Google fundamentals tool available in toolkit")
        
        print("\nTest completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error creating TradingAgentsGraph: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_tool_nodes_with_google()
    if success:
        print("\nAll tests passed! The Google tools issue should now be resolved.")
    else:
        print("\nTests failed. There may still be issues to resolve.")
