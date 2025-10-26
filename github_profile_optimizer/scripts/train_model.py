"""
GitHub Profile Optimizer - Model Training and Fine-tuning Script

This script trains and fine-tunes ML models to predict optimization recommendations
for GitHub profiles based on historical data and successful profile patterns.

Usage:
    python train_model.py --samples 2000 --tune --model-type random_forest
"""

import argparse
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, mean_squared_error, r2_score, accuracy_score
import joblib
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import logging
from datetime import datetime
from dataclasses import dataclass, asdict


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class TrainingConfig:
    """Configuration for model training."""
    n_samples: int = 2000
    test_size: float = 0.2
    random_state: int = 42
    cv_folds: int = 5
    tune_hyperparameters: bool = True
    model_type: str = 'random_forest'  # 'random_forest' or 'gradient_boost'
    output_dir: str = 'models'
    data_path: Optional[str] = None
    
    def validate(self) -> None:
        """Validate configuration parameters."""
        if self.n_samples < 100:
            raise ValueError("n_samples must be at least 100")
        if not 0 < self.test_size < 1:
            raise ValueError("test_size must be between 0 and 1")
        if self.cv_folds < 2:
            raise ValueError("cv_folds must be at least 2")
        if self.model_type not in ['random_forest', 'gradient_boost']:
            raise ValueError("model_type must be 'random_forest' or 'gradient_boost'")


