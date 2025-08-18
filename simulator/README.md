# LLM-Driven Algorithmic Trading Simulation

This is a comprehensive Python framework for evaluating trading strategies using either live LLM analysis or pre-generated stock analysis files. The system supports both Google's Gemini Pro model for real-time analysis and file-based analysis for reproducible testing.

## Analysis Modes

### File-Based Analysis (Recommended for Testing)
- Upload your own stock analysis files (JSON, CSV, or Excel)
- Consistent and reproducible results
- No API costs for LLM calls
- Perfect for backtesting and development

### Live LLM Analysis
- Real-time analysis using Google's Gemini Pro model
- Dynamic market insights
- Higher costs due to API usage
- Best for live trading scenarios

## Architecture Overview

The system follows a modular design with clear separation of concerns:

- **`config.py`** - Central configuration management and mode selection
- **`gemini_analyzer.py`** - Google Gemini API integration for live LLM analysis
- **`file_analyzer.py`** - File-based analysis reader (JSON/CSV/Excel support)
- **`trading_agent.py`** - Trading decision logic with pluggable agent interface
- **`market_data.py`** - Finnhub API integration for real-time market data
- **`portfolio_manager.py`** - Virtual portfolio simulation and transaction logging
- **`performance_reporter.py`** - Comprehensive performance analysis and reporting
- **`main.py`** - Daily workflow orchestration
- **`scheduler.py`** - Automated daily execution

## Setup Instructions

### 1. Environment Setup

Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Analysis Mode Configuration

The system supports two analysis modes:

**File-Based Mode (Default):**
```bash
ANALYSIS_MODE="file"
ANALYSIS_FILE_PATH="analysis/sample_analysis.json"
```

**LLM Mode:**
```bash
ANALYSIS_MODE="llm"
```

### 3. API Keys Configuration (for LLM mode or market data)

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and configure the analysis mode and API keys:
- **ANALYSIS_MODE**: Set to "file" for file-based analysis or "llm" for live LLM calls
- **ANALYSIS_FILE_PATH**: Path to your analysis file (when using file mode)
- Get a Google AI Studio API key from: https://makersuite.google.com/app/apikey (only needed for LLM mode)
- Get a Finnhub API key from: https://finnhub.io/dashboard (needed for market data)

### 4. Create Your Analysis File

For file-based mode, create your analysis file in JSON format:

```json
{
  "high_potential_stocks": [
    {
      "ticker": "AAPL",
      "company_name": "Apple Inc.",
      "confidence_score": 0.85,
      "reasoning": "Strong iPhone sales and expanding services revenue",
      "sentiment": "Positive"
    }
  ]
}
```

A sample file with 10 stocks is provided at `analysis/sample_analysis.json`.

### 3. Directory Structure

The system will automatically create these directories:
- `data/` - Portfolio valuations and transaction history
- `analysis/` - Analysis files for file-based mode

## Usage

### Running a Single Analysis

Test the system with a single run:
```bash
python main.py
```

### Automated Daily Execution

Start the scheduler for long-term automated trading:
```bash
python scheduler.py
```

The scheduler will run the analysis and trading workflow daily at 8:00 AM (configurable).

### Generate Performance Report

After accumulating some trading data:
```bash
python performance_reporter.py
```

This generates a comprehensive HTML report with risk-adjusted performance metrics.

## Key Features

### Structured LLM Output
- Uses Pydantic schemas to ensure reliable JSON output from Gemini
- Confidence scoring and sentiment analysis for each stock recommendation
- Chain-of-thought reasoning to improve analysis quality

### Professional Risk Management
- Virtual portfolio simulation with cash and position tracking
- Complete transaction audit trail
- Mark-to-market portfolio valuation

### Extensible Architecture
- Abstract base class for trading agents allows easy customization
- Modular design supports different data providers and LLM models
- Professional logging and error handling

### Comprehensive Analytics
- Uses quantstats library for institutional-grade performance metrics
- Benchmarking against market indices (default: S&P 500)
- Risk-adjusted returns, drawdown analysis, and Sharpe ratios

## Important Considerations

### Risks and Limitations
- **LLM Hallucinations**: AI models can generate plausible but false information
- **Market Efficiency**: Any edge discovered may diminish as similar strategies proliferate
- **Backtesting Bias**: Avoid overfitting by not frequently adjusting parameters
- **Data Quality**: Results depend on the accuracy of market data and LLM training

### Recommended Practices
- Start with paper trading only
- Monitor the `scheduler.log` for system health
- Regularly review performance reports
- Consider transaction costs in live implementation
- Maintain realistic expectations about AI trading performance

## File Descriptions

Each module serves a specific purpose in the trading pipeline:

1. **Configuration** (`config.py`) - Secure API key management and system settings
2. **Analysis** (`gemini_analyzer.py`) - Structured prompting and LLM interaction
3. **Decision** (`trading_agent.py`) - Trading logic with confidence-based example
4. **Data** (`market_data.py`) - Real-time price feeds from Finnhub
5. **Execution** (`portfolio_manager.py`) - Trade simulation and portfolio tracking
6. **Evaluation** (`performance_reporter.py`) - Professional performance analytics
7. **Orchestration** (`main.py`) - Daily workflow coordination
8. **Automation** (`scheduler.py`) - Unattended operation

## Extending the System

The modular architecture makes it easy to:
- Implement custom trading agents by inheriting from `BaseTradingAgent`
- Add new data sources by modifying `MarketDataProvider`
- Integrate different LLM providers by extending `GeminiAnalyzer`
- Customize performance metrics in `performance_reporter.py`

This framework provides a solid foundation for researching the intersection of artificial intelligence and quantitative finance.
