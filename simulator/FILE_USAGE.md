# File-Based Analysis Usage Guide

## Quick Start with File-Based Analysis

1. **Set up the environment:**
   ```bash
   # Copy the environment template
   cp .env.example .env
   
   # The default configuration uses file-based analysis
   # ANALYSIS_MODE="file"
   # ANALYSIS_FILE_PATH="analysis/sample_analysis.json"
   ```

2. **Run the simulator:**
   ```bash
   python main.py
   ```

## Creating Your Own Analysis Files

### JSON Format (Recommended)
Create a file like `analysis/my_analysis.json`:

```json
{
  "high_potential_stocks": [
    {
      "ticker": "AAPL",
      "company_name": "Apple Inc.",
      "confidence_score": 0.85,
      "reasoning": "Strong quarterly earnings, iPhone 15 sales exceeding expectations",
      "sentiment": "Positive"
    },
    {
      "ticker": "TSLA",
      "company_name": "Tesla Inc.",
      "confidence_score": 0.72,
      "reasoning": "EV market growth but increasing competition concerns",
      "sentiment": "Neutral"
    }
  ]
}
```

### Required Fields
- **ticker**: Stock symbol (e.g., "AAPL")
- **company_name**: Full company name
- **confidence_score**: Float between 0.0 and 1.0
- **reasoning**: Text explanation for the analysis
- **sentiment**: One of "Positive", "Neutral", or "Negative"

### CSV Format (Optional)
If you have pandas installed, you can also use CSV files:

```csv
ticker,company_name,confidence_score,reasoning,sentiment
AAPL,Apple Inc.,0.85,Strong quarterly earnings,Positive
TSLA,Tesla Inc.,0.72,EV growth but competition,Neutral
```

## Trading Agent Behavior

The confidence-based trading agent will:

1. **BUY** stocks with:
   - confidence_score >= 0.75 (configurable)
   - sentiment == "Positive"
   - Not already in portfolio

2. **HOLD** stocks that:
   - Are already in portfolio
   - Still meet buying criteria

3. **SELL** stocks that:
   - Are in portfolio
   - No longer meet buying criteria

## Example Workflow

1. **Upload your analysis file** to the `analysis/` directory
2. **Update .env** to point to your file:
   ```
   ANALYSIS_FILE_PATH="analysis/my_stocks.json"
   ```
3. **Run the simulator:**
   ```bash
   python main.py
   ```
4. **View results** in:
   - Console output for daily trades
   - `data/portfolio_value.csv` for portfolio history
   - `data/transactions.csv` for trade details

## Switching to LLM Mode

To use live Gemini analysis instead:

1. **Set up API key** in `.env`:
   ```
   GOOGLE_API_KEY="your_actual_api_key_here"
   ANALYSIS_MODE="llm"
   ```

2. **Run normally** - the system will make live API calls to Gemini

## Sample Analysis File

The provided `analysis/sample_analysis.json` contains 10 popular tech stocks with various confidence scores and sentiments. You can use this as a starting point or replace it with your own analysis.

## Benefits of File-Based Analysis

- **Reproducible**: Same analysis file gives consistent results
- **Cost-effective**: No LLM API costs
- **Fast**: No network delays
- **Controllable**: You define exactly what the system analyzes
- **Testable**: Easy to experiment with different scenarios
