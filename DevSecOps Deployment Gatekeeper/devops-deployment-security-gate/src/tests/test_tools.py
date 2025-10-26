"""
Unit tests for tools.
"""
import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from devops_deployment_security_gate.tools.sonarqube_scanner import SonarQubeSecurityScannerTool
from devops_deployment_security_gate.tools.github_tool import GitHubPRTool
from devops_deployment_security_gate.tools.slack_tool import SlackNotificationTool
from devops_deployment_security_gate.tools.base_tool import DevSecOpsBaseTool

class TestDevSecOpsBaseTool(unittest.TestCase):
    """Test cases for DevSecOpsBaseTool."""
    
    def test_base_tool_initialization(self):
        """Test base tool initialization."""
        tool = DevSecOpsBaseTool(name="Test Tool", description="A test tool")
        
        self.assertEqual(tool.name, "Test Tool")
        self.assertEqual(tool.description, "A test tool")
        self.assertIsNotNone(tool.logger)
    
    def test_validate_required_params_success(self):
        """Test successful validation of required parameters."""
        tool = DevSecOpsBaseTool(name="Test Tool", description="A test tool")
        
        # Should not raise exception
        tool._validate_required_params(
            {"param1": "value1", "param2": "value2"},
            ["param1", "param2"]
        )
    
    def test_validate_required_params_missing(self):
        """Test validation failure with missing parameters."""
        tool = DevSecOpsBaseTool(name="Test Tool", description="A test tool")
        
        with self.assertRaises(ValueError) as context:
            tool._validate_required_params(
                {"param1": "value1"},
                ["param1", "param2"]
            )
        self.assertTrue("Missing required parameters" in str(context.exception))
    
    def test_validate_required_params_empty_value(self):
        """Test validation failure with empty parameter values."""
        tool = DevSecOpsBaseTool(name="Test Tool", description="A test tool")
        
        with self.assertRaises(ValueError) as context:
            tool._validate_required_params(
                {"param1": "value1", "param2": ""},
                ["param1", "param2"]
            )
        self.assertTrue("Missing required parameters" in str(context.exception))

