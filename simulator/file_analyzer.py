import json
from typing import List, Dict, Any
from pathlib import Path

# Try to import pandas, but make it optional
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Warning: pandas not available. CSV and Excel support disabled.")

# Define basic data structures if pydantic is not available
try:
    from pydantic import BaseModel, Field, ValidationError
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    print("Warning: pydantic not available. Using basic validation.")

# Import or define the analysis structures
# Define basic structures for file-based analysis
class StockAnalysis:
    def __init__(self, ticker, company_name, confidence_score, reasoning, sentiment):
        self.ticker = ticker
        self.company_name = company_name
        self.confidence_score = confidence_score
        self.reasoning = reasoning
        self.sentiment = sentiment

class AnalysisReport:
    def __init__(self, high_potential_stocks):
        self.high_potential_stocks = high_potential_stocks

class FileAnalyzer:
    """
    Handles reading and parsing pre-generated stock analysis from files.
    Supports JSON, CSV, and Excel formats.
    """
    
    def __init__(self, file_path: str):
        """
        Initializes the FileAnalyzer with a path to the analysis file.
        
        Args:
            file_path (str): Path to the analysis file (JSON, CSV, or Excel)
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Analysis file not found: {file_path}")
        
        self.file_extension = self.file_path.suffix.lower()
        
    def get_analysis(self) -> AnalysisReport:
        """
        Reads the analysis file and returns a structured AnalysisReport.
        
        Returns:
            AnalysisReport: A Pydantic object containing the structured analysis.
            
        Raises:
            ValueError: If the file format is unsupported or data is invalid.
        """
        print(f"Reading analysis from file: {self.file_path}")
        
        try:
            if self.file_extension == '.json':
                return self._read_json_file()
            elif self.file_extension in ['.csv']:
                return self._read_csv_file()
            elif self.file_extension in ['.xlsx', '.xls']:
                return self._read_excel_file()
            else:
                raise ValueError(f"Unsupported file format: {self.file_extension}")
                
        except Exception as e:
            print(f"Error reading analysis file: {e}")
            raise
    
    def _read_json_file(self) -> AnalysisReport:
        """Reads JSON format analysis file."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validate and parse the JSON data
        try:
            # Always use basic validation for file mode
            stocks = []
            for stock_data in data.get('high_potential_stocks', []):
                stock = StockAnalysis(
                    ticker=stock_data['ticker'],
                    company_name=stock_data['company_name'],
                    confidence_score=float(stock_data['confidence_score']),
                    reasoning=stock_data['reasoning'],
                    sentiment=stock_data['sentiment']
                )
                stocks.append(stock)
            report = AnalysisReport(high_potential_stocks=stocks)
            print(f"Successfully loaded {len(report.high_potential_stocks)} stocks from JSON file.")
            return report
        except Exception as e:
            raise ValueError(f"Invalid JSON structure: {e}")
    
    def _read_csv_file(self) -> AnalysisReport:
        """Reads CSV format analysis file."""
        if not PANDAS_AVAILABLE:
            raise ImportError("pandas is required for CSV file support. Please install pandas.")
        df = pd.read_csv(self.file_path)
        return self._dataframe_to_analysis_report(df)
    
    def _read_excel_file(self) -> AnalysisReport:
        """Reads Excel format analysis file."""
        if not PANDAS_AVAILABLE:
            raise ImportError("pandas is required for Excel file support. Please install pandas.")
        df = pd.read_excel(self.file_path)
        return self._dataframe_to_analysis_report(df)
    
    def _dataframe_to_analysis_report(self, df: pd.DataFrame) -> AnalysisReport:
        """
        Converts a DataFrame to AnalysisReport.
        
        Expected columns: ticker, company_name, confidence_score, reasoning, sentiment
        """
        required_columns = ['ticker', 'company_name', 'confidence_score', 'reasoning', 'sentiment']
        
        # Check if all required columns exist
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        stocks = []
        for _, row in df.iterrows():
            try:
                stock = StockAnalysis(
                    ticker=str(row['ticker']).upper(),
                    company_name=str(row['company_name']),
                    confidence_score=float(row['confidence_score']),
                    reasoning=str(row['reasoning']),
                    sentiment=str(row['sentiment'])
                )
                stocks.append(stock)
            except Exception as e:
                print(f"Warning: Skipping invalid row for ticker {row.get('ticker', 'Unknown')}: {e}")
                continue
        
        if not stocks:
            raise ValueError("No valid stock data found in file")
        
        print(f"Successfully loaded {len(stocks)} stocks from {self.file_path.suffix.upper()} file.")
        return AnalysisReport(high_potential_stocks=stocks)

