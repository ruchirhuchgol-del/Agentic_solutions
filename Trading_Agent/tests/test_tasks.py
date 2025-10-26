"""
Unit tests for the tasks
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestMultiModalSignalSynthesis(unittest.TestCase):
    """Test cases for the Multi-Modal Signal Synthesis task"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.tasks_config = {
            "multi_modal_signal_synthesis": {
                "description": "Analyze market data and generate signals",
                "expected_output": "Trading signals and analysis",
                "agent": "market_intelligence_analyst"
            }
        }
    
    def test_task_creation(self):
        """Test that the task can be created"""
        try:
            from autonomous_trading_crew.tasks.multi_modal_signal_synthesis import create_multi_modal_signal_synthesis
            # Mock the Task class to avoid dependency issues
            with patch('autonomous_trading_crew.tasks.multi_modal_signal_synthesis.Task') as mock_task:
                mock_task.return_value = MagicMock()
                task = create_multi_modal_signal_synthesis(self.tasks_config)
                self.assertIsNotNone(task)
        except ImportError:
            self.skipTest("Multi-Modal Signal Synthesis module not available")

class TestRiskAssessmentGuardrailCheck(unittest.TestCase):
    """Test cases for the Risk Assessment Guardrail Check task"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.tasks_config = {
            "risk_assessment_guardrail_check": {
                "description": "Assess trading risks",
                "expected_output": "Risk assessment report",
                "agent": "risk_management_officer"
            }
        }
    
    def test_task_creation(self):
        """Test that the task can be created"""
        try:
            from autonomous_trading_crew.tasks.risk_assessment_guardrail_check import create_risk_assessment_guardrail_check
            # Mock the Task class to avoid dependency issues
            with patch('autonomous_trading_crew.tasks.risk_assessment_guardrail_check.Task') as mock_task:
                mock_task.return_value = MagicMock()
                task = create_risk_assessment_guardrail_check(self.tasks_config)
                self.assertIsNotNone(task)
        except ImportError:
            self.skipTest("Risk Assessment Guardrail Check module not available")

class TestTaxOptimizedExecutionPlan(unittest.TestCase):
    """Test cases for the Tax Optimized Execution Plan task"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.tasks_config = {
            "tax_optimized_execution_plan": {
                "description": "Create tax-optimized execution plans",
                "expected_output": "Execution plan",
                "agent": "trade_execution_specialist"
            }
        }
    
    def test_task_creation(self):
        """Test that the task can be created"""
        try:
            from autonomous_trading_crew.tasks.tax_optimized_execution_plan import create_tax_optimized_execution_plan
            # Mock the Task class to avoid dependency issues
            with patch('autonomous_trading_crew.tasks.tax_optimized_execution_plan.Task') as mock_task:
                mock_task.return_value = MagicMock()
                task = create_tax_optimized_execution_plan(self.tasks_config)
                self.assertIsNotNone(task)
        except ImportError:
            self.skipTest("Tax Optimized Execution Plan module not available")

class TestDecisionExplanationReport(unittest.TestCase):
    """Test cases for the Decision Explanation Report task"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.tasks_config = {
            "decision_explanation_report": {
                "description": "Generate explanation report",
                "expected_output": "Explanation report",
                "agent": "explainability_reporter"
            }
        }
    
    def test_task_creation(self):
        """Test that the task can be created"""
        try:
            from autonomous_trading_crew.tasks.decision_explanation_report import create_decision_explanation_report
            # Mock the Task class to avoid dependency issues
            with patch('autonomous_trading_crew.tasks.decision_explanation_report.Task') as mock_task:
                mock_task.return_value = MagicMock()
                task = create_decision_explanation_report(self.tasks_config)
                self.assertIsNotNone(task)
        except ImportError:
            self.skipTest("Decision Explanation Report module not available")

if __name__ == '__main__':
    unittest.main()