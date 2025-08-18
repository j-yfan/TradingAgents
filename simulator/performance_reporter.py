import pandas as pd
import quantstats as qs
import yfinance as yf

from config import config

def generate_performance_report(portfolio_log_path: str, benchmark_ticker: str = 'SPY'):
    """
    Generates a comprehensive performance report using quantstats.

    Args:
        portfolio_log_path (str): Path to the portfolio value log CSV file.
        benchmark_ticker (str): The ticker symbol for the benchmark (e.g., 'SPY' for S&P 500).
    """
    print("==================================================")
    print("Generating Performance Report...")
    print("==================================================")

    try:
        # 1. Load portfolio value history
        portfolio_df = pd.read_csv(portfolio_log_path, index_col='Date', parse_dates=True)
        if portfolio_df.empty or len(portfolio_df) < 2:
            print("Not enough data to generate a performance report. At least 2 data points are required.")
            return

        # Ensure the index is a DatetimeIndex and sort it
        portfolio_df.index = pd.to_datetime(portfolio_df.index)
        portfolio_df = portfolio_df.sort_index()
        
        # 2. Calculate daily returns
        # quantstats expects a pandas Series of returns
        returns = portfolio_df['TotalValue'].pct_change().dropna()
        returns.name = "Strategy"

        print(f"Loaded {len(returns)} daily returns for the strategy.")
        
        # Set timezone to None to avoid issues with yfinance and quantstats
        returns.index = returns.index.tz_localize(None)

        # 3. Generate the quantstats report
        # The html function will automatically download benchmark data
        output_filename = 'performance_report.html'
        print(f"Generating HTML report against benchmark '{benchmark_ticker}'...")
        print(f"This may take a moment as it downloads benchmark data...")
        
        qs.reports.html(
            returns,
            benchmark=benchmark_ticker,
            output=output_filename,
            title='LLM-Driven Trading Strategy Performance'
        )
        
        print("\n==================================================")
        print(f"Performance report successfully generated: {output_filename}")
        print("==================================================")

    except FileNotFoundError:
        print(f"Error: The portfolio log file was not found at '{portfolio_log_path}'.")
        print("Please run the main workflow at least once to generate the log file.")
    except Exception as e:
        print(f"An unexpected error occurred while generating the report: {e}")

if __name__ == '__main__':
    # This allows running the reporter directly
    # Ensure you have a portfolio_value.csv file with some data first
    generate_performance_report(config.PORTFOLIO_LOG_PATH)
