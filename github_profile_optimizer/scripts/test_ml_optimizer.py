#
"""
Test script to demonstrate the ML-powered predictive optimizer.
This script shows how to use a trained model with the predictive optimizer
to generate intelligent recommendations for GitHub profiles.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def test_ml_optimizer():
    """Test the ML-powered predictive optimizer."""
    try:
        from src.github_profile_optimizer.ml.predictive_optimizer import PredictiveOptimizer
        from src.github_profile_optimizer.models.github import GitHubProfile, GitHubRepository
        
        print("Testing ML-powered Predictive Optimizer...")
        print("=" * 50)
        
        # First, let's try to use a trained model if one exists
        # Look for trained models in the models directory
        models_dir = Path("models")
        model_files = list(models_dir.glob("github_optimizer_*.pkl")) if models_dir.exists() else []
        
        if model_files:
            # Use the most recent model
            model_path = str(model_files[0])
            print(f"Found trained model: {model_path}")
            optimizer = PredictiveOptimizer(model_path=model_path)
            print("✓ ML-based optimizer initialized successfully")
        else:
            # Fall back to rules-based approach
            print("No trained model found, using rules-based approach")
            optimizer = PredictiveOptimizer()
            print("✓ Rules-based optimizer initialized successfully")
        
        # Create sample profile and repositories
        profile = GitHubProfile(
            login="testuser",
            name="Test User",
            bio=None,  # Intentionally empty to trigger recommendation
            location="Test Location",
            company="Test Company",
            blog="https://test.example.com",
            email="test@example.com",
            public_repos=15,
            followers=100,
            following=50,
            created_at="2020-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z"
        )
        
        repositories = [
            GitHubRepository(
                name="test-repo-1",
                description="A test repository with a good description",
                language="Python",
                stargazers_count=50,
                forks=10,
                private=False,
                updated_at="2023-01-01T00:00:00Z"
            ),
            GitHubRepository(
                name="test-repo-2",
                description="",  # Empty description to trigger recommendation
                language="JavaScript",
                stargazers_count=25,
                forks=5,
                private=True,
                updated_at="2023-01-01T00:00:00Z"
            ),
            GitHubRepository(
                name="test-repo-3",
                description="Another test repository",
                language="Python",
                stargazers_count=150,
                forks=20,
                private=False,
                updated_at="2023-01-01T00:00:00Z"
            )
        ]
        
        # Generate recommendations
        recommendations = optimizer.suggest_improvements(profile, repositories)
        
        print(f"\nGenerated {len(recommendations)} recommendations:")
        print("-" * 50)
        
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. [{rec.type}] {rec.target}")
            print(f"   Confidence: {rec.confidence:.2f}")
            print(f"   Impact Score: {rec.impact_score:.2f}")
            print(f"   Description: {rec.description}")
            print(f"   Steps:")
            for step in rec.implementation_steps:
                print(f"     - {step}")
            print()
        
        print("✓ ML-powered recommendations generated successfully")
        return True
        
    except Exception as e:
        print(f"❌ ML optimizer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run the ML optimizer test."""
    print("GitHub Profile Optimizer - ML Testing")
    print("=" * 50)
    
    if test_ml_optimizer():
        print("\n" + "=" * 50)
        print("SUCCESS: ML optimizer test completed!")
        return 0
    else:
        print("\n" + "=" * 50)
        print("FAILURE: ML optimizer test failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())