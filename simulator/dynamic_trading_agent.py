from abc import ABC, abstractmethod
from typing import List, Tuple, Dict
import math

# Define a basic AnalysisReport for file-based analysis
class AnalysisReport:
    def __init__(self, high_potential_stocks):
        self.high_potential_stocks = high_potential_stocks

# Define a type alias for a trading signal for clarity
TradingSignal = Tuple[str, str, float]  # (Action, Ticker, Quantity - can be fractional)

class BaseTradingAgent(ABC):
    """
    Abstract Base Class for a trading agent.
    Defines the interface that all trading agents must implement.
    """
    @abstractmethod
    def decide(self, analysis_report: AnalysisReport, current_holdings: Dict[str, int]) -> List[TradingSignal]:
        """
        Makes trading decisions based on the analysis report and current holdings.

        Args:
            analysis_report (AnalysisReport): The structured analysis from the analysis.
            current_holdings (Dict[str, int]): A dictionary of currently held stocks and their quantities.

        Returns:
            List[TradingSignal]: A list of trading signals to be executed.
        """
        pass


class DynamicTradingAgent(BaseTradingAgent):
    """
    A smart trading agent that dynamically allocates capital based on confidence scores
    and available cash, ensuring it doesn't exceed budget constraints.
    """
    def __init__(self, 
                 confidence_threshold: float = 0.75, 
                 max_position_pct: float = 0.25,
                 min_cash_reserve: float = 0.1):
        """
        Initializes the agent with dynamic trading parameters.

        Args:
            confidence_threshold (float): The minimum confidence score to trigger a BUY signal.
            max_position_pct (float): Maximum percentage of portfolio to allocate to single position.
            min_cash_reserve (float): Minimum cash reserve percentage to maintain.
        """
        if not 0.0 <= confidence_threshold <= 1.0:
            raise ValueError("Confidence threshold must be between 0.0 and 1.0")
        if not 0.0 < max_position_pct <= 1.0:
            raise ValueError("Max position percentage must be between 0.0 and 1.0")
        if not 0.0 <= min_cash_reserve < 1.0:
            raise ValueError("Min cash reserve must be between 0.0 and 1.0")
            
        self.confidence_threshold = confidence_threshold
        self.max_position_pct = max_position_pct
        self.min_cash_reserve = min_cash_reserve

    def decide(self, analysis_report: AnalysisReport, current_holdings: Dict[str, int], 
              current_prices: Dict[str, float], available_cash: float) -> List[TradingSignal]:
        """
        Implements dynamic decision-making logic with intelligent position sizing.

        Args:
            analysis_report (AnalysisReport): The structured analysis.
            current_holdings (Dict[str, int]): Current holdings.
            current_prices (Dict[str, float]): Current stock prices.
            available_cash (float): Available cash for trading.

        Returns:
            List[TradingSignal]: A list of trading signals.
        """
        signals: List[TradingSignal] = []
        recommended_buys = set()

        print("\n--- Dynamic Trading Agent Decision Process ---")
        print(f"Available Cash: ${available_cash:,.2f}")
        
        # Calculate portfolio value for position sizing
        holdings_value = sum(
            current_holdings.get(ticker, 0) * current_prices.get(ticker, 0) 
            for ticker in current_holdings
        )
        total_portfolio_value = available_cash + holdings_value
        
        # Reserve cash for minimum reserve
        cash_reserve = available_cash * self.min_cash_reserve
        investable_cash = available_cash - cash_reserve
        print(f"Cash Reserve ({self.min_cash_reserve*100}%): ${cash_reserve:,.2f}")
        print(f"Investable Cash: ${investable_cash:,.2f}")
        
        # 1. Identify buy candidates
        buy_candidates = []
        for stock in analysis_report.high_potential_stocks:
            if (stock.confidence_score >= self.confidence_threshold and 
                stock.sentiment == "Positive" and
                stock.ticker in current_prices and
                current_prices[stock.ticker] is not None):
                
                if stock.ticker not in current_holdings:
                    buy_candidates.append(stock)
                    print(f"Buy candidate: {stock.ticker} (Confidence: {stock.confidence_score:.2f})")
                else:
                    print(f"Decision: HOLD {stock.ticker} (already in portfolio, still recommended)")
                    recommended_buys.add(stock.ticker)

        # 2. Dynamic position sizing for buy candidates
        if buy_candidates:
            # Sort by confidence score (highest first)
            buy_candidates.sort(key=lambda x: x.confidence_score, reverse=True)
            
            # Calculate weight allocation based on confidence scores
            total_confidence = sum(stock.confidence_score for stock in buy_candidates)
            remaining_cash = investable_cash
            
            print(f"Processing {len(buy_candidates)} buy candidates...")
            
            for stock in buy_candidates:
                if remaining_cash <= 0:
                    print(f"Skipping {stock.ticker}: No remaining cash")
                    break
                    
                stock_price = current_prices[stock.ticker]
                
                # Calculate allocation as a percentage of remaining investable cash
                confidence_weight = stock.confidence_score / total_confidence
                
                # Use a more flexible allocation approach
                base_allocation = confidence_weight * investable_cash
                
                # Apply max position constraint but use remaining cash if it's more restrictive
                max_position_value = total_portfolio_value * self.max_position_pct
                target_allocation = min(base_allocation, max_position_value, remaining_cash)
                
                # Calculate number of shares (allow fractional shares)
                # Always try to use all available remaining cash if target allocation is higher
                affordable_allocation = min(target_allocation, remaining_cash)
                
                # Calculate shares based on affordable allocation
                shares = affordable_allocation / stock_price
                
                # Round to reasonable precision (e.g., 4 decimal places)
                shares = round(shares, 4)
                
                # Calculate actual cost and ensure it doesn't exceed remaining cash
                actual_cost = round(shares * stock_price, 2)
                
                # If rounding caused us to exceed remaining cash, adjust shares down
                if actual_cost > remaining_cash:
                    # Work backwards: find maximum shares we can afford with exact remaining cash
                    max_affordable_shares = remaining_cash / stock_price
                    # Round down slightly to ensure we don't exceed budget
                    shares = math.floor(max_affordable_shares * 10000) / 10000  # Floor to 4 decimal places
                    actual_cost = round(shares * stock_price, 2)
                    
                    # Double-check we're still within budget
                    if actual_cost > remaining_cash:
                        shares = (remaining_cash - 0.01) / stock_price  # Leave 1 cent buffer
                        shares = math.floor(shares * 10000) / 10000
                        actual_cost = round(shares * stock_price, 2)
                    
                    if shares > 0:  # Final check after all adjustments
                        signals.append(('BUY', stock.ticker, shares))
                        remaining_cash = round(remaining_cash - actual_cost, 2)
                        recommended_buys.add(stock.ticker)
                        
                        print(f"Decision: BUY {shares} shares of {stock.ticker} at ${stock_price:.2f}")
                        print(f"  Cost: ${actual_cost:,.2f} ({confidence_weight*100:.1f}% weight)")
                        print(f"  Remaining cash: ${remaining_cash:,.2f}")
                    else:
                        print(f"Remaining cash ${remaining_cash:.2f} too small for any shares of {stock.ticker}")
                else:
                    # This handles the case where no rounding adjustment was needed
                    if shares > 0:
                        signals.append(('BUY', stock.ticker, shares))
                        remaining_cash = round(remaining_cash - actual_cost, 2)
                        recommended_buys.add(stock.ticker)
                        
                        print(f"Decision: BUY {shares} shares of {stock.ticker} at ${stock_price:.2f}")
                        print(f"  Cost: ${actual_cost:,.2f} ({confidence_weight*100:.1f}% weight)")
                        print(f"  Remaining cash: ${remaining_cash:,.2f}")
                    else:
                        print(f"Target allocation too small for {stock.ticker} (${target_allocation:.2f})")

        # 3. Generate SELL signals for holdings that are no longer recommended
        for ticker, quantity in current_holdings.items():
            if ticker not in recommended_buys:
                signals.append(('SELL', ticker, quantity))
                print(f"Decision: SELL {quantity} shares of {ticker} (no longer recommended)")

        if not signals:
            print("No trading signals generated for today.")
            
        print(f"Total signals generated: {len(signals)}")
        return signals