def create_sample_analysis_file(file_path: str, format_type: str = 'json'):
    """
    Creates a sample analysis file for testing purposes.
    
    Args:
        file_path (str): Path where to save the sample file
        format_type (str): Format type ('json', 'csv', or 'excel')
    """
    sample_stocks = [
        {
            "ticker": "AAPL",
            "company_name": "Apple Inc.",
            "confidence_score": 0.85,
            "reasoning": "Strong iPhone sales, expanding services revenue, and solid cash position. Recent earnings beat expectations.",
            "sentiment": "Positive"
        },
        {
            "ticker": "MSFT",
            "company_name": "Microsoft Corporation",
            "confidence_score": 0.78,
            "reasoning": "Cloud business growth, Azure expansion, and AI integration showing promise. Steady dividend growth.",
            "sentiment": "Positive"
        },
        {
            "ticker": "GOOGL",
            "company_name": "Alphabet Inc.",
            "confidence_score": 0.72,
            "reasoning": "Search dominance continues, but regulatory concerns and competition in cloud. YouTube growth solid.",
            "sentiment": "Neutral"
        },
        {
            "ticker": "TSLA",
            "company_name": "Tesla Inc.",
            "confidence_score": 0.65,
            "reasoning": "EV market leadership but increasing competition. Production targets met but margin pressure.",
            "sentiment": "Neutral"
        },
        {
            "ticker": "NVDA",
            "company_name": "NVIDIA Corporation",
            "confidence_score": 0.92,
            "reasoning": "AI chip demand explosion, data center growth, and gaming recovery. Strong technical indicators.",
            "sentiment": "Positive"
        },
        {
            "ticker": "META",
            "company_name": "Meta Platforms Inc.",
            "confidence_score": 0.58,
            "reasoning": "Metaverse investments showing mixed results. Ad revenue stable but regulatory headwinds persist.",
            "sentiment": "Neutral"
        },
        {
            "ticker": "AMZN",
            "company_name": "Amazon.com Inc.",
            "confidence_score": 0.81,
            "reasoning": "AWS growth strong, retail margins improving, and logistics efficiency gains. Prime growth steady.",
            "sentiment": "Positive"
        },
        {
            "ticker": "NFLX",
            "company_name": "Netflix Inc.",
            "confidence_score": 0.45,
            "reasoning": "Subscriber growth slowing, increased competition from Disney+ and others. Content costs rising.",
            "sentiment": "Negative"
        },
        {
            "ticker": "AMD",
            "company_name": "Advanced Micro Devices",
            "confidence_score": 0.76,
            "reasoning": "Server chip gains against Intel, data center growth, but consumer PC market weak.",
            "sentiment": "Positive"
        },
        {
            "ticker": "CRM",
            "company_name": "Salesforce Inc.",
            "confidence_score": 0.69,
            "reasoning": "SaaS leadership position solid, but growth slowing and valuation concerns in rising rate environment.",
            "sentiment": "Neutral"
        }
    ]
    
    file_path = Path(file_path)
    
    if format_type.lower() == 'json':
        analysis_data = {"high_potential_stocks": sample_stocks}
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2)
    
    elif format_type.lower() == 'csv':
        df = pd.DataFrame(sample_stocks)
        df.to_csv(file_path, index=False)
    
    elif format_type.lower() in ['excel', 'xlsx']:
        df = pd.DataFrame(sample_stocks)
        df.to_excel(file_path, index=False)
    
    print(f"Sample analysis file created: {file_path}")

if __name__ == '__main__':
    # Create sample files for testing
    create_sample_analysis_file("sample_analysis.json", "json")
    create_sample_analysis_file("sample_analysis.csv", "csv")
    create_sample_analysis_file("sample_analysis.xlsx", "excel")
    
    # Test reading the JSON file
    try:
        analyzer = FileAnalyzer("sample_analysis.json")
        report = analyzer.get_analysis()
        
        print("\n--- File Analysis Report ---")
        for stock in report.high_potential_stocks:
            print(f"Ticker: {stock.ticker} ({stock.company_name})")
            print(f"  Confidence: {stock.confidence_score:.2f}")
            print(f"  Sentiment: {stock.sentiment}")
            print(f"  Reasoning: {stock.reasoning[:100]}...\n")
            
    except Exception as e:
        print(f"Failed to get analysis: {e}")
