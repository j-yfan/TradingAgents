import pandas as pd
import os
from datetime import datetime
from typing import Dict, List, Tuple

from config import config

TradingSignal = Tuple[str, str, float] # (Action, Ticker, Quantity - can be fractional)

class PortfolioManager:
    """
    Manages the virtual portfolio, including cash, holdings, and transaction logging.
    """
    def __init__(self, initial_cash: float):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.holdings: Dict[str, float] = {}  # {ticker: quantity - can be fractional}
        
        self.transactions_log_path = config.TRANSACTIONS_LOG_PATH
        self.portfolio_log_path = config.PORTFOLIO_LOG_PATH
        
        self.transactions_df = self._load_log(self.transactions_log_path, ['Ticker', 'Action', 'Quantity', 'Price', 'Value'])
        self.portfolio_df = self._load_log(self.portfolio_log_path, ['TotalValue'])

        self._reconstruct_state()

    def _load_log(self, path: str, columns: List[str]) -> pd.DataFrame:
        """Loads a log file if it exists, otherwise creates an empty DataFrame."""
        if os.path.exists(path):
            return pd.read_csv(path, index_col='Date', parse_dates=True)
        else:
            # Create empty DataFrame with Date as index
            df = pd.DataFrame(columns=columns)
            df.index.name = 'Date'
            return df

    def _reconstruct_state(self):
        """Reconstructs current cash and holdings from the transaction log."""
        if not self.transactions_df.empty:
            cash_flow = 0
            temp_holdings = {}
            for _, row in self.transactions_df.iterrows():
                if row['Action'] == 'BUY':
                    cash_flow -= row['Value']
                    temp_holdings[row['Ticker']] = temp_holdings.get(row['Ticker'], 0) + row['Quantity']
                elif row['Action'] == 'SELL':
                    cash_flow += row['Value']
                    temp_holdings[row['Ticker']] = temp_holdings.get(row['Ticker'], 0) - row['Quantity']
            
            self.cash = self.initial_cash + cash_flow
            self.holdings = {k: v for k, v in temp_holdings.items() if v > 0.0001}  # Filter out near-zero holdings
        
        print("\n--- Portfolio State Reconstructed ---")
        print(f"Current Cash: ${self.cash:,.2f}")
        print(f"Current Holdings: {self.holdings}")

    def execute_trade(self, signal: TradingSignal, price: float):
        """
        Executes a single trading signal, updating cash and holdings.

        Args:
            signal (TradingSignal): The trade to execute.
            price (float): The execution price of the asset.
        """
        action, ticker, quantity = signal
        trade_value = quantity * price

        if action == 'BUY':
            if self.cash >= trade_value:
                self.cash -= trade_value
                self.holdings[ticker] = self.holdings.get(ticker, 0) + quantity
                self._log_transaction(ticker, action, quantity, price)
                print(f"Executed BUY: {quantity} of {ticker} at ${price:.2f} (Total: ${trade_value:,.2f})")
            else:
                print(f"Failed BUY: Insufficient cash for {quantity} of {ticker}. Need ${trade_value:,.2f}, have ${self.cash:,.2f}")

        elif action == 'SELL':
            if ticker in self.holdings and self.holdings[ticker] >= quantity:
                self.cash += trade_value
                self.holdings[ticker] -= quantity
                if self.holdings[ticker] <= 0.0001:  # Handle floating point precision
                    del self.holdings[ticker]
                self._log_transaction(ticker, action, quantity, price)
                print(f"Executed SELL: {quantity} of {ticker} at ${price:.2f} (Total: ${trade_value:,.2f})")
            else:
                current_holding = self.holdings.get(ticker, 0)
                print(f"Failed SELL: Not enough shares of {ticker} to sell. Have {current_holding}, need {quantity}")

    def _log_transaction(self, ticker: str, action: str, quantity: float, price: float):
        """Logs a transaction to the DataFrame and saves it."""
        new_log = pd.DataFrame({
            'Ticker': [ticker],
            'Action': [action],
            'Quantity': [quantity],
            'Price': [price],
            'Value': [quantity * price]
        }, index=[datetime.now().strftime('%Y-%m-%d')])
        new_log.index.name = 'Date'
        
        self.transactions_df = pd.concat([self.transactions_df, new_log])
        self.transactions_df.to_csv(self.transactions_log_path)

    def update_portfolio_value(self, current_prices: Dict[str, float]):
        """
        Calculates the total market value of the portfolio and logs it.

        Args:
            current_prices (Dict[str, float]): A dictionary of current prices for all held assets.
        """
        holdings_value = 0
        for ticker, quantity in self.holdings.items():
            price = current_prices.get(ticker)
            if price is not None:
                holdings_value += quantity * price
            else:
                print(f"Warning: Could not find price for held asset {ticker} during valuation. It will be excluded from total value.")

        total_value = self.cash + holdings_value
        
        new_log = pd.DataFrame({
            'TotalValue': [total_value]
        }, index=[datetime.now().strftime('%Y-%m-%d')])
        new_log.index.name = 'Date'

        self.portfolio_df = pd.concat([self.portfolio_df, new_log])
        self.portfolio_df.to_csv(self.portfolio_log_path)
        
        print("\n--- Portfolio Value Updated ---")
        print(f"Holdings Value: ${holdings_value:,.2f}")
        print(f"Cash: ${self.cash:,.2f}")
        print(f"Total Portfolio Value: ${total_value:,.2f}")

if __name__ == '__main__':
    # Example usage for testing the module directly
    pm = PortfolioManager(initial_cash=config.INITIAL_CASH)
    
    # Simulate some trades
    pm.execute_trade(('BUY', 'AAPL', 10), 150.0)
    pm.execute_trade(('BUY', 'GOOG', 5), 2800.0)
    
    # Simulate portfolio valuation
    prices = {'AAPL': 155.0, 'GOOG': 2850.0}
    pm.update_portfolio_value(prices)
    
    print("\nTransaction Log:")
    print(pm.transactions_df.tail())
    print("\nPortfolio Value Log:")
    print(pm.portfolio_df.tail())