class TestSonarQubeSecurityScannerTool(unittest.TestCase):
    """Test cases for SonarQubeSecurityScannerTool."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tool = SonarQubeSecurityScannerTool()
    
    def test_tool_attributes(self):
        """Test tool attributes."""
        self.assertEqual(self.tool.name, "SonarQube Security Scanner")
        self.assertEqual(self.tool.description, "Tool for executing security scans using SonarQube")
    
    @patch('devops_deployment_security_gate.tools.sonarqube_scanner.get_sonarqube_integration')
    def test_run_success(self, mock_get_integration):
        """Test successful execution of the tool."""
        # Mock the SonarQube integration
        mock_sonarqube = MagicMock()
        mock_sonarqube.trigger_analysis.return_value = "task123"
        mock_sonarqube.wait_for_analysis_completion.return_value = None
        mock_sonarqube.get_security_report.return_value = MagicMock()
        mock_sonarqube.get_security_report.return_value.dict.return_value = {"test": "data"}
        mock_get_integration.return_value = mock_sonarqube
        
        # Test the tool
        result = self.tool._run(
            branch_name="main",
            project_key="test-project",
            sonarqube_url="https://sonarqube.example.com"
        )
        
        self.assertEqual(result, {"test": "data"})
        mock_get_integration.assert_called_once_with("https://sonarqube.example.com")
        mock_sonarqube.trigger_analysis.assert_called_once_with("test-project", "main")
        mock_sonarqube.wait_for_analysis_completion.assert_called_once_with("task123")
        mock_sonarqube.get_security_report.assert_called_once_with("test-project", "main")
    
    def test_run_validation(self):
        """Test validation in tool execution."""
        # Test with missing branch name
        with self.assertRaises(ValueError) as context:
            self.tool._run(
                branch_name="",
                project_key="test-project",
                sonarqube_url="https://sonarqube.example.com"
            )
        self.assertTrue("Missing required parameters" in str(context.exception))

class TestGitHubPRTool(unittest.TestCase):
    """Test cases for GitHubPRTool."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tool = GitHubPRTool()
    
    def test_tool_attributes(self):
        """Test tool attributes."""
        self.assertEqual(self.tool.name, "GitHub PR Tool")
        self.assertEqual(self.tool.description, "Tool for extracting metadata from GitHub Pull Requests")
    
    @patch('devops_deployment_security_gate.tools.github_tool.get_github_integration')
    def test_run_success(self, mock_get_integration):
        """Test successful execution of the tool."""
        # Mock the GitHub integration
        mock_github = MagicMock()
        mock_github.get_pull_request.return_value = {
            "head": {"ref": "feature-branch", "sha": "abc123"},
            "user": {"login": "test-user"},
            "title": "Test PR",
            "body": "Test description",
            "state": "open"
        }
        mock_github.get_pull_request_files.return_value = [
            {"filename": "src/main.py"},
            {"filename": "src/utils.py"}
        ]
        mock_get_integration.return_value = mock_github
        
        # Test the tool
        result = self.tool._run(
            pr_number="123",
            repository="test-org/test-repo"
        )
        
        self.assertEqual(result["pr_number"], "123")
        self.assertEqual(result["repository"], "test-org/test-repo")
        self.assertEqual(result["branch_name"], "feature-branch")
        self.assertEqual(result["commit_sha"], "abc123")
        self.assertEqual(result["author"], "test-user")
        self.assertEqual(result["title"], "Test PR")
        self.assertEqual(result["description"], "Test description")
        self.assertEqual(result["status"], "open")
        self.assertEqual(len(result["changed_files"]), 2)
        
        mock_get_integration.assert_called_once()
        mock_github.get_pull_request.assert_called_once_with("test-org/test-repo", "123")
        mock_github.get_pull_request_files.assert_called_once_with("test-org/test-repo", "123")
    
    def test_run_validation(self):
        """Test validation in tool execution."""
        # Test with missing PR number
        with self.assertRaises(ValueError) as context:
            self.tool._run(
                pr_number="",
                repository="test-org/test-repo"
            )
        self.assertTrue("Missing required parameters" in str(context.exception))

class TestSlackNotificationTool(unittest.TestCase):
    """Test cases for SlackNotificationTool."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tool = SlackNotificationTool()
    
    def test_tool_attributes(self):
        """Test tool attributes."""
        self.assertEqual(self.tool.name, "Slack Notification Tool")
        self.assertEqual(self.tool.description, "Tool for sending security alerts to Slack channels")
    
    @patch('devops_deployment_security_gate.tools.slack_tool.get_slack_integration')
    def test_run_success(self, mock_get_integration):
        """Test successful execution of the tool."""
        # Mock the Slack integration
        mock_slack = MagicMock()
        mock_slack.send_message.return_value = {
            "ok": True,
            "ts": "1234567890.001200"
        }
        mock_get_integration.return_value = mock_slack
        
        # Test the tool
        result = self.tool._run(
            message="Test message",
            channel="#test-channel"
        )
        
        self.assertEqual(result["channel"], "#test-channel")
        self.assertEqual(result["message"], "Test message")
        self.assertEqual(result["status"], "sent")
        self.assertEqual(result["recipient_count"], 1)
        
        mock_get_integration.assert_called_once()
        mock_slack.send_message.assert_called_once_with("#test-channel", "Test message")
    
    def test_run_validation(self):
        """Test validation in tool execution."""
        # Test with missing message
        with self.assertRaises(ValueError) as context:
            self.tool._run(
                message="",
                channel="#test-channel"
            )
        self.assertTrue("Missing required parameters" in str(context.exception))

if __name__ == '__main__':
    unittest.main()