class PercentageAllocationAgent(BaseTradingAgent):
    """
    Alternative agent that allocates fixed percentages to each qualifying stock.
    """
    def __init__(self, 
                 confidence_threshold: float = 0.75,
                 allocation_per_stock: float = 0.15,
                 min_cash_reserve: float = 0.1):
        """
        Initializes the percentage allocation agent.

        Args:
            confidence_threshold (float): Minimum confidence for buy signals.
            allocation_per_stock (float): Percentage of portfolio to allocate per stock.
            min_cash_reserve (float): Minimum cash reserve percentage.
        """
        self.confidence_threshold = confidence_threshold
        self.allocation_per_stock = allocation_per_stock
        self.min_cash_reserve = min_cash_reserve

    def decide(self, analysis_report: AnalysisReport, current_holdings: Dict[str, int],
              current_prices: Dict[str, float], available_cash: float) -> List[TradingSignal]:
        """
        Implements percentage-based allocation logic.
        """
        signals: List[TradingSignal] = []
        recommended_buys = set()

        print("\n--- Percentage Allocation Trading Agent ---")
        print(f"Available Cash: ${available_cash:,.2f}")
        print(f"Allocation per stock: {self.allocation_per_stock*100}%")
        
        # Calculate investable cash
        investable_cash = available_cash * (1 - self.min_cash_reserve)
        allocation_amount = investable_cash * self.allocation_per_stock
        
        print(f"Allocation amount per stock: ${allocation_amount:,.2f}")

        # Generate buy signals
        for stock in analysis_report.high_potential_stocks:
            if (stock.confidence_score >= self.confidence_threshold and 
                stock.sentiment == "Positive" and
                stock.ticker in current_prices and
                current_prices[stock.ticker] is not None):
                
                if stock.ticker not in current_holdings:
                    stock_price = current_prices[stock.ticker]
                    shares = allocation_amount / stock_price
                    shares = round(shares, 4)  # Round to 4 decimal places
                    
                    if shares > 0:
                        signals.append(('BUY', stock.ticker, shares))
                        recommended_buys.add(stock.ticker)
                        actual_cost = shares * stock_price
                        print(f"Decision: BUY {shares} shares of {stock.ticker} for ${actual_cost:,.2f}")
                    else:
                        print(f"Allocation too small for {stock.ticker} at ${stock_price:.2f}")
                else:
                    print(f"Decision: HOLD {stock.ticker} (already owned)")
                    recommended_buys.add(stock.ticker)

        # Generate sell signals
        for ticker, quantity in current_holdings.items():
            if ticker not in recommended_buys:
                signals.append(('SELL', ticker, quantity))
                print(f"Decision: SELL {quantity} shares of {ticker}")

        return signals


