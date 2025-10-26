from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Import sklearn preprocessing directly to ensure availability
try:
    from sklearn.preprocessing import MinMaxScaler
    SCIKIT_LEARN_AVAILABLE = True
except ImportError:
    SCIKIT_LEARN_AVAILABLE = False
    print("Warning: scikit-learn not available. Some features will not be functional.")
    MinMaxScaler = None

# Conditional imports for deep learning
try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("Warning: PyTorch not available. LSTM model will not be functional.")

# Conditional imports for time series
try:
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.seasonal import seasonal_decompose
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    STATS_MODELS_AVAILABLE = True
except ImportError:
    STATS_MODELS_AVAILABLE = False
    print("Warning: statsmodels not available. ARIMA/SARIMA models will not be functional.")

# Define the input schema
class PredictiveAnalyticsInput(BaseModel):
    symbol: str = Field(..., description="Stock symbol to analyze")
    historical_data: list = Field(..., description="Historical price data for prediction")
    prediction_days: int = Field(5, description="Number of days to predict into the future")

# Only define LSTMModel if torch is available
if TORCH_AVAILABLE:
    class LSTMModel(nn.Module):
        def __init__(self, input_size=1, hidden_layer_size=50, output_size=1, num_layers=2):
            super(LSTMModel, self).__init__()
            self.hidden_layer_size = hidden_layer_size
            self.num_layers = num_layers
            
            self.lstm = nn.LSTM(input_size, hidden_layer_size, num_layers, batch_first=True, dropout=0.2)
            self.linear = nn.Linear(hidden_layer_size, output_size)
            
        def forward(self, input_seq):
            lstm_out, _ = self.lstm(input_seq)
            predictions = self.linear(lstm_out[:, -1])
            return predictions

