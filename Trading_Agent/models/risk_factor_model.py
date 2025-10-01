import numpy as np
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class RiskFactorModel:
    def __init__(self, model_path="models/risk_factor_model.pkl"):
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self._load_or_create_model()

    def _generate_synthetic_data(self, n_samples=1000):
        """Generate synthetic risk data for training"""
        np.random.seed(42)
        
        # Generate features
        data = pd.DataFrame({
            'volatility': np.random.uniform(0.1, 0.5, n_samples),
            'beta': np.random.uniform(0.5, 2.0, n_samples),
            'sharpe_ratio': np.random.uniform(-1, 3, n_samples),
            'max_drawdown': np.random.uniform(0.05, 0.4, n_samples),
            'var_95': np.random.uniform(0.02, 0.15, n_samples),
            'correlation_market': np.random.uniform(-0.5, 1.0, n_samples),
            'liquidity_ratio': np.random.uniform(0.5, 2.0, n_samples),
            'earnings_volatility': np.random.uniform(0.1, 0.8, n_samples)
        })
        
        # Create risk labels (0: Low, 1: Medium, 2: High)
        # Simple rule-based labeling for synthetic data
        conditions = [
            (data['volatility'] < 0.2) & (data['max_drawdown'] < 0.15),
            (data['volatility'] >= 0.2) & (data['volatility'] < 0.35) & (data['max_drawdown'] < 0.25)
        ]
        choices = [0, 1]  # Low, Medium
        data['risk_level'] = np.select(conditions, choices, default=2)  # High
        
        return data

    def _load_or_create_model(self):
        if os.path.exists(self.model_path):
            print(f"Loading existing risk factor model from {self.model_path}")
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.model_path.replace(".pkl", "_scaler.pkl"))
        else:
            print("Training new risk factor model...")
            data = self._generate_synthetic_data()
            
            # Prepare features and target
            X = data.drop('risk_level', axis=1)
            y = data['risk_level']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Scale features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.model.fit(X_train_scaled, y_train)
            
            # Save model
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.model_path.replace(".pkl", "_scaler.pkl"))
            print(f"Model saved to {self.model_path}")

    def predict(self, features):
        """Predict risk level from features"""
        if self.model is None or self.scaler is None:
            raise ValueError("Model not loaded")
            
        # Scale features
        features_scaled = self.scaler.transform([features])
        
        # Predict
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        risk_labels = ["Low", "Medium", "High"]
        return {
            "risk_level": risk_labels[prediction],
            "risk_score": prediction,
            "probabilities": {
                "low": float(probabilities[0]),
                "medium": float(probabilities[1]),
                "high": float(probabilities[2])
            }
        }

# Singleton instance
_risk_factor_model = None

def get_risk_factor_model():
    global _risk_factor_model
    if _risk_factor_model is None:
        _risk_factor_model = RiskFactorModel()
    return _risk_factor_model