class GitHubProfileDataset:
    """Handles dataset creation and preprocessing for GitHub profiles."""
    
    # Feature column definitions
    FEATURE_COLUMNS = [
        'profile_completeness',
        'repo_count',
        'total_stars',
        'languages_count',
        'recent_activity',
        'description_quality',
        'has_bio',
        'has_location',
        'has_company',
        'follower_count',
        'following_count',
        'avg_stars_per_repo',
        'follower_following_ratio'
    ]
    
    # Target column definitions
    TARGET_COLUMNS = [
        'needs_bio',
        'needs_repo_descriptions',
        'needs_activity_boost',
        'needs_language_showcase',
        'needs_pin_repos'
    ]
    
    def __init__(self, config: TrainingConfig):
        """Initialize dataset handler.
        
        Args:
            config: Training configuration object
        """
        self.config = config
        self.scaler: Optional[StandardScaler] = None
        
    def generate_synthetic_data(self) -> pd.DataFrame:
        """Generate synthetic GitHub profile data for training.
        
        This generates realistic profiles with correlated features and targets
        based on common GitHub profile patterns.
        
        Returns:
            DataFrame with synthetic profile data
            
        Raises:
            ValueError: If n_samples is invalid
        """
        n_samples = self.config.n_samples
        if n_samples < 1:
            raise ValueError(f"Invalid n_samples: {n_samples}")
            
        logger.info(f"Generating {n_samples} synthetic GitHub profiles...")
        
        # Set seed for reproducibility
        np.random.seed(self.config.random_state)
        
        # Generate base features with realistic distributions
        # Beta distribution for percentages (0-1)
        # Poisson for counts
        # Exponential for long-tail distributions (stars, followers)
        
        data = {
            # Profile completeness: beta(5,2) gives mean ~0.71
            'profile_completeness': np.clip(np.random.beta(5, 2, n_samples), 0, 1),
            
            # Repository count: Poisson mean=15
            'repo_count': np.clip(np.random.poisson(15, n_samples), 0, 200),
            
            # Total stars: Exponential scale=50, right-skewed
            'total_stars': np.clip(np.random.exponential(50, n_samples).astype(int), 0, 10000),
            
            # Languages: Most devs use 1-7 languages
            'languages_count': np.clip(np.random.randint(1, 8, n_samples), 1, 20),
            
            # Recent activity: beta(3,2) gives mean ~0.6
            'recent_activity': np.clip(np.random.beta(3, 2, n_samples), 0, 1),
            
            # Description quality: beta(4,2) gives mean ~0.67
            'description_quality': np.clip(np.random.beta(4, 2, n_samples), 0, 1),
            
            # Binary features: has_bio (70% have), has_location (75%), has_company (60%)
            'has_bio': np.random.choice([0, 1], n_samples, p=[0.3, 0.7]),
            'has_location': np.random.choice([0, 1], n_samples, p=[0.25, 0.75]),
            'has_company': np.random.choice([0, 1], n_samples, p=[0.4, 0.6]),
            
            # Follower/following counts: exponential distributions
            'follower_count': np.clip(np.random.exponential(100, n_samples).astype(int), 0, 50000),
            'following_count': np.clip(np.random.exponential(50, n_samples).astype(int), 0, 5000),
        }
        
        df = pd.DataFrame(data)
        
        # Calculate derived features
        df['avg_stars_per_repo'] = df['total_stars'] / (df['repo_count'] + 1)  # +1 to avoid division by zero
        df['follower_following_ratio'] = df['follower_count'] / (df['following_count'] + 1)
        
        # Generate success score (0-1 scale) - weighted combination of features
        df['profile_success_score'] = self._calculate_success_score(df)
        
        # Generate recommendation targets based on business logic
        df = self._generate_targets(df)
        
        logger.info(f"Generated dataset shape: {df.shape}")
        logger.info(f"Feature columns: {len(self.FEATURE_COLUMNS)}")
        logger.info(f"Target columns: {len(self.TARGET_COLUMNS)}")
        
        # Log target distribution
        for target in self.TARGET_COLUMNS:
            positive_rate = df[target].mean()
            logger.info(f"  {target}: {positive_rate:.2%} positive samples")
        
        return df
    
    def _calculate_success_score(self, df: pd.DataFrame) -> pd.Series:
        """Calculate profile success score based on multiple factors.
        
        Args:
            df: Input DataFrame with features
            
        Returns:
            Series with success scores (0-1)
        """
        # Weighted combination of normalized features
        score = (
            0.25 * df['profile_completeness'] +
            0.20 * np.clip(np.log1p(df['total_stars']) / 10, 0, 1) +
            0.20 * df['recent_activity'] +
            0.15 * df['description_quality'] +
            0.20 * np.clip(np.log1p(df['follower_count']) / 10, 0, 1)
        )
        
        # Normalize to 0-1 range
        return np.clip(score, 0, 1)
    
    def _generate_targets(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate target labels based on business rules.
        
        Args:
            df: Input DataFrame with features
            
        Returns:
            DataFrame with added target columns
        """
        # needs_bio: Missing bio AND low profile completeness
        df['needs_bio'] = (
            (df['has_bio'] == 0) & 
            (df['profile_completeness'] < 0.6)
        ).astype(int)
        
        # needs_repo_descriptions: Low description quality
        df['needs_repo_descriptions'] = (
            df['description_quality'] < 0.5
        ).astype(int)
        
        # needs_activity_boost: Low recent activity
        df['needs_activity_boost'] = (
            df['recent_activity'] < 0.4
        ).astype(int)
        
        # needs_language_showcase: High language diversity not showcased
        df['needs_language_showcase'] = (
            (df['languages_count'] >= 4) &
            (df['profile_completeness'] < 0.7)
        ).astype(int)
        
        # needs_pin_repos: Popular repos exist but not highlighted
        df['needs_pin_repos'] = (
            (df['total_stars'] > 20) & 
            (df['repo_count'] > 5) &
            (df['profile_completeness'] < 0.8)
        ).astype(int)
        
        return df
    
    def load_real_data(self) -> pd.DataFrame:
        """Load real GitHub profile data from JSON file.
        
        Expected JSON format:
        [
            {
                "profile_completeness": 0.8,
                "repo_count": 25,
                ...
            },
            ...
        ]
        
        Returns:
            DataFrame with real profile data
            
        Raises:
            FileNotFoundError: If data file doesn't exist
            ValueError: If data format is invalid
        """
        data_path = self.config.data_path
        
        if not data_path:
            logger.warning("No data path provided, generating synthetic data")
            return self.generate_synthetic_data()
        
        path = Path(data_path)
        if not path.exists():
            raise FileNotFoundError(f"Data file not found: {data_path}")
        
        logger.info(f"Loading data from {data_path}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                raise ValueError("JSON data must be a list of profile objects")
            
            df = pd.DataFrame(data)
            
            # Validate required columns exist
            missing_features = set(self.FEATURE_COLUMNS) - set(df.columns)
            if missing_features:
                raise ValueError(f"Missing required features: {missing_features}")
            
            logger.info(f"Loaded {len(df)} real profiles")
            return df
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
    
    def preprocess_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, StandardScaler]:
        """Preprocess features for model training.
        
        Steps:
        1. Select feature columns
        2. Handle missing values (fill with 0)
        3. Standardize features (mean=0, std=1)
        
        Args:
            df: Input DataFrame with raw features
            
        Returns:
            Tuple of (scaled features DataFrame, fitted scaler)
            
        Raises:
            ValueError: If required feature columns are missing
        """
        logger.info("Preprocessing features...")
        
        # Validate feature columns exist
        missing_cols = set(self.FEATURE_COLUMNS) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing feature columns: {missing_cols}")
        
        # Select and copy feature columns
        X = df[self.FEATURE_COLUMNS].copy()
        
        # Log missing value statistics
        missing_counts = X.isnull().sum()
        if missing_counts.any():
            logger.warning("Missing values detected:")
            for col, count in missing_counts[missing_counts > 0].items():
                logger.warning(f"  {col}: {count} missing ({count/len(X):.2%})")
        
        # Fill missing values with 0 (conservative approach)
        X = X.fillna(0)
        
        # Fit and transform scaler
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Convert back to DataFrame for easier handling
        X_scaled_df = pd.DataFrame(
            X_scaled, 
            columns=self.FEATURE_COLUMNS, 
            index=X.index
        )
        
        # Log scaling statistics
        logger.info(f"Features scaled: {X_scaled_df.shape[1]} columns")
        logger.info(f"Feature means: min={X_scaled_df.mean().min():.3f}, max={X_scaled_df.mean().max():.3f}")
        logger.info(f"Feature stds: min={X_scaled_df.std().min():.3f}, max={X_scaled_df.std().max():.3f}")
        
        self.scaler = scaler
        return X_scaled_df, scaler


class RecommendationModel:
    """Multi-output model for generating GitHub profile recommendations."""
    
    def __init__(self, config: TrainingConfig):
        """Initialize recommendation model.
        
        Args:
            config: Training configuration object
        """
        self.config = config
        self.models: Dict[str, Any] = {}
        self.scaler: Optional[StandardScaler] = None
        self.feature_names: Optional[List[str]] = None
        self.training_metrics: Dict[str, Dict[str, float]] = {}
        
    def _get_base_classifier(self):
        """Get base classifier based on configuration.
        
        Returns:
            Unfitted classifier instance
        """
        if self.config.model_type == 'random_forest':
            return RandomForestClassifier(
                random_state=self.config.random_state,
                n_jobs=-1,
                class_weight='balanced'  # Handle imbalanced classes
            )
        elif self.config.model_type == 'gradient_boost':
            return GradientBoostingClassifier(
                random_state=self.config.random_state
            )
        else:
            raise ValueError(f"Unknown model type: {self.config.model_type}")
    
    def _get_param_grid(self) -> Dict[str, List]:
        """Get hyperparameter grid for tuning.
        
        Returns:
            Dictionary of hyperparameter ranges
        """
        if self.config.model_type == 'random_forest':
            return {
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 20, 30, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4],
                'max_features': ['sqrt', 'log2']
            }
        else:  # gradient_boost
            return {
                'n_estimators': [100, 200, 300],
                'learning_rate': [0.01, 0.05, 0.1, 0.2],
                'max_depth': [3, 5, 7],
                'min_samples_split': [2, 5, 10],
                'subsample': [0.8, 0.9, 1.0]
            }
    
    def train(self, X: pd.DataFrame, y: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Train classification models for each recommendation type.
        
        Args:
            X: Feature DataFrame (already scaled)
            y: Target DataFrame with recommendation columns
            
        Returns:
            Dictionary with training metrics for each model
            
        Raises:
            ValueError: If target columns are missing
        """
        logger.info(f"Training {self.config.model_type} models...")
        logger.info(f"Training samples: {len(X)}")
        
        self.feature_names = X.columns.tolist()
        
        # Validate target columns
        missing_targets = set(GitHubProfileDataset.TARGET_COLUMNS) - set(y.columns)
        if missing_targets:
            raise ValueError(f"Missing target columns: {missing_targets}")
        
        for rec_type in GitHubProfileDataset.TARGET_COLUMNS:
            logger.info(f"\n{'='*60}")
            logger.info(f"Training model for: {rec_type}")
            logger.info(f"{'='*60}")
            
            # Check class distribution
            class_dist = y[rec_type].value_counts()
            logger.info(f"Class distribution:\n{class_dist}")
            
            if len(class_dist) < 2:
                logger.warning(f"Skipping {rec_type}: only one class present")
                continue
            
            # Split data with stratification to preserve class distribution
            try:
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y[rec_type],
                    test_size=self.config.test_size,
                    random_state=self.config.random_state,
                    stratify=y[rec_type]
                )
            except ValueError as e:
                logger.error(f"Failed to split data for {rec_type}: {e}")
                continue
            
            # Initialize base model
            base_model = self._get_base_classifier()
            
            # Train with or without hyperparameter tuning
            if self.config.tune_hyperparameters:
                model = self._tune_model(base_model, X_train, y_train, rec_type)
            else:
                logger.info("Training with default parameters...")
                base_model.fit(X_train, y_train)
                model = base_model
            
            # Evaluate model
            metrics = self._evaluate_model(model, X_train, X_test, y_train, y_test, rec_type)
            
            # Store model and metrics
            self.models[rec_type] = model
            self.training_metrics[rec_type] = metrics
            
            # Log feature importance
            self._log_feature_importance(model, rec_type)
        
        return self.training_metrics
    
    def _tune_model(self, base_model, X_train, y_train, rec_type: str):
        """Tune model hyperparameters using grid search.
        
        Args:
            base_model: Base model instance
            X_train: Training features
            y_train: Training targets
            rec_type: Recommendation type name
            
        Returns:
            Best model from grid search
        """
        logger.info(f"Performing hyperparameter tuning...")
        
        param_grid = self._get_param_grid()
        
        grid_search = GridSearchCV(
            estimator=base_model,
            param_grid=param_grid,
            cv=self.config.cv_folds,
            scoring='f1',
            n_jobs=-1,
            verbose=1,
            error_score='raise'
        )
        
        grid_search.fit(X_train, y_train)
        
        logger.info(f"Best parameters: {grid_search.best_params_}")
        logger.info(f"Best CV F1 score: {grid_search.best_score_:.3f}")
        
        return grid_search.best_estimator_
    
    def _evaluate_model(self, model, X_train, X_test, y_train, y_test, 
                        rec_type: str) -> Dict[str, float]:
        """Evaluate trained model and compute metrics.
        
        Args:
            model: Trained model
            X_train: Training features
            X_test: Test features
            y_train: Training targets
            y_test: Test targets
            rec_type: Recommendation type name
            
        Returns:
            Dictionary with evaluation metrics
        """
        # Predictions
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        # Classification report
        report = classification_report(y_test, y_pred_test, output_dict=True, zero_division=0)
        
        # Cross-validation scores
        cv_scores = cross_val_score(
            model, X_train, y_train,
            cv=self.config.cv_folds,
            scoring='f1',
            n_jobs=-1
        )
        
        metrics = {
            'train_accuracy': accuracy_score(y_train, y_pred_train),
            'test_accuracy': accuracy_score(y_test, y_pred_test),
            'f1_score': report['weighted avg']['f1-score'],
            'precision': report['weighted avg']['precision'],
            'recall': report['weighted avg']['recall'],
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
        
        # Log metrics
        logger.info(f"\nMetrics for {rec_type}:")
        logger.info(f"  Train Accuracy: {metrics['train_accuracy']:.3f}")
        logger.info(f"  Test Accuracy:  {metrics['test_accuracy']:.3f}")
        logger.info(f"  F1 Score:       {metrics['f1_score']:.3f}")
        logger.info(f"  Precision:      {metrics['precision']:.3f}")
        logger.info(f"  Recall:         {metrics['recall']:.3f}")
        logger.info(f"  CV Score:       {metrics['cv_mean']:.3f} ± {metrics['cv_std']:.3f}")
        
        # Check for overfitting
        accuracy_diff = metrics['train_accuracy'] - metrics['test_accuracy']
        if accuracy_diff > 0.15:
            logger.warning(f"⚠️  Potential overfitting detected (train-test gap: {accuracy_diff:.3f})")
        
        return metrics
    
    def _log_feature_importance(self, model, rec_type: str, top_n: int = 5):
        """Log top important features for the model.
        
        Args:
            model: Trained model
            rec_type: Recommendation type name
            top_n: Number of top features to display
        """
        if not hasattr(model, 'feature_importances_'):
            return
        
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1][:top_n]
        
        logger.info(f"\nTop {top_n} features for {rec_type}:")
        for i, idx in enumerate(indices, 1):
            logger.info(f"  {i}. {self.feature_names[idx]}: {importances[idx]:.4f}")
    
    def train_impact_predictor(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Train a regression model to predict recommendation impact scores.
        
        This model predicts how much a recommendation will improve the profile.
        
        Args:
            X: Feature DataFrame (already scaled)
            y: Target series with success scores
            
        Returns:
            Dictionary with regression metrics
        """
        logger.info("\n" + "="*60)
        logger.info("Training Impact Prediction Model")
        logger.info("="*60)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=self.config.test_size,
            random_state=self.config.random_state
        )
        
        logger.info(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")
        
        # Initialize regression model
        model = GradientBoostingRegressor(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=5,
            min_samples_split=5,
            min_samples_leaf=2,
            subsample=0.9,
            random_state=self.config.random_state,
            verbose=0
        )
        
        # Train
        logger.info("Training regression model...")
        model.fit(X_train, y_train)
        
        # Predict
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        # Calculate metrics
        metrics = {
            'train_mse': mean_squared_error(y_train, y_pred_train),
            'test_mse': mean_squared_error(y_test, y_pred_test),
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, y_pred_test)),
            'train_r2': r2_score(y_train, y_pred_train),
            'test_r2': r2_score(y_test, y_pred_test)
        }
        
        # Log metrics
        logger.info("\nImpact Predictor Metrics:")
        logger.info(f"  Train RMSE: {metrics['train_rmse']:.4f}")
        logger.info(f"  Test RMSE:  {metrics['test_rmse']:.4f}")
        logger.info(f"  Train R²:   {metrics['train_r2']:.4f}")
        logger.info(f"  Test R²:    {metrics['test_r2']:.4f}")
        
        # Check for overfitting
        r2_diff = metrics['train_r2'] - metrics['test_r2']
        if r2_diff > 0.15:
            logger.warning(f"⚠️  Potential overfitting detected (train-test R² gap: {r2_diff:.3f})")
        
        # Store model
        self.models['impact_predictor'] = model
        self.training_metrics['impact_predictor'] = metrics
        
        return metrics
    
    def save_model(self) -> Path:
        """Save trained models and metadata to disk.
        
        Returns:
            Path to saved model file
            
        Raises:
            ValueError: If no models have been trained
        """
        if not self.models:
            raise ValueError("No models to save. Train models first.")
        
        output_path = Path(self.config.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        model_name = f'github_optimizer_{self.config.model_type}_{timestamp}.pkl'
        
        # Prepare model data
        model_data = {
            'models': self.models,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'recommendation_types': GitHubProfileDataset.TARGET_COLUMNS,
            'model_type': self.config.model_type,
            'training_config': asdict(self.config),
            'training_metrics': self.training_metrics,
            'timestamp': timestamp
        }
        
        # Save model
        model_file = output_path / model_name
        joblib.dump(model_data, model_file, compress=3)
        logger.info(f"✓ Model saved to: {model_file}")
        
        # Save human-readable metadata
        metadata = {
            'model_file': model_name,
            'timestamp': timestamp,
            'model_type': self.config.model_type,
            'feature_names': self.feature_names,
            'recommendation_types': GitHubProfileDataset.TARGET_COLUMNS,
            'training_config': asdict(self.config),
            'training_metrics': self.training_metrics
        }
        
        metadata_file = output_path / f'metadata_{timestamp}.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, default=str)
        
        logger.info(f"✓ Metadata saved to: {metadata_file}")
        
        return model_file
    
    def predict_recommendations(self, X: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Predict recommendations for new profiles.
        
        Args:
            X: Feature DataFrame (should be scaled using the same scaler)
            
        Returns:
            Dictionary mapping recommendation types to probability arrays
            
        Raises:
            ValueError: If models haven't been trained
        """
        if not self.models:
            raise ValueError("No models available. Train or load models first.")
        
        predictions = {}
        
        for rec_type in GitHubProfileDataset.TARGET_COLUMNS:
            if rec_type not in self.models:
                logger.warning(f"Model for {rec_type} not found, skipping...")
                continue
            
            model = self.models[rec_type]
            # Get probability of positive class (needs recommendation)
            predictions[rec_type] = model.predict_proba(X)[:, 1]
        
        return predictions


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Train GitHub Profile Optimizer ML models',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        '--samples', type=int, default=2000,
        help='Number of synthetic samples to generate'
    )
    parser.add_argument(
        '--data-path', type=str, default=None,
        help='Path to real data JSON file (if available)'
    )
    parser.add_argument(
        '--model-type', type=str, default='random_forest',
        choices=['random_forest', 'gradient_boost'],
        help='Type of classification model to use'
    )
    parser.add_argument(
        '--no-tune', action='store_true',
        help='Disable hyperparameter tuning (faster but less optimal)'
    )
    parser.add_argument(
        '--test-size', type=float, default=0.2,
        help='Fraction of data to use for testing'
    )
    parser.add_argument(
        '--cv-folds', type=int, default=5,
        help='Number of cross-validation folds'
    )
    parser.add_argument(
        '--output-dir', type=str, default='models',
        help='Directory to save trained models'
    )
    parser.add_argument(
        '--random-seed', type=int, default=42,
        help='Random seed for reproducibility'
    )
    
    return parser.parse_args()


