import numpy as np
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class VolatilityPredictor:
    def __init__(self, model_path="models/volatility_predictor.pkl"):
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self._load_or_create_model()

    def _generate_synthetic_data(self, n_samples=1000):
        """Generate synthetic financial data for training"""
        np.random.seed(42)
        dates = pd.date_range(start="2020-01-01", periods=n_samples)
        
        # Generate synthetic price data
        base_price = 100
        prices = [base_price]
        for _ in range(1, n_samples):
            change = np.random.normal(0, 0.02)  # 2% daily volatility
            prices.append(prices[-1] * (1 + change))
        
        # Calculate returns and volatility
        returns = np.diff(prices) / prices[:-1]
        volatility = pd.Series(returns).rolling(30).std() * np.sqrt(252)  # Annualized volatility
        
        # Create features
        data = pd.DataFrame({
            'price': prices[1:],
            'return': returns,
            'volatility_30d': volatility,
            'volume': np.random.lognormal(10, 1, n_samples-1),
            'rsi': np.random.uniform(20, 80, n_samples-1),
            'macd': np.random.normal(0, 0.5, n_samples-1),
            'vix': np.random.uniform(10, 40, n_samples-1)
        }).dropna()
        
        return data

    def _load_or_create_model(self):
        if os.path.exists(self.model_path):
            print(f"Loading existing volatility model from {self.model_path}")
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.model_path.replace(".pkl", "_scaler.pkl"))
        else:
            print("Training new volatility prediction model...")
            data = self._generate_synthetic_data()
            
            # Prepare features and target
            X = data[['return', 'volume', 'rsi', 'macd', 'vix']]
            y = data['volatility_30d']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Scale features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.model.fit(X_train_scaled, y_train)
            
            # Save model
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.model_path.replace(".pkl", "_scaler.pkl"))
            print(f"Model saved to {self.model_path}")

    def predict(self, features):
        """Predict volatility from features"""
        if self.model is None or self.scaler is None:
            raise ValueError("Model not loaded")
            
        # Scale features
        features_scaled = self.scaler.transform([features])
        
        # Predict
        prediction = self.model.predict(features_scaled)[0]
        return max(0.01, prediction)  # Ensure positive volatility

# Singleton instance
_volatility_model = None

def get_volatility_model():
    global _volatility_model
    if _volatility_model is None:
        _volatility_model = VolatilityPredictor()
    return _volatility_model