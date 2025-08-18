from abc import ABC, abstractmethod
from typing import List, Tuple, Dict

# Define a basic AnalysisReport for file-based analysis
class AnalysisReport:
    def __init__(self, high_potential_stocks):
        self.high_potential_stocks = high_potential_stocks

# Define a type alias for a trading signal for clarity
TradingSignal = Tuple[str, str, int]  # (Action, Ticker, Quantity)

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
            analysis_report (AnalysisReport): The structured analysis from the Gemini model.
            current_holdings (Dict[str, int]): A dictionary of currently held stocks and their quantities.

        Returns:
            List[TradingSignal]: A list of trading signals to be executed.
        """
        pass


class ConfidenceBasedAgent(BaseTradingAgent):
    """
    An example implementation of a trading agent.
    This agent makes decisions based on the confidence score from the LLM analysis.
    """
    def __init__(self, confidence_threshold: float = 0.75, trade_quantity: int = 10):
        """
        Initializes the agent with its trading parameters.

        Args:
            confidence_threshold (float): The minimum confidence score to trigger a BUY signal.
            trade_quantity (int): The number of shares to buy for each signal.
        """
        if not 0.0 <= confidence_threshold <= 1.0:
            raise ValueError("Confidence threshold must be between 0.0 and 1.0")
        self.confidence_threshold = confidence_threshold
        self.trade_quantity = trade_quantity

    def decide(self, analysis_report: AnalysisReport, current_holdings: Dict[str, int]) -> List[TradingSignal]:
        """
        Implements the decision-making logic.

        - Buys stocks with high confidence and positive sentiment.
        - Sells currently held stocks that are no longer recommended for buying.

        Args:
            analysis_report (AnalysisReport): The structured analysis from the Gemini model.
            current_holdings (Dict[str, int]): A dictionary of currently held stocks and their quantities.

        Returns:
            List[TradingSignal]: A list of trading signals.
        """
        signals: List[TradingSignal] = []
        recommended_buys = set()

        print("\n--- Trading Agent Decision Process ---")
        
        # 1. Generate BUY signals based on analysis
        for stock in analysis_report.high_potential_stocks:
            if stock.confidence_score >= self.confidence_threshold and stock.sentiment == "Positive":
                # Check if we already own this stock. If so, hold. If not, buy.
                if stock.ticker not in current_holdings:
                    signals.append(('BUY', stock.ticker, self.trade_quantity))
                    print(f"Decision: BUY {self.trade_quantity} shares of {stock.ticker} (Confidence: {stock.confidence_score:.2f})")
                else:
                    print(f"Decision: HOLD {stock.ticker} (already in portfolio, still recommended)")
                recommended_buys.add(stock.ticker)

        # 2. Generate SELL signals for holdings that are no longer recommended
        for ticker, quantity in current_holdings.items():
            if ticker not in recommended_buys:
                signals.append(('SELL', ticker, quantity)) # Sell all shares
                print(f"Decision: SELL {quantity} shares of {ticker} (no longer recommended)")

        if not signals:
            print("No trading signals generated for today.")
            
        return signals

if __name__ == '__main__':
    # Example usage for testing the module directly
    # Define StockAnalysis for testing
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
            StockAnalysis(ticker="MSFT", company_name="Microsoft Corp.", confidence_score=0.65, reasoning="Mixed signals", sentiment="Neutral"),
            StockAnalysis(ticker="GOOG", company_name="Google Inc.", confidence_score=0.90, reasoning="AI growth", sentiment="Positive")
        ]
    )
    
    # Create mock current holdings
    mock_holdings = {'GOOG': 10, 'NVDA': 5} # We own GOOG and NVDA

    # Initialize and run the agent
    agent = ConfidenceBasedAgent(confidence_threshold=0.75)
    trading_signals = agent.decide(mock_report, mock_holdings)

    print("\n--- Generated Trading Signals ---")
    print(trading_signals)
    # Expected output:
    # AAPL: BUY (confidence 0.85 > 0.75, positive sentiment)
    # GOOG is held because it's still recommended.
    # MSFT is ignored because confidence is too low.
    # NVDA is sold because it's not in today's recommendations.