if __name__ == '__main__':
    # Example usage for testing
    class StockAnalysis:
        def __init__(self, ticker, company_name, confidence_score, reasoning, sentiment):
            self.ticker = ticker
            self.company_name = company_name
            self.confidence_score = confidence_score
            self.reasoning = reasoning
            self.sentiment = sentiment

    # Create a mock analysis report
    mock_report = AnalysisReport(
        high_potential_stocks=[
            StockAnalysis(ticker="AAPL", company_name="Apple Inc.", confidence_score=0.85, reasoning="Strong earnings", sentiment="Positive"),
            StockAnalysis(ticker="MSFT", company_name="Microsoft Corp.", confidence_score=0.78, reasoning="Cloud growth", sentiment="Positive"),
            StockAnalysis(ticker="GOOGL", company_name="Google Inc.", confidence_score=0.90, reasoning="AI leadership", sentiment="Positive")
        ]
    )
    
    # Mock data
    mock_holdings = {}
    mock_prices = {'AAPL': 150.0, 'MSFT': 300.0, 'GOOGL': 2500.0}
    mock_cash = 1000.0

    # Test dynamic agent
    print("=== Testing Dynamic Trading Agent ===")
    agent = DynamicTradingAgent(confidence_threshold=0.75, max_position_pct=0.4)
    signals = agent.decide(mock_report, mock_holdings, mock_prices, mock_cash)
    print(f"Generated signals: {signals}")

    print("\n=== Testing Percentage Allocation Agent ===")
    agent2 = PercentageAllocationAgent(allocation_per_stock=0.3)
    signals2 = agent2.decide(mock_report, mock_holdings, mock_prices, mock_cash)
    print(f"Generated signals: {signals2}")
