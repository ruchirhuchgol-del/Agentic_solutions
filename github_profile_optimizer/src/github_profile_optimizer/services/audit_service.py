"""
Profile analysis engine.

Provides comprehensive analysis capabilities for GitHub profiles and repositories.
"""

from typing import Dict, Any, List
from ..utils.logger import get_logger


class AuditService:
    """
    Service for auditing and analyzing GitHub profiles.
    
    This service provides detailed analysis of GitHub profiles and repositories
    to identify strengths, weaknesses, and opportunities for improvement.
    """
    
    def __init__(self):
        """Initialize the audit service."""
        self.logger = get_logger(self.__class__.__name__)
    
    def analyze_profile_completeness(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the completeness of a GitHub profile.
        
        Args:
            profile: GitHub profile data
            
        Returns:
            Completeness analysis results
        """
        completeness_score = 0
        total_checks = 0
        missing_fields = []
        
        # Check profile picture
        total_checks += 1
        if profile.get("avatar_url"):
            completeness_score += 1
        else:
            missing_fields.append("profile picture")
            
        # Check bio
        total_checks += 1
        if profile.get("bio"):
            completeness_score += 1
        else:
            missing_fields.append("bio")
            
        # Check location
        total_checks += 1
        if profile.get("location"):
            completeness_score += 1
        else:
            missing_fields.append("location")
            
        # Check blog/website
        total_checks += 1
        if profile.get("blog"):
            completeness_score += 1
        else:
            missing_fields.append("website")
            
        # Check email (public)
        total_checks += 1
        if profile.get("email"):
            completeness_score += 1
        else:
            missing_fields.append("public email")
            
        # Check company
        total_checks += 1
        if profile.get("company"):
            completeness_score += 1
        else:
            missing_fields.append("company")
            
        completeness_percentage = (completeness_score / total_checks) * 100 if total_checks > 0 else 0
        
        return {
            "completeness_score": completeness_score,
            "total_checks": total_checks,
            "completeness_percentage": completeness_percentage,
            "missing_fields": missing_fields
        }
    
    def analyze_repository_quality(self, repositories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze the quality of user repositories.
        
        Args:
            repositories: List of repository data
            
        Returns:
            Repository quality analysis
        """
        if not repositories:
            return {
                "repository_count": 0,
                "total_stars": 0,
                "average_stars": 0,
                "well_starred_count": 0,
                "well_described_count": 0
            }
            
        total_stars = sum(repo.get("stars", 0) for repo in repositories)
        average_stars = total_stars / len(repositories)
        
        # Count well-starred repositories (more than 5 stars)
        well_starred_count = sum(1 for repo in repositories if repo.get("stars", 0) > 5)
        
        # Count repositories with descriptions
        well_described_count = sum(1 for repo in repositories if repo.get("description"))
        
        return {
            "repository_count": len(repositories),
            "total_stars": total_stars,
            "average_stars": average_stars,
            "well_starred_count": well_starred_count,
            "well_described_count": well_described_count
        }
    
    def generate_audit_report(self, profile: Dict[str, Any], repositories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a complete audit report.
        
        Args:
            profile: GitHub profile data
            repositories: List of repository data
            
        Returns:
            Complete audit report
        """
        profile_analysis = self.analyze_profile_completeness(profile)
        repo_analysis = self.analyze_repository_quality(repositories)
        
        overall_score = (
            profile_analysis["completeness_percentage"] * 0.6 +
            (repo_analysis["well_described_count"] / max(repo_analysis["repository_count"], 1) * 100) * 0.4
        )
        
        return {
            "profile_analysis": profile_analysis,
            "repository_analysis": repo_analysis,
            "overall_score": overall_score,
            "recommendations": self._generate_recommendations(profile_analysis, repo_analysis)
        }
    
    def _generate_recommendations(self, profile_analysis: Dict[str, Any], repo_analysis: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations based on analysis.
        
        Args:
            profile_analysis: Profile completeness analysis
            repo_analysis: Repository quality analysis
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Profile recommendations
        if profile_analysis["missing_fields"]:
            recommendations.append(
                f"Complete your profile by adding: {', '.join(profile_analysis['missing_fields'])}"
            )
            
        # Repository recommendations
        if repo_analysis["repository_count"] > 0:
            if repo_analysis["well_described_count"] < repo_analysis["repository_count"]:
                recommendations.append(
                    f"Add descriptions to {repo_analysis['repository_count'] - repo_analysis['well_described_count']} repositories"
                )
                
            if repo_analysis["well_starred_count"] == 0:
                recommendations.append("Work on improving repository visibility to gain stars")
                
        return recommendations