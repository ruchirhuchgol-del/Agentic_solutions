from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json
import pandas as pd
import numpy as np
from datetime import datetime

class ReportGeneratorToolInput(BaseModel):
    stock_data: dict = Field(..., description="Dictionary containing stock analysis data")
    report_type: str = Field("summary", description="Type of report to generate (summary, detailed, technical)")
    include_charts: bool = Field(False, description="Whether to include chart data in the report")

class ReportGeneratorTool(BaseTool):
    name: str = "Report Generator"
    description: str = "Generates comprehensive financial reports from stock analysis data"
    args_schema: Type[BaseModel] = ReportGeneratorToolInput
    
    def _run(self, stock_data: dict, report_type: str = "summary", include_charts: bool = False) -> str:
        try:
            if not stock_data:
                return "Error: No stock data provided for report generation."
            
            report = {}
            
            # Basic report information
            report["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            report["report_type"] = report_type
            
            # Extract stock symbol and name
            symbol = stock_data.get("symbol", "Unknown")
            report["symbol"] = symbol
            
            # Generate appropriate report based on type
            if report_type == "summary":
                report["content"] = self._generate_summary_report(stock_data)
            elif report_type == "detailed":
                report["content"] = self._generate_detailed_report(stock_data)
            elif report_type == "technical":
                report["content"] = self._generate_technical_report(stock_data)
            else:
                report["content"] = self._generate_summary_report(stock_data)
            
            # Add chart data if requested
            if include_charts and "history" in stock_data:
                report["chart_data"] = self._prepare_chart_data(stock_data["history"])
            
            return json.dumps(report, indent=2)
            
        except Exception as e:
            return f"Error generating report: {str(e)}"
    
    def _generate_summary_report(self, stock_data: dict) -> dict:
        """Generate a concise summary report with key metrics"""
        summary = {}
        
        # Extract quote data if available
        if "quote" in stock_data:
            quote = stock_data["quote"]
            summary["current_price"] = quote.get("currentPrice", "N/A")
            summary["price_change"] = quote.get("change", "N/A")
            summary["price_change_percent"] = quote.get("changePercent", "N/A")
            summary["market_cap"] = quote.get("marketCap", "N/A")
            summary["volume"] = quote.get("volume", "N/A")
        
        # Extract fundamental highlights if available
        if "fundamentals" in stock_data:
            fundamentals = stock_data["fundamentals"]
            summary["pe_ratio"] = fundamentals.get("trailingPE", "N/A")
            summary["eps"] = fundamentals.get("trailingEps", "N/A")
            summary["dividend_yield"] = fundamentals.get("dividendYield", "N/A")
            summary["52w_high"] = fundamentals.get("fiftyTwoWeekHigh", "N/A")
            summary["52w_low"] = fundamentals.get("fiftyTwoWeekLow", "N/A")
        
        # Add key technical indicators if available
        if "indicators" in stock_data:
            indicators = stock_data["indicators"]
            summary["sma_50"] = indicators.get("SMA_50", "N/A")
            summary["rsi"] = indicators.get("RSI", "N/A")
        
        return summary
    
    def _generate_detailed_report(self, stock_data: dict) -> dict:
        """Generate a comprehensive detailed report with all available data"""
        # Start with summary data
        detailed = self._generate_summary_report(stock_data)
        
        # Add more detailed fundamental data
        if "fundamentals" in stock_data:
            fundamentals = stock_data["fundamentals"]
            detailed["fundamentals"] = {
                "beta": fundamentals.get("beta", "N/A"),
                "profit_margins": fundamentals.get("profitMargins", "N/A"),
                "return_on_equity": fundamentals.get("returnOnEquity", "N/A"),
                "debt_to_equity": fundamentals.get("debtToEquity", "N/A"),
                "revenue_growth": fundamentals.get("revenueGrowth", "N/A"),
                "earnings_growth": fundamentals.get("earningsGrowth", "N/A"),
                "book_value": fundamentals.get("bookValue", "N/A"),
                "price_to_book": fundamentals.get("priceToBook", "N/A"),
                "forward_pe": fundamentals.get("forwardPE", "N/A"),
                "peg_ratio": fundamentals.get("pegRatio", "N/A")
            }
        
        # Add sentiment data if available
        if "sentiment" in stock_data:
            detailed["sentiment"] = stock_data["sentiment"]
        
        # Add risk assessment if available
        if "risk" in stock_data:
            detailed["risk_assessment"] = stock_data["risk"]
        
        return detailed
    
    def _generate_technical_report(self, stock_data: dict) -> dict:
        """Generate a technical analysis focused report"""
        technical = {}
        
        # Add price data summary
        if "quote" in stock_data:
            quote = stock_data["quote"]
            technical["current_price"] = quote.get("currentPrice", "N/A")
            technical["price_change"] = quote.get("change", "N/A")
            technical["price_change_percent"] = quote.get("changePercent", "N/A")
        
        # Add all technical indicators
        if "indicators" in stock_data:
            technical["indicators"] = stock_data["indicators"]
        
        # Add trading signals if available
        if "signals" in stock_data:
            technical["signals"] = stock_data["signals"]
        
        return technical
    
    def _prepare_chart_data(self, history_data: dict) -> dict:
        """Prepare historical data for charting"""
        chart_data = {}
        
        # Format data for easy charting
        if isinstance(history_data, dict):
            # Extract dates and prices
            dates = list(history_data.keys()) if "dates" not in history_data else history_data["dates"]
            prices = list(history_data.values()) if "prices" not in history_data else history_data["prices"]
            
            chart_data["dates"] = dates
            chart_data["prices"] = prices
            
            # Calculate moving averages if enough data points
            if len(prices) >= 20:
                chart_data["sma_20"] = self._calculate_sma(prices, 20)
            if len(prices) >= 50:
                chart_data["sma_50"] = self._calculate_sma(prices, 50)
        
        return chart_data
    
    def _calculate_sma(self, data: list, window: int) -> list:
        """Calculate Simple Moving Average"""
        if not isinstance(data, list) or len(data) < window:
            return []
        
        try:
            # Convert to numpy array for calculation
            data_array = np.array(data)
            sma = []
            
            for i in range(len(data_array)):
                if i < window - 1:
                    sma.append(None)  # Not enough data points yet
                else:
                    window_avg = np.mean(data_array[i-(window-1):i+1])
                    sma.append(float(window_avg))
            
            return sma
        except Exception:
            return []