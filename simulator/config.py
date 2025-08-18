import os
from dotenv import load_dotenv

# Load environment variables from.env file
load_dotenv()

class Config:
    """
    Configuration class to hold all settings and API keys.
    Loads values from environment variables.
    """
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

    # Portfolio settings
    INITIAL_CASH = 1000.00

    # Analysis mode: 'llm' for live LLM calls, 'file' for pre-generated analysis
    ANALYSIS_MODE = os.getenv("ANALYSIS_MODE", "file")
    ANALYSIS_FILE_PATH = os.getenv("ANALYSIS_FILE_PATH", "analysis/sample_analysis.json")

    # Data storage paths
    PORTFOLIO_LOG_PATH = "data/portfolio_value.csv"
    TRANSACTIONS_LOG_PATH = "data/transactions.csv"

    # Ensure data directory exists
    @staticmethod
    def setup_directories():
        """Creates the data directory if it doesn't exist."""
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists('analysis'):
            os.makedirs('analysis')

# Initialize a single config object to be used throughout the application
config = Config()
config.setup_directories()

# Validate that API keys are loaded (only if using LLM mode)
if config.ANALYSIS_MODE == "llm" and (not config.GOOGLE_API_KEY or not config.FINNHUB_API_KEY):
    raise ValueError("API keys for Google and Finnhub must be set in the .env file when using LLM mode.")
elif config.ANALYSIS_MODE == "file" and not config.FINNHUB_API_KEY:
    raise ValueError("Finnhub API key must be set in the .env file for market data.")
