"""
Refactored GitHub agent.

Implements an AI agent specialized for GitHub profile analysis and optimization tasks.
"""

from typing import Dict, Any, List, Optional
import asyncio
import os
from ..agents.base_agent import BaseAgent
from ..tools.base_tool import BaseTool
from ..tools.github_client import GitHubProfileTool
from ..tools.file_operation_tool import FileOperationTool
from ..utils.state_manager import RedisStateManager
from ..services.safety_checker import SafetyChecker
from ..services.audit_service import AuditService
from ..services.optimization_engine import OptimizationEngine
from ..models.github import GitHubParams, Operation
from ..utils.logger import get_logger
from crewai_tools import ScrapeWebsiteTool


class OptimizationResult:
    """
    Result of optimization process.
    
    Contains the results of a profile optimization operation including
    audit data, recommendations, and state information.
    """
    
    def __init__(self, audit: Dict[str, Any], recommendations: List[Dict[str, Any]], state: Any):
        self.audit = audit
        self.recommendations = recommendations
        self.state = state


class GitHubAutomationAgent(BaseAgent):
    """
    Agent for automating GitHub profile optimization tasks.
    
    This agent coordinates various tools and services to analyze and optimize
    GitHub profiles according to best practices and recruiter preferences.
    """
    
    def __init__(self, github_token: Optional[str] = None, dry_run: bool = True):
        """
        Initialize the GitHub automation agent.
        
        Args:
            github_token: GitHub personal access token
            dry_run: Whether to run in dry-run mode
        """
        tools = [
            GitHubProfileTool(dry_run=dry_run),
            FileOperationTool(dry_run=dry_run),
            ScrapeWebsiteTool()
        ]
        
        super().__init__("GitHub Automation Agent", tools)
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.dry_run = dry_run
        self.state_manager = RedisStateManager()
        self.safety_checker = SafetyChecker()
        self.logger = get_logger(self.__class__.__name__)
    
    async def optimize_profile(self, task: Dict[str, Any]) -> OptimizationResult:
        """
        Optimize a GitHub profile.
        
        Args:
            task: Task definition containing parameters
            
        Returns:
            Optimization result
        """
        task_id = task.get("task_id", "default")
        params = task.get("params", {})
        
        # Create state
        state = self.state_manager.create_state(task_id, self.dry_run)
        self.logger.info(f"Created state for task {task_id}")
        
        # 1. Audit current state
        self.logger.info("Running profile audit")
        audit = await self._run_audit(params)
        
        # 2. Generate recommendations
        self.logger.info("Generating recommendations")
        recommendations = OptimizationEngine().generate_profile_recommendations(audit)
        
        # 3. Safety-checked execution
        if not self.dry_run:
            self.logger.info("Applying changes")
            await self._apply_changes(recommendations, state)
        
        return OptimizationResult(
            audit=audit,
            recommendations=recommendations,
            state=state
        )
    
    async def _run_audit(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run profile audit.
        
        Args:
            params: Audit parameters
            
        Returns:
            Audit results
        """
        username = params.get("username")
        if not username:
            raise ValueError("Username is required")
            
        github_params = GitHubParams(
            token=self.github_token,
            handle=username,
            dry_run=self.dry_run
        )
        
        # Run GitHub tool
        tool_result = self.run_tool("GitHubProfileTool", params=github_params)
        
        # Run audit service
        audit_service = AuditService()
        profile = tool_result.get("profile", {})
        repos = tool_result.get("repos", [])
        
        return audit_service.generate_audit_report(profile, repos)
    
    async def _apply_changes(self, recommendations: List[Dict[str, Any]], state: Any) -> None:
        """
        Apply recommended changes.
        
        Args:
            recommendations: List of recommendations to apply
            state: Current optimization state
        """
        # In a real implementation, this would apply the recommendations
        # For now, we'll just log what would be done
        self.logger.info(f"Would apply {len(recommendations)} recommendations")
        
        # Example of how changes would be applied:
        operations = []
        for rec in recommendations:
            # This would create actual file operations based on recommendations
            if rec.get("type") == "profile":
                self.logger.info(f"Would update profile: {rec.get('title')}")
            elif rec.get("type") == "repositories":
                self.logger.info(f"Would update repositories: {rec.get('title')}")
                
        # Perform safety checks
        check_result = self.safety_checker.preflight_check(operations)
        if not check_result.passed:
            self.logger.error(f"Safety checks failed: {check_result.errors}")
            raise ValueError(f"Safety checks failed: {check_result.errors}")
            
        # Update state with safety check results
        self.state_manager.update_safety_check(state.task_id, "preflight", check_result.passed)
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a GitHub automation task.
        
        Args:
            task: Task definition containing action and parameters
            
        Returns:
            Result of the task execution
        """
        action = task.get("action")
        params = task.get("params", {})
        
        if action == "analyze_profile":
            return self._analyze_profile(params)
        elif action == "optimize_profile":
            return self._optimize_profile(params)
        elif action == "update_profile":
            return self._update_profile(params)
        else:
            return {"error": f"Unknown action: {action}"}
    
    def _analyze_profile(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a GitHub profile.
        
        Args:
            params: Parameters including username
            
        Returns:
            Profile analysis results
        """
        username = params.get("username")
        if not username:
            return {"error": "Username is required"}
            
        try:
            # Create GitHub params
            github_params = GitHubParams(
                token=self.github_token,
                handle=username
            )
            
            # Run GitHub tool
            tool_result = self.run_tool("GitHubProfileTool", params=github_params)
            profile = tool_result.get("profile", {})
            repos = tool_result.get("repos", [])
            
            # Run audit service
            audit_service = AuditService()
            audit_report = audit_service.generate_audit_report(profile, repos)
            
            return {
                "profile": profile,
                "repositories": repos,
                "audit": audit_report
            }
        except Exception as e:
            return {"error": f"Failed to analyze profile: {str(e)}"}
    
    def _optimize_profile(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate profile optimization recommendations.
        
        Args:
            params: Parameters for optimization
            
        Returns:
            Optimization recommendations
        """
        try:
            # First analyze the profile
            analysis_result = self._analyze_profile(params)
            if "error" in analysis_result:
                return analysis_result
                
            # Generate recommendations using optimization engine
            optimization_engine = OptimizationEngine()
            recommendations = optimization_engine.generate_profile_recommendations(
                analysis_result.get("audit", {})
            )
            
            return {
                "analysis": analysis_result,
                "recommendations": recommendations
            }
        except Exception as e:
            return {"error": f"Failed to optimize profile: {str(e)}"}
    
    def _update_profile(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update GitHub profile.
        
        Args:
            params: Profile fields to update
            
        Returns:
            Update result
        """
        # Validate updates
        validation_result = self.safety_checker.validate_profile_update(params)
        if not validation_result["valid"]:
            return {"error": "Validation failed", "issues": validation_result["issues"]}
            
        # In a real implementation, this would update the profile
        # For now, we'll just return a success message
        return {"success": True, "message": "Profile update would be applied in live mode"}