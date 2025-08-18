import finnhub
from typing import Dict, List

from config import config

class MarketDataProvider:
    """
    Handles fetching market data from the Finnhub API.
    """
    def __init__(self, api_key: str):
        """
        Initializes the Finnhub client.

        Args:
            api_key (str): The Finnhub API key.
        """
        if not api_key:
            raise ValueError("Finnhub API key is not provided.")
        self.client = finnhub.Client(api_key=api_key)

    def get_latest_prices(self, tickers: List[str]) -> Dict[str, float]:
        """
        Fetches the latest closing price for a list of tickers.

        Args:
            tickers (List[str]): A list of stock ticker symbols.

        Returns:
            Dict[str, float]: A dictionary mapping tickers to their latest price.
                              Returns None for tickers where data could not be fetched.
        """
        prices = {}
        print(f"\nFetching latest prices for: {tickers}")
        for ticker in tickers:
            try:
                # The 'quote' endpoint provides the previous day's close price ('pc')
                # which is suitable for end-of-day simulations.
                quote = self.client.quote(ticker)
                if quote and 'c' in quote and quote['c'] != 0:
                    prices[ticker] = quote['c'] # 'c' is the current price
                    print(f"  {ticker}: ${quote['c']:.2f}")
                else:
                    prices[ticker] = None
                    print(f"  Could not fetch price for {ticker}")
            except Exception as e:
                print(f"Error fetching price for {ticker}: {e}")
                prices[ticker] = None
        return prices

if __name__ == '__main__':
    # Example usage for testing the module directly
    provider = MarketDataProvider(api_key=config.FINNHUB_API_KEY)
    sample_tickers = ['AAPL', 'GOOG', 'MSFT']
    latest_prices = provider.get_latest_prices(sample_tickers)
    print("\n--- Fetched Prices ---")
    print(latest_prices)
