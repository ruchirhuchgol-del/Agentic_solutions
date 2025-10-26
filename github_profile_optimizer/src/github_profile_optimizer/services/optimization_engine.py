"""
Recommendation generator.

Provides intelligent recommendation generation for GitHub profile optimization.
"""

from typing import Dict, Any, List
from ..utils.logger import get_logger


class OptimizationEngine:
    """
    Engine for generating profile optimization recommendations.
    
    This engine analyzes audit reports and generates targeted recommendations
    for improving GitHub profiles based on best practices and recruiter preferences.
    """
    
    def __init__(self):
        """Initialize the optimization engine."""
        self.logger = get_logger(self.__class__.__name__)
    
    def generate_profile_recommendations(self, audit_report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate detailed recommendations for profile improvement.
        
        Args:
            audit_report: Audit report containing profile and repository analysis
            
        Returns:
            List of recommendation objects
        """
        recommendations = []
        
        profile_analysis = audit_report.get("profile_analysis", {})
        repo_analysis = audit_report.get("repository_analysis", {})
        
        # Profile completeness recommendations
        missing_fields = profile_analysis.get("missing_fields", [])
        if "bio" in missing_fields:
            recommendations.append({
                "type": "profile",
                "priority": "high",
                "title": "Add a professional bio",
                "description": "Write a compelling bio that highlights your skills, experience, and interests.",
                "impact": "High"
            })
            
        if "profile picture" in missing_fields:
            recommendations.append({
                "type": "profile",
                "priority": "medium",
                "title": "Add a profile picture",
                "description": "Upload a professional-looking profile picture to make your profile more engaging.",
                "impact": "Medium"
            })
            
        if "location" in missing_fields:
            recommendations.append({
                "type": "profile",
                "priority": "low",
                "title": "Add your location",
                "description": "Include your location to help others in your area connect with you.",
                "impact": "Low"
            })
            
        # Repository recommendations
        if repo_analysis.get("repository_count", 0) > 0:
            if repo_analysis.get("well_described_count", 0) < repo_analysis.get("repository_count", 0):
                recommendations.append({
                    "type": "repositories",
                    "priority": "high",
                    "title": "Improve repository descriptions",
                    "description": "Add clear, descriptive README files to your repositories to explain what they do.",
                    "impact": "High"
                })
                
            if repo_analysis.get("well_starred_count", 0) == 0:
                recommendations.append({
                    "type": "repositories",
                    "priority": "medium",
                    "title": "Increase repository visibility",
                    "description": "Consider sharing your projects on social media or developer communities to gain visibility.",
                    "impact": "Medium"
                })
                
        return recommendations
    
    def prioritize_recommendations(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Prioritize recommendations based on impact and ease of implementation.
        
        Args:
            recommendations: List of recommendation objects
            
        Returns:
            Prioritized list of recommendations
        """
        # Priority mapping
        priority_order = {"high": 3, "medium": 2, "low": 1}
        
        # Sort by priority (high to low)
        return sorted(
            recommendations, 
            key=lambda x: priority_order.get(x.get("priority", "low"), 0), 
            reverse=True
        )
    
    def generate_action_plan(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate an actionable plan from recommendations.
        
        Args:
            recommendations: List of prioritized recommendations
            
        Returns:
            Action plan with timeline and steps
        """
        prioritized = self.prioritize_recommendations(recommendations)
        
        return {
            "immediate_actions": [r for r in prioritized if r["priority"] == "high"],
            "short_term_actions": [r for r in prioritized if r["priority"] == "medium"],
            "long_term_actions": [r for r in prioritized if r["priority"] == "low"],
            "estimated_timeline": self._estimate_timeline(prioritized)
        }
    
    def _estimate_timeline(self, recommendations: List[Dict[str, Any]]) -> str:
        """
        Estimate timeline for implementing recommendations.
        
        Args:
            recommendations: List of recommendations
            
        Returns:
            Estimated timeline as string
        """
        high_priority_count = len([r for r in recommendations if r["priority"] == "high"])
        medium_priority_count = len([r for r in recommendations if r["priority"] == "medium"])
        
        if high_priority_count > 0:
            return "1-2 weeks for immediate actions, 1-2 months for all improvements"
        elif medium_priority_count > 0:
            return "2-4 weeks for all improvements"
        else:
            return "1-2 weeks for all improvements"