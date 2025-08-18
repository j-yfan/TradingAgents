# Trading Simulator Project Structure

```
📁 TradingAgents/simulator/
├── 📄 main.py                          # Main entry point - orchestrates daily trading workflow
├── 📄 config.py                        # Configuration management (API keys, paths, settings)
├── 📄 README.md                        # Project documentation
├── 📄 requirements.txt                  # Python dependencies
├── 📄 .env                             # Environment variables (API keys)
├── 📄 PROJECT_STRUCTURE.md             # This file - project overview
│
├── 🧠 **TRADING AGENTS** 
│   ├── 📄 dynamic_trading_agent.py     # Smart agent with confidence-based position sizing
│   └── 📄 confidence_based_agent.py    # Simple confidence threshold agent (legacy)
│
├── 💰 **PORTFOLIO MANAGEMENT**
│   └── 📄 portfolio_manager.py         # Virtual portfolio with fractional shares support
│
├── 📊 **MARKET DATA**
│   └── 📄 market_data.py              # Yahoo Finance integration for live prices
│
├── 📈 **ANALYSIS ENGINE**
│   └── 📁 analysis/
│       └── 📄 sample_analysis.json     # Stock analysis with confidence scores
│
├── 💾 **DATA STORAGE**
│   └── 📁 data/
│       ├── 📄 transactions.csv         # Detailed trade history
│       └── 📄 portfolio_value.csv      # Daily portfolio performance tracking
│
└── 🔧 **UTILITIES**
    └── 📄 utils.py                     # Helper functions and utilities

================================================================================

## 🔄 WORKFLOW ARCHITECTURE

┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   main.py       │───▶│  Analysis Data   │───▶│ Trading Agent   │
│  (Orchestrator) │    │ (JSON Analysis)  │    │ (AI Decision)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                                               │
         ▼                                               ▼
┌─────────────────┐                            ┌─────────────────┐
│  Market Data    │                            │ Portfolio Mgr   │
│ (Live Prices)   │                            │ (Trade Exec)    │
└─────────────────┘                            └─────────────────┘
         │                                               │
         └──────────────┐                   ┌───────────┘
                        ▼                   ▼
                 ┌─────────────────────────────┐
                 │      Data Storage           │
                 │ (CSV Files & Logging)       │
                 └─────────────────────────────┘

================================================================================

## 📋 KEY COMPONENTS BREAKDOWN

### 🎯 **MAIN CONTROLLER** (`main.py`)
- **Purpose**: Orchestrates the entire trading workflow
- **Functions**: 
  - Load analysis data from JSON
  - Initialize portfolio state
  - Coordinate trading decisions
  - Execute trades and update records

### 🤖 **TRADING AGENTS**
- **`dynamic_trading_agent.py`**: Advanced AI agent with:
  - Confidence-weighted position sizing
  - Dynamic cash allocation
  - Fractional share support
  - Risk management (cash reserves)
  
- **`confidence_based_agent.py`**: Simple threshold-based agent

### 💼 **PORTFOLIO MANAGER** (`portfolio_manager.py`)
- Virtual trading simulation
- Fractional share handling
- Transaction logging
- Portfolio value tracking
- CSV export functionality

### 📊 **ANALYSIS DATA** (`analysis/sample_analysis.json`)
```json
{
  "high_potential_stocks": [
    {
      "ticker": "AAPL",
      "confidence_score": 0.85,      # 85% confidence
      "sentiment": "Positive",
      "reasoning": "Strong fundamentals..."
    }
  ]
}
```

### 📈 **MARKET DATA** (`market_data.py`)
- Real-time stock price fetching
- Yahoo Finance integration
- Batch price retrieval
- Error handling for missing data

### 🗄️ **DATA STORAGE**
- **`transactions.csv`**: Complete trade log
  ```csv
  Date,Symbol,Action,Quantity,Price,Total,Cash_Balance
  2025-08-16,MSFT,BUY,0.3277,520.17,170.46,8.96
  ```

- **`portfolio_value.csv`**: Daily performance tracking
  ```csv
  Date,Total_Value,Cash,Holdings_Value
  2025-08-16,1000.00,8.96,991.04
  ```

================================================================================

## 🚀 **EXECUTION FLOW**

1. **🏁 START** → `main.py` launches daily workflow
2. **📖 LOAD** → Read stock analysis from JSON
3. **💰 INIT** → Reconstruct portfolio state from CSV
4. **📊 FETCH** → Get current market prices via Yahoo Finance
5. **🧠 DECIDE** → AI agent analyzes and generates trading signals
6. **⚡ EXECUTE** → Portfolio manager processes trades
7. **📝 LOG** → Record transactions and update portfolio value
8. **🏆 FINISH** → Display final portfolio state

================================================================================

## 🔧 **CONFIGURATION** (`config.py`)

```python
# API Configuration
GOOGLE_API_KEY = "your-gemini-api-key"

# File Paths
TRANSACTIONS_LOG_PATH = "data/transactions.csv"
PORTFOLIO_LOG_PATH = "data/portfolio_value.csv"
ANALYSIS_FILE_PATH = "analysis/sample_analysis.json"

# Trading Parameters
INITIAL_CASH = 1000.0
CONFIDENCE_THRESHOLD = 0.75
MAX_POSITION_PCT = 0.25
MIN_CASH_RESERVE = 0.05  # 5% cash reserve
```

================================================================================

## 📈 **FEATURES**

✅ **Fractional Shares**: Buy 0.3277 shares of MSFT  
✅ **Dynamic Allocation**: Confidence-weighted position sizing  
✅ **Risk Management**: Automatic cash reserves (5%)  
✅ **Real-time Prices**: Live market data integration  
✅ **Complete Logging**: Full audit trail in CSV format  
✅ **AI Decision Making**: Intelligent buy/sell signals  
✅ **Portfolio Tracking**: Daily performance monitoring  

================================================================================

## 🎯 **NEXT STEPS**

- [ ] Add more sophisticated analysis sources
- [ ] Implement technical indicators
- [ ] Add backtesting capabilities
- [ ] Create web dashboard
- [ ] Add email notifications
- [ ] Implement stop-loss orders
