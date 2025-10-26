"""
Security Policy Decision Engine Agent for the DevSecOps Deployment Gatekeeper.
"""
from typing import Dict, Any, List, Optional
from crewai import Agent
from ..models.security import SecurityReport, SecurityDecision, SeverityLevel
from ..config.settings import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)

class SecurityPolicyDecisionEngine(Agent):
    """Enhanced security policy decision engine with configurable policies and ML support."""
    
    def __init__(self, **kwargs):
        super().__init__(
            role="Security Policy Decision Engine",
            goal="Evaluate security scan results against organizational policies and make deployment decisions",
            backstory=(
                "You are a senior security architect with expertise in threat modeling, "
                "compliance frameworks, and secure development practices. You analyze "
                "security reports to make data-driven decisions about deployment readiness."
            ),
            allow_delegation=False,
            **kwargs
        )
        
        # Store security policies as instance variables
        self._critical_threshold = settings.critical_vulnerability_threshold
        self._major_threshold = settings.major_vulnerability_threshold
        self._allow_override = settings.allow_manual_override
        
        # ML model for false positive detection (placeholder)
        self._false_positive_model = None
    
    @property
    def critical_threshold(self):
        return self._critical_threshold
    
    @property
    def major_threshold(self):
        return self._major_threshold
    
    @property
    def allow_override(self):
        return self._allow_override
    
    @property
    def false_positive_model(self):
        return self._false_positive_model
    
    @false_positive_model.setter
    def false_positive_model(self, value):
        self._false_positive_model = value
    
    def evaluate_security_report(self, report: SecurityReport) -> SecurityDecision:
        """Evaluate a security report against organizational policies."""
        try:
            if not isinstance(report, SecurityReport):
                raise TypeError("Expected SecurityReport instance")
            
            logger.info(f"Evaluating security report for {report.project_key}/{report.branch}")
            
            policy_violations = []
            recommendations = []
            
            # Check critical vulnerabilities
            if report.critical_count > self.critical_threshold:
                policy_violations.append(
                    f"Critical vulnerability threshold exceeded: {report.critical_count} > {self.critical_threshold}"
                )
                recommendations.append(
                    "All critical vulnerabilities must be resolved before deployment"
                )
            
            # Check major vulnerabilities
            if report.major_count > self.major_threshold:
                policy_violations.append(
                    f"Major vulnerability threshold exceeded: {report.major_count} > {self.major_threshold}"
                )
                recommendations.append(
                    f"Reduce major vulnerabilities to {self.major_threshold} or below"
                )
            
            # Check for specific high-risk CWEs
            high_risk_cwes = [79, 89, 90, 200, 352]  # XSS, SQLi, etc.
            critical_high_risk = [
                issue for issue in report.issues 
                if issue.severity == SeverityLevel.CRITICAL and issue.cwe in high_risk_cwes
            ]
            
            if critical_high_risk:
                policy_violations.append(
                    f"Found {len(critical_high_risk)} critical high-risk CWEs"
                )
                recommendations.append(
                    "High-risk CWEs require immediate remediation"
                )
            
            # Check security score
            if hasattr(report, 'security_score') and report.security_score < 70.0:
                policy_violations.append(
                    f"Security score below threshold: {report.security_score} < 70"
                )
                recommendations.append(
                    "Improve security score to 70 or higher"
                )
            
            # Make decision
            if not policy_violations:
                decision = "ALLOW"
                reason = "No policy violations detected"
            else:
                decision = "BLOCK"
                reason = "; ".join(policy_violations)
            
            # Generate additional recommendations
            if report.security_hotspots > 10:
                recommendations.append(
                    "Review and address security hotspots to improve code quality"
                )
            
            if report.major_count > 0:
                recommendations.append(
                    "Prioritize fixing major vulnerabilities to reduce security debt"
                )
            
            return SecurityDecision(
                decision=decision,
                reason=reason,
                policy_violations=policy_violations,
                recommendations=recommendations,
                override_allowed=self.allow_override,
                decision_timestamp=self._get_current_timestamp()
            )
        except Exception as e:
            error_message = f"Error evaluating security report: {str(e)}"
            logger.error(error_message)
            # Provide a safe default decision in case of errors
            return SecurityDecision(
                decision="BLOCK",
                reason=f"Error evaluating security report: {str(e)}",
                policy_violations=[f"System error: {str(e)}"],
                recommendations=["Investigate system error and retry security evaluation"],
                override_allowed=False,
                decision_timestamp=self._get_current_timestamp()
            )
    
    def apply_ml_enhancement(self, report: SecurityReport) -> SecurityReport:
        """Apply machine learning enhancements to the security report."""
        try:
            # This is a placeholder for ML integration
            # In a real implementation, this would:
            # 1. Use a trained model to predict false positives
            # 2. Adjust severity scores based on historical data
            # 3. Identify patterns in vulnerabilities
            
            logger.debug("Applying ML enhancements to security report")
            
            # Placeholder: Adjust critical count based on false positive prediction
            if self.false_positive_model:
                # This would be replaced with actual ML model inference
                pass
            
            return report
        except Exception as e:
            error_message = f"Error applying ML enhancement: {str(e)}"
            logger.error(error_message)
            # Return the original report if ML enhancement fails
            return report
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"