class PredictiveAnalyticsTool(BaseTool):
    name: str = "Predictive Analytics Tool"
    description: str = "Uses LSTM, ARIMA, and SARIMA models to predict future stock prices with adaptive quality features"
    args_schema: Type[BaseModel] = PredictiveAnalyticsInput
    
    def __init__(self):
        super().__init__()
        if SCIKIT_LEARN_AVAILABLE and MinMaxScaler is not None:
            self.scaler = MinMaxScaler(feature_range=(0, 1))
        else:
            self.scaler = None
            print("Warning: MinMaxScaler not available. Scaling will be disabled.")
        
    def _run(self, symbol: str, historical_data: list, prediction_days: int = 5) -> str:
        try:
            # Convert historical data to DataFrame
            df = pd.DataFrame(historical_data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')
            df = df.sort_index()
            
            # Get closing prices
            prices = df['close'].values.reshape(-1, 1)
            
            predictions = {}
            
            # LSTM Prediction
            if TORCH_AVAILABLE:
                predictions["lstm"] = self._lstm_prediction(prices, prediction_days)
            else:
                predictions["lstm"] = {"error": "PyTorch not available"}
            
            # ARIMA Prediction
            if STATS_MODELS_AVAILABLE:
                predictions["arima"] = self._arima_prediction(prices.flatten(), prediction_days)
            else:
                predictions["arima"] = {"error": "statsmodels not available"}
            
            # SARIMA Prediction
            if STATS_MODELS_AVAILABLE:
                predictions["sarima"] = self._sarima_prediction(prices.flatten(), prediction_days)
            else:
                predictions["sarima"] = {"error": "statsmodels not available"}
            
            # Ensemble prediction (simple average)
            ensemble_pred = self._ensemble_prediction(predictions, prediction_days, historical_data)
            
            # Adaptive quality assessment
            adaptive_quality = self._assess_adaptive_quality(predictions, prices)
            
            return json.dumps({
                "symbol": symbol,
                "prediction_days": prediction_days,
                "predictions": predictions,
                "ensemble_prediction": ensemble_pred,
                "adaptive_quality": adaptive_quality
            })
        except Exception as e:
            return json.dumps({
                "error": f"Failed to generate predictions for {symbol}: {str(e)}",
                "symbol": symbol
            })
    
    def _lstm_prediction(self, prices, prediction_days):
        """LSTM-based price prediction"""
        try:
            # Check if scaler is available
            if self.scaler is None:
                return {"error": "Scaler not available, cannot perform LSTM prediction"}
            
            # Scale the data
            scaled_data = self.scaler.fit_transform(prices)
            
            # Prepare training data
            sequence_length = 60
            x_train, y_train = [], []
            
            for i in range(sequence_length, len(scaled_data)):
                x_train.append(scaled_data[i-sequence_length:i, 0])
                y_train.append(scaled_data[i, 0])
            
            if len(x_train) == 0:
                return {"error": "Insufficient data for LSTM prediction"}
            
            x_train, y_train = np.array(x_train), np.array(y_train)
            x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
            
            # Convert to PyTorch tensors
            x_train_tensor = torch.FloatTensor(x_train)
            y_train_tensor = torch.FloatTensor(y_train)
            
            # Initialize and train model
            model = LSTMModel()
            criterion = nn.MSELoss()
            optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
            
            # Training (simplified - in practice, you'd train more)
            model.train()
            for epoch in range(50):  # Reduced epochs for faster execution
                optimizer.zero_grad()
                y_pred = model(x_train_tensor)
                loss = criterion(y_pred.squeeze(), y_train_tensor)
                loss.backward()
                optimizer.step()
            
            # Prediction
            model.eval()
            predictions = []
            current_sequence = scaled_data[-sequence_length:].reshape(1, sequence_length, 1)
            current_sequence = torch.FloatTensor(current_sequence)
            
            for _ in range(prediction_days):
                with torch.no_grad():
                    pred = model(current_sequence)
                    predictions.append(pred.item())
                    
                    # Update sequence for next prediction
                    new_seq = torch.cat((current_sequence[:, 1:, :], pred.unsqueeze(0).unsqueeze(0)), dim=1)
                    current_sequence = new_seq
            
            # Inverse transform predictions
            predictions = np.array(predictions).reshape(-1, 1)
            predictions = self.scaler.inverse_transform(predictions)
            
            # Format predictions with dates
            last_date = pd.to_datetime(pd.DataFrame(historical_data)['date'].iloc[-1])
            prediction_dates = [(last_date + timedelta(days=i+1)).strftime('%Y-%m-%d') for i in range(prediction_days)]
            
            return {
                "model": "LSTM",
                "predicted_prices": [round(float(p), 2) for p in predictions.flatten()],
                "prediction_dates": prediction_dates,
                "confidence": "medium"
            }
        except Exception as e:
            return {"error": f"LSTM prediction failed: {str(e)}"}
    
    def _arima_prediction(self, prices, prediction_days):
        """ARIMA-based price prediction"""
        try:
            # Fit ARIMA model (order=(1,1,1) is a simple starting point)
            model = ARIMA(prices, order=(1, 1, 1))
            fitted_model = model.fit()
            
            # Forecast
            forecast = fitted_model.forecast(steps=prediction_days)
            
            # Format predictions with dates
            last_date = pd.to_datetime(pd.DataFrame(historical_data)['date'].iloc[-1])
            prediction_dates = [(last_date + timedelta(days=i+1)).strftime('%Y-%m-%d') for i in range(prediction_days)]
            
            return {
                "model": "ARIMA",
                "predicted_prices": [round(float(p), 2) for p in forecast],
                "prediction_dates": prediction_dates,
                "confidence": "low"  # ARIMA can be unreliable for stock prices
            }
        except Exception as e:
            return {"error": f"ARIMA prediction failed: {str(e)}"}
    
    def _sarima_prediction(self, prices, prediction_days):
        """SARIMA-based price prediction"""
        try:
            # Fit SARIMA model (seasonal_order=(1,1,1,12) assumes yearly seasonality)
            model = SARIMAX(prices, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
            fitted_model = model.fit(disp=False)
            
            # Forecast
            forecast = fitted_model.forecast(steps=prediction_days)
            
            # Format predictions with dates
            last_date = pd.to_datetime(pd.DataFrame(historical_data)['date'].iloc[-1])
            prediction_dates = [(last_date + timedelta(days=i+1)).strftime('%Y-%m-%d') for i in range(prediction_days)]
            
            return {
                "model": "SARIMA",
                "predicted_prices": [round(float(p), 2) for p in forecast],
                "prediction_dates": prediction_dates,
                "confidence": "low"  # SARIMA can be unreliable for stock prices
            }
        except Exception as e:
            return {"error": f"SARIMA prediction failed: {str(e)}"}
    
    def _ensemble_prediction(self, predictions, prediction_days, historical_data):
        """Simple ensemble of all available models"""
        try:
            valid_predictions = []
            
            # Collect valid predictions
            for model_name, pred_data in predictions.items():
                if isinstance(pred_data, dict) and "predicted_prices" in pred_data:
                    valid_predictions.append(pred_data["predicted_prices"])
            
            if not valid_predictions:
                return {"error": "No valid predictions available for ensemble"}
            
            # Simple average of predictions
            ensemble_prices = np.mean(valid_predictions, axis=0)
            
            # Format with dates
            last_date = pd.to_datetime(pd.DataFrame(historical_data)['date'].iloc[-1])
            prediction_dates = [(last_date + timedelta(days=i+1)).strftime('%Y-%m-%d') for i in range(prediction_days)]
            
            return {
                "model": "Ensemble (Average)",
                "predicted_prices": [round(float(p), 2) for p in ensemble_prices],
                "prediction_dates": prediction_dates,
                "confidence": "medium"
            }
        except Exception as e:
            return {"error": f"Ensemble prediction failed: {str(e)}"}
    
    def _assess_adaptive_quality(self, predictions, actual_prices):
        """Assess the adaptive quality of predictions based on market conditions"""
        try:
            # Calculate volatility of recent prices as a measure of market stability
            recent_returns = np.diff(actual_prices.flatten()) / actual_prices[:-1].flatten()
            volatility = np.std(recent_returns) * np.sqrt(252)  # Annualized volatility
            
            # Assess model agreement (how similar the predictions are)
            valid_predictions = []
            for model_name, pred_data in predictions.items():
                if isinstance(pred_data, dict) and "predicted_prices" in pred_data:
                    valid_predictions.append(pred_data["predicted_prices"])
            
            agreement_score = 1.0
            if len(valid_predictions) > 1:
                # Calculate correlation between predictions
                pred_df = pd.DataFrame(valid_predictions).T
                correlations = pred_df.corr()
                # Average correlation as agreement measure
                if len(correlations) > 1:
                    agreement_score = correlations.values[np.triu_indices_from(correlations, k=1)].mean()
                    if np.isnan(agreement_score):
                        agreement_score = 0.5
            
            # Adjust confidence based on market conditions
            if volatility > 0.3:  # High volatility market
                market_condition = "high_volatility"
                confidence_adjustment = 0.7
            elif volatility < 0.15:  # Low volatility market
                market_condition = "low_volatility"
                confidence_adjustment = 1.1
            else:  # Normal market
                market_condition = "normal"
                confidence_adjustment = 1.0
            
            return {
                "market_volatility": round(volatility, 4),
                "model_agreement": round(agreement_score, 4) if not np.isnan(agreement_score) else 0.5,
                "market_condition": market_condition,
                "confidence_adjustment": confidence_adjustment,
                "adaptive_quality_score": round(agreement_score * confidence_adjustment, 4)
            }
        except Exception as e:
            return {"error": f"Adaptive quality assessment failed: {str(e)}"}