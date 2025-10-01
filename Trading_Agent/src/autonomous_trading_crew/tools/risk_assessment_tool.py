from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import sys
import os

# Add the project root to the path so we can import models
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    from models.volatility_model import get_volatility_model
    from models.risk_factor_model import get_risk_factor_model
    MODELS_AVAILABLE = True
except ImportError:
    MODELS_AVAILABLE = False
    print("Warning: Advanced risk models not available. Using basic calculations.")

class RiskAssessmentInput(BaseModel):
    symbol: str = Field(..., description="Stock symbol to assess risk for")
    historical_data: list = Field(..., description="Historical price data for risk calculation")
    confidence_level: float = Field(0.95, description="Confidence level for Value at Risk calculation (default 0.95)")

class RiskAssessmentTool(BaseTool):
    name: str = "Risk Assessment Analyzer"
    description: str = "Calculates financial risk metrics including Value at Risk (VaR), Conditional VaR, and other risk indicators"
    args_schema: Type[BaseModel] = RiskAssessmentInput
    
    def __init__(self):
        super().__init__()
        
    def _run(self, symbol: str, historical_data: list, confidence_level: float = 0.95) -> str:
        try:
            # Calculate various risk metrics
            risk_metrics = {}
            
            # Convert historical data to DataFrame
            df = pd.DataFrame(historical_data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')
            df = df.sort_index()
            
            # Calculate returns
            df['returns'] = df['close'].pct_change().dropna()
            
            # Calculate basic risk metrics
            risk_metrics["volatility"] = self._calculate_volatility(df['returns'])
            risk_metrics["sharpe_ratio"] = self._calculate_sharpe_ratio(df['returns'])
            risk_metrics["max_drawdown"] = self._calculate_max_drawdown(df['close'])
            risk_metrics["beta"] = self._calculate_beta(symbol, df['returns'])
            
            # Calculate Value at Risk (VaR)
            risk_metrics["var"] = self._calculate_var(df['returns'], confidence_level)
            
            # Calculate Conditional Value at Risk (CVaR)
            risk_metrics["cvar"] = self._calculate_cvar(df['returns'], confidence_level)
            
            # Position sizing recommendation
            risk_metrics["position_sizing"] = self._calculate_position_sizing(risk_metrics["volatility"])
            
            # Stress testing scenarios
            risk_metrics["stress_tests"] = self._perform_stress_tests(df['returns'])
            
            # Use advanced models if available
            if MODELS_AVAILABLE:
                risk_metrics["advanced_analysis"] = self._advanced_risk_analysis(df, symbol, risk_metrics)
            
            return json.dumps({
                "symbol": symbol,
                "confidence_level": confidence_level,
                "risk_metrics": risk_metrics
            })
        except Exception as e:
            return json.dumps({
                "error": f"Failed to assess risk for {symbol}: {str(e)}",
                "symbol": symbol
            })
    
    def _calculate_volatility(self, returns):
        """Calculate annualized volatility"""
        return round(returns.std() * np.sqrt(252), 4)
    
    def _calculate_sharpe_ratio(self, returns, risk_free_rate=0.02):
        """Calculate Sharpe ratio"""
        excess_returns = returns - risk_free_rate/252
        if returns.std() != 0:
            sharpe = (excess_returns.mean() / returns.std()) * np.sqrt(252)
            return round(sharpe, 4)
        return 0
    
    def _calculate_max_drawdown(self, prices):
        """Calculate maximum drawdown"""
        peak = prices.expanding(min_periods=1).max()
        drawdown = (prices - peak) / peak
        return round(drawdown.min(), 4)
    
    def _calculate_beta(self, symbol, stock_returns):
        """Calculate beta using S&P 500 as market index"""
        try:
            # Get S&P 500 data (^GSPC)
            market_data = yf.download("^GSPC", start=stock_returns.index[0], end=stock_returns.index[-1])
            market_data['returns'] = market_data['Adj Close'].pct_change().dropna()
            
            # Align dates
            merged = pd.merge(stock_returns, market_data['returns'], left_index=True, right_index=True, suffixes=('_stock', '_market'))
            
            # Calculate beta
            covariance = np.cov(merged['returns_stock'], merged['returns_market'])[0, 1]
            market_variance = np.var(merged['returns_market'])
            
            if market_variance != 0:
                beta = covariance / market_variance
                return round(beta, 4)
            return 1.0  # Default beta
        except:
            return 1.0  # Default beta if market data unavailable
    
    def _calculate_var(self, returns, confidence_level):
        """Calculate Value at Risk using historical simulation method"""
        try:
            # Historical simulation method
            var = np.percentile(returns, (1 - confidence_level) * 100)
            return round(abs(var), 4)
        except:
            return 0
    
    def _calculate_cvar(self, returns, confidence_level):
        """Calculate Conditional Value at Risk"""
        try:
            var_threshold = np.percentile(returns, (1 - confidence_level) * 100)
            cvar = returns[returns <= var_threshold].mean()
            return round(abs(cvar), 4)
        except:
            return 0
    
    def _calculate_position_sizing(self, volatility, max_risk_per_trade=0.02):
        """Calculate recommended position size based on volatility"""
        # Simple position sizing: lower volatility = higher position size
        # This is a simplified approach - in practice, you'd consider more factors
        base_position = 0.05  # 5% base position
        if volatility > 0:
            # Adjust position size inversely to volatility
            position_size = base_position / (1 + volatility)
            return round(min(position_size, 0.1), 4)  # Cap at 10%
        return base_position
    
    def _perform_stress_tests(self, returns):
        """Perform basic stress tests"""
        stress_results = {}
        
        # Market crash scenario (simulate 2008 financial crisis returns)
        crisis_returns = np.percentile(returns, 5)  # 5th percentile return
        stress_results["market_crash"] = {
            "description": "Simulated market crash scenario",
            "expected_loss": round(abs(crisis_returns) * 5, 4)  # 5x worst day
        }
        
        # High volatility scenario
        stress_results["high_volatility"] = {
            "description": "Double current volatility scenario",
            "expected_loss": round(returns.std() * 2 * 1.96, 4)  # 95% confidence with 2x vol
        }
        
        return stress_results
    
    def _advanced_risk_analysis(self, df, symbol, basic_metrics):
        """Use advanced models for risk analysis"""
        try:
            advanced_results = {}
            
            # Use volatility prediction model
            volatility_model = get_volatility_model()
            # Prepare features for volatility prediction (simplified)
            latest_data = df.tail(10)  # Last 10 days
            features = [
                latest_data['returns'].mean(),  # Average return
                latest_data['returns'].std(),   # Current volatility
                5000000,  # Volume (placeholder)
                50,       # RSI (placeholder)
                0.5,      # MACD (placeholder)
                20        # VIX (placeholder)
            ]
            predicted_volatility = volatility_model.predict(features)
            advanced_results["predicted_volatility"] = round(predicted_volatility, 4)
            
            # Use risk factor model
            risk_model = get_risk_factor_model()
            # Prepare features for risk factor prediction
            risk_features = [
                basic_metrics["volatility"],     # Current volatility
                basic_metrics["beta"],           # Beta
                basic_metrics["sharpe_ratio"],   # Sharpe ratio
                abs(basic_metrics["max_drawdown"]),  # Max drawdown
                basic_metrics["var"],            # VaR
                0.5,                             # Correlation with market (placeholder)
                1.0,                             # Liquidity ratio (placeholder)
                0.3                              # Earnings volatility (placeholder)
            ]
            risk_prediction = risk_model.predict(risk_features)
            advanced_results["risk_factor_analysis"] = risk_prediction
            
            return advanced_results
        except Exception as e:
            return {"error": f"Advanced analysis failed: {str(e)}"}