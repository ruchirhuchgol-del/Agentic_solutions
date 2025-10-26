"""
ML-powered predictive optimization engine.

Provides machine learning capabilities for predictive GitHub profile optimization.
"""

import json
from typing import List, Dict, Any
from dataclasses import dataclass
import numpy as np
import pandas as pd
from ..models.github import GitHubProfile, GitHubRepository
from ..utils.logger import get_logger


@dataclass
class Recommendation:
    """
    Recommendation for profile improvement.
    
    Contains a specific recommendation for improving a GitHub profile
    with confidence scoring and implementation guidance.
    """
    type: str
    target: str
    confidence: float
    impact_score: float
    description: str = ""
    implementation_steps: List[str] = None
    
    def __post_init__(self):
        if self.implementation_steps is None:
            self.implementation_steps = []


class PredictiveOptimizer:
    """
    ML-powered predictive optimizer for GitHub profiles.
    
    Provides predictive analytics and recommendation generation
    for optimizing GitHub profiles based on machine learning models.
    """
    
    def __init__(self, model_path: str = None):
        """
        Initialize predictive optimizer.
        
        Args:
            model_path: Path to trained model (None for default rules-based approach)
        """
        self.logger = get_logger(self.__class__.__name__)
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.recommendation_types = None
        
        # Load model if path provided
        if model_path:
            self._load_model(model_path)
        else:
            self.logger.info("Using rules-based prediction engine")
    
    def _load_model(self, model_path: str) -> None:
        """
        Load trained ML model.
        
        Args:
            model_path: Path to trained model
        """
        try:
            # Import joblib only when needed
            import joblib
            model_data = joblib.load(model_path)
            
            self.model = model_data.get('models', {})
            self.scaler = model_data.get('scaler')
            self.feature_names = model_data.get('feature_names')
            self.recommendation_types = model_data.get('recommendation_types')
            
            self.logger.info(f"Model loaded successfully from {model_path}")
            self.logger.info(f"Loaded {len(self.model)} models for recommendation types: {list(self.model.keys())}")
        except Exception as e:
            self.logger.error(f"Failed to load model from {model_path}: {e}")
            # Fall back to rules-based approach
            self.model = None
    
    def suggest_improvements(self, profile: GitHubProfile, 
                           repositories: List[GitHubRepository]) -> List[Recommendation]:
        """
        Generate predictive recommendations for profile improvements.
        
        Args:
            profile: GitHub profile data
            repositories: List of repositories
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Use ML model if available, otherwise use rules-based approach
        if self.model and self.scaler and self.feature_names:
            recommendations = self._ml_based_recommendations(profile, repositories)
        else:
            recommendations = self._rules_based_recommendations(profile, repositories)
            
        self.logger.info(f"Generated {len(recommendations)} recommendations")
        return recommendations
    
    def _ml_based_recommendations(self, profile: GitHubProfile, 
                                repositories: List[GitHubRepository]) -> List[Recommendation]:
        """
        Generate recommendations using ML model.
        
        Args:
            profile: GitHub profile data
            repositories: List of repositories
            
        Returns:
            List of recommendations
        """
        try:
            # Extract features
            features = self._extract_features(profile, repositories)
            
            # Convert to DataFrame
            X = pd.DataFrame([features], columns=self.feature_names)
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            X_scaled_df = pd.DataFrame(X_scaled, columns=self.feature_names)
            
            # Get predictions
            predictions = {}
            impact_score = 0.5  # Default impact score
            
            # Get recommendation predictions
            for rec_type in self.recommendation_types:
                if rec_type in self.model:
                    model = self.model[rec_type]
                    if hasattr(model, 'predict_proba'):
                        # Get probability of positive class (needs recommendation)
                        prob = model.predict_proba(X_scaled_df)[:, 1]
                        predictions[rec_type] = prob[0]
                    else:
                        # For models without predict_proba, use predict
                        pred = model.predict(X_scaled_df)
                        predictions[rec_type] = pred[0]
            
            # Get impact score if impact predictor exists
            if 'impact_predictor' in self.model:
                impact_model = self.model['impact_predictor']
                if hasattr(impact_model, 'predict'):
                    impact_score = max(0.0, min(1.0, impact_model.predict(X_scaled_df)[0]))
            
            # Convert predictions to recommendations
            recommendations = self._convert_predictions_to_recommendations(
                predictions, profile, repositories, impact_score
            )
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error in ML-based recommendations: {e}")
            # Fall back to rules-based approach
            return self._rules_based_recommendations(profile, repositories)
    
    def _convert_predictions_to_recommendations(self, predictions: Dict[str, float], 
                                              profile: GitHubProfile, 
                                              repositories: List[GitHubRepository],
                                              impact_score: float) -> List[Recommendation]:
        """
        Convert model predictions to recommendation objects.
        
        Args:
            predictions: Dictionary of prediction probabilities
            profile: GitHub profile data
            repositories: List of repositories
            impact_score: Predicted impact score
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Convert each prediction to a recommendation
        for rec_type, confidence in predictions.items():
            # Only create recommendations with confidence above threshold
            if confidence > 0.3:  # 30% threshold
                recommendation = self._create_recommendation_from_type(
                    rec_type, confidence, impact_score, profile, repositories
                )
                if recommendation:
                    recommendations.append(recommendation)
        
        return recommendations
    
    def _create_recommendation_from_type(self, rec_type: str, confidence: float, 
                                       impact_score: float, profile: GitHubProfile, 
                                       repositories: List[GitHubRepository]) -> Recommendation:
        """
        Create a recommendation object based on the recommendation type.
        
        Args:
            rec_type: Type of recommendation
            confidence: Confidence score from model
            impact_score: Predicted impact score
            profile: GitHub profile data
            repositories: List of repositories
            
        Returns:
            Recommendation object or None
        """
        if rec_type == 'needs_bio' and not profile.bio:
            return Recommendation(
                type="profile",
                target="bio",
                confidence=confidence,
                impact_score=impact_score,
                description="Add a professional bio to your profile",
                implementation_steps=[
                    "Write 2-3 sentences describing your skills and experience",
                    "Include relevant technologies and domains you work with",
                    "Mention your career goals or interests"
                ]
            )
        elif rec_type == 'needs_repo_descriptions':
            poorly_described = [r for r in repositories if not r.description]
            if poorly_described:
                return Recommendation(
                    type="repo_quality",
                    target="descriptions",
                    confidence=confidence,
                    impact_score=impact_score,
                    description=f"Add descriptions to {len(poorly_described)} repositories",
                    implementation_steps=[
                        "Write clear, concise descriptions for each repository",
                        "Include the main purpose and technologies used",
                        "Add relevant keywords for discoverability"
                    ]
                )
        elif rec_type == 'needs_activity_boost':
            return Recommendation(
                type="activity",
                target="contribution",
                confidence=confidence,
                impact_score=impact_score,
                description="Increase your contribution activity",
                implementation_steps=[
                    "Work on open issues in your repositories",
                    "Merge pull requests regularly",
                    "Update documentation and README files"
                ]
            )
        elif rec_type == 'needs_language_showcase':
            languages = set(r.language for r in repositories if r.language)
            if len(languages) > 3:
                return Recommendation(
                    type="showcase",
                    target="skills",
                    confidence=confidence,
                    impact_score=impact_score,
                    description="Showcase your language diversity in profile",
                    implementation_steps=[
                        "Create a skills section in your bio",
                        "List the main programming languages you work with",
                        "Mention any frameworks or tools you specialize in"
                    ]
                )
        elif rec_type == 'needs_pin_repos':
            if repositories:
                most_starred = max(repositories, key=lambda r: r.stars)
                if most_starred.stars > 10:
                    return Recommendation(
                        type="pin_repo",
                        target=most_starred.name,
                        confidence=confidence,
                        impact_score=impact_score,
                        description=f"Pin your most popular repository: {most_starred.name}",
                        implementation_steps=[
                            "Go to your GitHub profile",
                            f"Pin the {most_starred.name} repository",
                            "Add a short description if missing"
                        ]
                    )
        
        return None
    
    def _rules_based_recommendations(self, profile: GitHubProfile, 
                                   repositories: List[GitHubRepository]) -> List[Recommendation]:
        """
        Generate recommendations using rules-based approach.
        
        Args:
            profile: GitHub profile data
            repositories: List of repositories
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Profile completeness recommendations
        if not profile.bio:
            recommendations.append(Recommendation(
                type="profile",
                target="bio",
                confidence=0.95,
                impact_score=0.85,
                description="Add a professional bio to your profile",
                implementation_steps=[
                    "Write 2-3 sentences describing your skills and experience",
                    "Include relevant technologies and domains you work with",
                    "Mention your career goals or interests"
                ]
            ))
        
        if not profile.location:
            recommendations.append(Recommendation(
                type="profile",
                target="location",
                confidence=0.85,
                impact_score=0.65,
                description="Add your location to improve discoverability",
                implementation_steps=[
                    "Add your city and country",
                    "Consider adding timezone for collaboration"
                ]
            ))
        
        if not profile.company:
            recommendations.append(Recommendation(
                type="profile",
                target="company",
                confidence=0.80,
                impact_score=0.70,
                description="Add your company or organization",
                implementation_steps=[
                    "Include your current employer",
                    "Add previous companies if relevant"
                ]
            ))
        
        # Repository recommendations
        if repositories:
            # Find most starred repository
            most_starred = max(repositories, key=lambda r: r.stars)
            if most_starred.stars > 10:
                recommendations.append(Recommendation(
                    type="pin_repo",
                    target=most_starred.name,
                    confidence=0.90,
                    impact_score=0.80,
                    description=f"Pin your most popular repository: {most_starred.name}",
                    implementation_steps=[
                        "Go to your GitHub profile",
                        f"Pin the {most_starred.name} repository",
                        "Add a short description if missing"
                    ]
                ))
            
            # Repository quality recommendations
            poorly_described = [r for r in repositories if not r.description]
            if poorly_described:
                recommendations.append(Recommendation(
                    type="repo_quality",
                    target="descriptions",
                    confidence=0.85,
                    impact_score=0.75,
                    description=f"Add descriptions to {len(poorly_described)} repositories",
                    implementation_steps=[
                        "Write clear, concise descriptions for each repository",
                        "Include the main purpose and technologies used",
                        "Add relevant keywords for discoverability"
                    ]
                ))
            
            # Language diversity recommendation
            languages = set(r.language for r in repositories if r.language)
            if len(languages) > 3:
                recommendations.append(Recommendation(
                    type="showcase",
                    target="skills",
                    confidence=0.80,
                    impact_score=0.70,
                    description="Showcase your language diversity in profile",
                    implementation_steps=[
                        "Create a skills section in your bio",
                        "List the main programming languages you work with",
                        "Mention any frameworks or tools you specialize in"
                    ]
                ))
        
        # Activity recommendations
        if repositories:
            # Find recently updated repositories
            recent_repos = [r for r in repositories if r.updated_at]
            if recent_repos:
                recommendations.append(Recommendation(
                    type="activity",
                    target="contribution",
                    confidence=0.75,
                    impact_score=0.80,
                    description="Maintain consistent contribution activity",
                    implementation_steps=[
                        "Work on open issues in your repositories",
                        "Merge pull requests regularly",
                        "Update documentation and README files"
                    ]
                ))
        
        return recommendations
    
    def _extract_features(self, profile: GitHubProfile, 
                         repositories: List[GitHubRepository]) -> Dict[str, Any]:
        """
        Extract features from profile and repositories for ML model.
        
        Args:
            profile: GitHub profile data
            repositories: List of repositories
            
        Returns:
            Feature dictionary
        """
        # Calculate derived metrics
        repo_count = len(repositories)
        total_stars = sum(r.stars for r in repositories)
        languages = set(r.language for r in repositories if r.language)
        languages_count = len(languages)
        
        # Profile completeness (0-1 scale)
        profile_fields = [
            profile.name,
            profile.bio,
            profile.location,
            profile.company,
            profile.blog,
            profile.email
        ]
        profile_completeness = sum(1 for field in profile_fields if field) / len(profile_fields) if profile_fields else 0
        
        # Recent activity (simplified as repository count normalized)
        recent_activity = min(repo_count / 20.0, 1.0)
        
        # Description quality
        described_repos = [r for r in repositories if r.description]
        description_quality = len(described_repos) / repo_count if repo_count > 0 else 0
        
        # Average stars per repo
        avg_stars_per_repo = total_stars / repo_count if repo_count > 0 else 0
        
        # Follower/following ratio (using dummy values since not in model)
        follower_count = getattr(profile, 'followers', 100)
        following_count = getattr(profile, 'following', 50)
        follower_following_ratio = follower_count / (following_count + 1)
        
        features = {
            'profile_completeness': profile_completeness,
            'repo_count': repo_count,
            'total_stars': total_stars,
            'languages_count': languages_count,
            'recent_activity': recent_activity,
            'description_quality': description_quality,
            'has_bio': 1 if profile.bio else 0,
            'has_location': 1 if profile.location else 0,
            'has_company': 1 if profile.company else 0,
            'follower_count': follower_count,
            'following_count': following_count,
            'avg_stars_per_repo': avg_stars_per_repo,
            'follower_following_ratio': follower_following_ratio
        }
        
        return features


# Global predictive optimizer instance
predictive_optimizer = PredictiveOptimizer()