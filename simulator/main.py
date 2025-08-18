import pandas as pd
from config import config

# Import analyzers based on mode
if config.ANALYSIS_MODE == "llm":
    from gemini_analyzer import GeminiAnalyzer
else:
    from file_analyzer import FileAnalyzer

from dynamic_trading_agent import DynamicTradingAgent, PercentageAllocationAgent
from market_data import MarketDataProvider
from portfolio_manager import PortfolioManager

def run_daily_workflow():
    """
    Executes the entire daily workflow from analysis to trade execution.
    """
    print("==================================================")
    print(f"Starting daily trading workflow for {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("==================================================")

    try:
        # 1. Initialize all components
        if config.ANALYSIS_MODE == "llm":
            analyzer = GeminiAnalyzer(api_key=config.GOOGLE_API_KEY)
            print("Using LLM-based analysis (Google Gemini)")
        else:
            analyzer = FileAnalyzer(file_path=config.ANALYSIS_FILE_PATH)
            print(f"Using file-based analysis from: {config.ANALYSIS_FILE_PATH}")
            
        # Use the dynamic trading agent for better capital allocation
        agent = DynamicTradingAgent(
            confidence_threshold=0.75, 
            max_position_pct=0.25,  # Max 25% per position
            min_cash_reserve=0.05   # Keep 5% cash reserve
        )
        market_data = MarketDataProvider(api_key=config.FINNHUB_API_KEY)
        portfolio = PortfolioManager(initial_cash=config.INITIAL_CASH)

        # 2. Get analysis from analyzer (LLM or File)
        analysis_report = analyzer.get_analysis()
        if not analysis_report or not analysis_report.high_potential_stocks:
            print("No analysis received from analyzer. Ending workflow for today.")
            # Still need to log portfolio value for continuous tracking
            tickers_to_price = list(portfolio.holdings.keys())
            if tickers_to_price:
                current_prices = market_data.get_latest_prices(tickers_to_price)
                portfolio.update_portfolio_value(current_prices)
            else: # If no holdings, just log the cash value
                portfolio.update_portfolio_value({})
            return

        # 3. Get trading decisions from the agent
        # The dynamic agent needs current holdings, prices, and available cash
        current_holdings = portfolio.holdings
        
        # 4. Fetch market data for all relevant tickers first
        tickers_from_analysis = [stock.ticker for stock in analysis_report.high_potential_stocks]
        tickers_in_holdings = list(current_holdings.keys())
        all_relevant_tickers = list(set(tickers_from_analysis + tickers_in_holdings))

        current_prices = {}
        if all_relevant_tickers:
            current_prices = market_data.get_latest_prices(all_relevant_tickers)

        # Now make trading decisions with all required information
        signals = agent.decide(analysis_report, current_holdings, current_prices, portfolio.cash)

        if not signals:
            print("Trading agent generated no signals. No trades to execute.")

        # 5. Execute trades through the portfolio manager
        print("\n--- Executing Trades ---")
        for signal in signals:
            ticker = signal[1]
            price = current_prices.get(ticker)
            if price:
                portfolio.execute_trade(signal, price)
            else:
                print(f"Skipping trade for {ticker} due to missing price data.")

        # 6. Update and log final portfolio value for the day
        # We need prices for all holdings, not just those in today's signals
        final_tickers_to_price = list(portfolio.holdings.keys())
        if final_tickers_to_price:
             # Re-fetch in case holdings changed and we need a new price
            final_prices = market_data.get_latest_prices(final_tickers_to_price)
            portfolio.update_portfolio_value(final_prices)
        else: # If portfolio is all cash
            portfolio.update_portfolio_value({})


    except Exception as e:
        print(f"An error occurred during the daily workflow: {e}")
        # Optionally, add more robust error handling/notification here
    
    print("\n==================================================")
    print("Daily trading workflow finished.")
    print("==================================================")


if __name__ == '__main__':
    # This allows running the workflow directly for testing
    run_daily_workflow()
