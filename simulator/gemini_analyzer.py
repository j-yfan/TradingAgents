import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from pydantic import BaseModel, Field
from typing import List
import datetime
import json

from config import config

# --- Pydantic Schemas for Structured Output ---

class StockAnalysis(BaseModel):
    """
    A structured representation of the analysis for a single stock.
    """
    ticker: str = Field(description="The stock ticker symbol, e.g., 'AAPL'.")
    company_name: str = Field(description="The full name of the company.")
    confidence_score: float = Field(
        description="A score from 0.0 to 1.0 indicating the confidence in the short-term growth potential.",
        ge=0.0,
        le=1.0
    )
    reasoning: str = Field(description="A concise, step-by-step analysis supporting the recommendation, covering news sentiment, financials, and momentum.")
    sentiment: str = Field(
        description="Overall sentiment derived from recent news analysis.",
        enum=["Positive", "Neutral", "Negative"]
    )

class AnalysisReport(BaseModel):
    """
    The top-level JSON object that contains the list of stock analyses.
    This is the expected output structure from the Gemini model.
    """
    high_potential_stocks: List[StockAnalysis]


# --- Gemini Analyzer Class ---

class GeminiAnalyzer:
    """
    Handles all interactions with the Google Gemini API for stock analysis.
    """
    def __init__(self, api_key: str):
        """
        Initializes the Gemini client.

        Args:
            api_key (str): The Google AI Studio API key.
        """
        if not api_key:
            raise ValueError("Gemini API key is not provided.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def _build_prompt(self) -> str:
        """
        Constructs the detailed prompt for the Gemini model.

        Returns:
            str: The fully formatted prompt string.
        """
        current_date = datetime.date.today().strftime("%Y-%m-%d")
        prompt = f"""
        You are a senior quantitative financial analyst at a top-tier hedge fund, renowned for your data-driven, unemotional, and highly analytical approach to identifying short-term market opportunities.

        Your task is to analyze the current market conditions, recent news, and technical indicators to identify the top 3 US-listed stocks with the highest growth potential over the next 1-5 trading days. Today's date is {current_date}.

        For each stock you select, you must provide a concise, step-by-step reasoning. This reasoning must include:
        1. A sentiment analysis of significant news from the past 48 hours.
        2. A summary of key financial metrics (e.g., P/E ratio, recent earnings performance).
        3. An analysis of recent price momentum and volume trends.

        The final output MUST be a single, valid JSON object. Do not include any introductory text, concluding summaries, or markdown formatting like ```json. The JSON object must adhere strictly to the schema provided.
        """
        return prompt

    def get_analysis(self) -> AnalysisReport:
        """
        Queries the Gemini model for stock analysis and returns a structured report.

        Returns:
            AnalysisReport: A Pydantic object containing the structured analysis.
        
        Raises:
            ValueError: If the model response is not valid JSON or does not match the schema.
        """
        prompt = self._build_prompt()
        
        generation_config = GenerationConfig(
            response_mime_type="application/json",
            response_schema=AnalysisReport.model_json_schema()
        )

        try:
            print("Querying Gemini Pro for stock analysis...")
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            print("Received response from Gemini Pro.")

            # The response.text should be a valid JSON string due to the generation_config
            response_json = json.loads(response.text)
            
            # Validate the JSON against our Pydantic model
            report = AnalysisReport.model_validate(response_json)
            return report

        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode JSON from model response. Response text: {response.text}")
            raise ValueError("Model returned invalid JSON.") from e
        except Exception as e:
            print(f"An unexpected error occurred during Gemini API call: {e}")
            raise

if __name__ == '__main__':
    # Example usage for testing the module directly
    try:
        analyzer = GeminiAnalyzer(api_key=config.GOOGLE_API_KEY)
        analysis_report = analyzer.get_analysis()
        
        print("\n--- Gemini Analysis Report ---")
        for stock in analysis_report.high_potential_stocks:
            print(f"Ticker: {stock.ticker} ({stock.company_name})")
            print(f"  Confidence: {stock.confidence_score:.2f}")
            print(f"  Sentiment: {stock.sentiment}")
            print(f"  Reasoning: {stock.reasoning}\n")
            
    except Exception as e:
        print(f"Failed to get analysis: {e}")
