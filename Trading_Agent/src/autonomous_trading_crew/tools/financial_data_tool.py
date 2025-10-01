from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import json
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class FinancialDataToolInput(BaseModel):
    symbol: str = Field(..., description="Stock symbol to analyze")
    data_types: list = Field(..., description="Types of data to retrieve (quote, history, fundamentals, indicators)")
    timeframe: str = Field("1mo", description="Historical data timeframe (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)")

class FinancialDataTool(BaseTool):
    name: str = "Financial Data API"
    description: str = "Fetches real-time and historical market data from Yahoo Finance"
    args_schema: Type[BaseModel] = FinancialDataToolInput
    cache: dict = {}  # Define cache as a class field
    
    def __init__(self):
        super().__init__()
        
    def _run(self, symbol: str, data_types: list, timeframe: str = "1mo") -> str:
        results = {}
        
        try:
            # Fetch stock data using yfinance
            ticker = yf.Ticker(symbol)
            
            # Fetch real-time quote data
            if "quote" in data_types:
                results["quote"] = self._fetch_quote_data(ticker)
                
            # Fetch historical price data
            if "history" in data_types:
                results["history"] = self._fetch_historical_data(ticker, timeframe)
                
            # Fetch fundamental data
            if "fundamentals" in data_types:
                results["fundamentals"] = self._fetch_fundamental_data(ticker)
                
            # Calculate technical indicators
            if "indicators" in data_types and ("history" in results or "history" not in data_types):
                # If history wasn't requested but indicators are needed, fetch history
                if "history" not in results:
                    results["history"] = self._fetch_historical_data(ticker, timeframe)
                results["indicators"] = self._calculate_technical_indicators(results["history"])
                
        except Exception as e:
            return json.dumps({"error": f"Failed to fetch data for {symbol}: {str(e)}"})
            
        return json.dumps(results)
    
    def _fetch_quote_data(self, ticker):
        """Fetch real-time quote data"""
        try:
            info = ticker.info
            hist = ticker.history(period="2d")
            
            if len(hist) >= 2:
                previous_close = hist['Close'].iloc[-2]
                current_price = hist['Close'].iloc[-1]
                price_change = current_price - previous_close
                price_change_percent = (price_change / previous_close) * 100
            else:
                current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
                previous_close = info.get('previousClose', 0)
                price_change = current_price - previous_close if previous_close else 0
                price_change_percent = (price_change / previous_close) * 100 if previous_close else 0
            
            return {
                "symbol": ticker.ticker,
                "current_price": round(current_price, 2),
                "previous_close": round(previous_close, 2),
                "price_change": round(price_change, 2),
                "price_change_percent": round(price_change_percent, 2),
                "market_cap": info.get('marketCap', 0),
                "volume": info.get('volume', 0),
                "avg_volume": info.get('averageVolume', 0),
                "pe_ratio": info.get('trailingPE', 0),
                "dividend_yield": info.get('dividendYield', 0),
            }
        except Exception as e:
            return {"error": f"Failed to fetch quote data: {str(e)}"}
    
    def _fetch_historical_data(self, ticker, timeframe):
        """Fetch historical price data"""
        try:
            hist = ticker.history(period=timeframe)
            if hist.empty:
                return {"error": "No historical data available"}
            
            # Convert to list of dictionaries for JSON serialization
            history_data = []
            for index, row in hist.iterrows():
                history_data.append({
                    "date": index.strftime('%Y-%m-%d'),
                    "open": round(row['Open'], 2),
                    "high": round(row['High'], 2),
                    "low": round(row['Low'], 2),
                    "close": round(row['Close'], 2),
                    "volume": int(row['Volume'])
                })
            
            return history_data
        except Exception as e:
            return {"error": f"Failed to fetch historical data: {str(e)}"}
    
    def _fetch_fundamental_data(self, ticker):
        """Fetch fundamental data"""
        try:
            info = ticker.info
            return {
                "sector": info.get('sector', 'N/A'),
                "industry": info.get('industry', 'N/A'),
                "market_cap": info.get('marketCap', 0),
                "pe_ratio": info.get('trailingPE', 0),
                "forward_pe": info.get('forwardPE', 0),
                "peg_ratio": info.get('pegRatio', 0),
                "price_to_book": info.get('priceToBook', 0),
                "dividend_yield": info.get('dividendYield', 0),
                "eps": info.get('trailingEps', 0),
                "revenue": info.get('totalRevenue', 0),
                "gross_margins": info.get('grossMargins', 0),
                "ebitda_margins": info.get('ebitdaMargins', 0),
                "profit_margins": info.get('profitMargins', 0),
                "beta": info.get('beta', 0),
                "fifty_two_week_high": info.get('fiftyTwoWeekHigh', 0),
                "fifty_two_week_low": info.get('fiftyTwoWeekLow', 0)
            }
        except Exception as e:
            return {"error": f"Failed to fetch fundamental data: {str(e)}"}
    
    def _calculate_technical_indicators(self, historical_data):
        """Calculate technical indicators"""
        try:
            if isinstance(historical_data, dict) and "error" in historical_data:
                return historical_data
                
            # Convert to DataFrame for easier calculation
            df = pd.DataFrame(historical_data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')
            df = df.sort_index()
            
            # Calculate RSI (14-day)
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # Calculate 50-day and 200-day moving averages
            ma_50 = df['close'].rolling(window=50).mean()
            ma_200 = df['close'].rolling(window=200).mean()
            
            # Calculate MACD
            exp1 = df['close'].ewm(span=12).mean()
            exp2 = df['close'].ewm(span=26).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=9).mean()
            
            # Calculate Bollinger Bands
            rolling_mean = df['close'].rolling(window=20).mean()
            rolling_std = df['close'].rolling(window=20).std()
            upper_band = rolling_mean + (rolling_std * 2)
            lower_band = rolling_mean - (rolling_std * 2)
            
            # Get latest values
            latest_idx = df.index[-1]
            
            return {
                "rsi": round(rsi.loc[latest_idx], 2) if not pd.isna(rsi.loc[latest_idx]) else 0,
                "ma_50": round(ma_50.loc[latest_idx], 2) if not pd.isna(ma_50.loc[latest_idx]) else 0,
                "ma_200": round(ma_200.loc[latest_idx], 2) if not pd.isna(ma_200.loc[latest_idx]) else 0,
                "macd": round(macd.loc[latest_idx], 2) if not pd.isna(macd.loc[latest_idx]) else 0,
                "macd_signal": round(signal.loc[latest_idx], 2) if not pd.isna(signal.loc[latest_idx]) else 0,
                "upper_bollinger": round(upper_band.loc[latest_idx], 2) if not pd.isna(upper_band.loc[latest_idx]) else 0,
                "lower_bollinger": round(lower_band.loc[latest_idx], 2) if not pd.isna(lower_band.loc[latest_idx]) else 0,
                "current_price": round(df['close'].loc[latest_idx], 2)
            }
        except Exception as e:
            return {"error": f"Failed to calculate technical indicators: {str(e)}"}