def main():
    """Main training pipeline with comprehensive error handling."""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Create configuration
        config = TrainingConfig(
            n_samples=args.samples,
            test_size=args.test_size,
            random_state=args.random_seed,
            cv_folds=args.cv_folds,
            tune_hyperparameters=not args.no_tune,
            model_type=args.model_type,
            output_dir=args.output_dir,
            data_path=args.data_path
        )
        
        # Validate configuration
        config.validate()
        
        logger.info("\n" + "="*70)
        logger.info("GitHub Profile Optimizer - Model Training Pipeline")
        logger.info("="*70)
        logger.info(f"Configuration:")
        logger.info(f"  Samples: {config.n_samples}")
        logger.info(f"  Model Type: {config.model_type}")
        logger.info(f"  Hyperparameter Tuning: {config.tune_hyperparameters}")
        logger.info(f"  Test Size: {config.test_size}")
        logger.info(f"  CV Folds: {config.cv_folds}")
        logger.info(f"  Output Directory: {config.output_dir}")
        logger.info(f"  Random Seed: {config.random_state}")
        logger.info("="*70 + "\n")
        
        # Step 1: Prepare dataset
        logger.info("STEP 1: Preparing Dataset")
        logger.info("-" * 70)
        dataset = GitHubProfileDataset(config)
        
        if config.data_path:
            try:
                df = dataset.load_real_data()
                logger.info("✓ Real data loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load real data: {e}")
                logger.info("Falling back to synthetic data generation...")
                df = dataset.generate_synthetic_data()
        else:
            df = dataset.generate_synthetic_data()
        
        logger.info(f"✓ Dataset ready: {df.shape[0]} samples, {df.shape[1]} columns\n")
        
        # Step 2: Preprocess features
        logger.info("STEP 2: Preprocessing Features")
        logger.info("-" * 70)
        X, scaler = dataset.preprocess_features(df)
        logger.info("✓ Features preprocessed and scaled\n")
        
        # Step 3: Prepare targets
        logger.info("STEP 3: Preparing Target Variables")
        logger.info("-" * 70)
        y_classification = df[GitHubProfileDataset.TARGET_COLUMNS]
        y_regression = df['profile_success_score']
        
        logger.info(f"Classification targets: {len(GitHubProfileDataset.TARGET_COLUMNS)}")
        logger.info(f"Regression target: profile_success_score")
        logger.info(f"✓ Targets prepared\n")
        
        # Step 4: Train recommendation classifiers
        logger.info("STEP 4: Training Recommendation Classifiers")
        logger.info("-" * 70)
        model = RecommendationModel(config)
        model.scaler = scaler
        
        classification_metrics = model.train(X, y_classification)
        logger.info("✓ Classification models trained\n")
        
        # Step 5: Train impact predictor
        logger.info("STEP 5: Training Impact Predictor")
        logger.info("-" * 70)
        impact_metrics = model.train_impact_predictor(X, y_regression)
        logger.info("✓ Impact predictor trained\n")
        
        # Step 6: Save models
        logger.info("STEP 6: Saving Models")
        logger.info("-" * 70)
        model_path = model.save_model()
        logger.info("✓ All models saved successfully\n")
        
        # Step 7: Generate training summary
        logger.info("="*70)
        logger.info("TRAINING COMPLETE - SUMMARY")
        logger.info("="*70)
        
        logger.info("\n📊 Classification Model Performance:")
        logger.info("-" * 70)
        for rec_type, metrics in classification_metrics.items():
            logger.info(f"\n{rec_type}:")
            logger.info(f"  Test Accuracy:  {metrics['test_accuracy']:.3f}")
            logger.info(f"  F1 Score:       {metrics['f1_score']:.3f}")
            logger.info(f"  Precision:      {metrics['precision']:.3f}")
            logger.info(f"  Recall:         {metrics['recall']:.3f}")
            logger.info(f"  CV Score:       {metrics['cv_mean']:.3f} ± {metrics['cv_std']:.3f}")
        
        logger.info("\n📈 Impact Predictor Performance:")
        logger.info("-" * 70)
        logger.info(f"  Test RMSE:  {impact_metrics['test_rmse']:.4f}")
        logger.info(f"  Test R²:    {impact_metrics['test_r2']:.4f}")
        
        logger.info("\n💾 Saved Artifacts:")
        logger.info("-" * 70)
        logger.info(f"  Model File: {model_path}")
        logger.info(f"  Log File:   training.log")
        
        logger.info("\n🚀 Next Steps:")
        logger.info("-" * 70)
        logger.info("1. Review training.log for detailed training information")
        logger.info("2. Check metadata JSON for model specifications")
        logger.info("3. Integrate model into predictive_optimizer.py:")
        logger.info(f"   optimizer = PredictiveOptimizer(model_path='{model_path}')")
        logger.info("4. Test model with real GitHub profiles")
        logger.info("5. Monitor model performance and retrain if needed")
        
        logger.info("\n" + "="*70)
        logger.info("✅ Training pipeline completed successfully!")
        logger.info("="*70 + "\n")
        
        return 0
        
    except KeyboardInterrupt:
        logger.error("\n❌ Training interrupted by user")
        return 130
        
    except ValueError as e:
        logger.error(f"\n❌ Configuration error: {e}")
        return 1
        
    except Exception as e:
        logger.error(f"\n❌ Unexpected error during training: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    exit(main())