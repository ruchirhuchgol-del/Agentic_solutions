"""Unit tests for the base tool."""
import pytest
from src.github_profile_optimizer.tools.base_tool import BaseTool
from pydantic import BaseModel


class TestParams(BaseModel):
    """Test parameters model."""
    value: str


class TestTool(BaseTool):
    """Test tool implementation."""
    
    def execute(self, params: BaseModel) -> dict:
        """Execute the test tool."""
        return {"result": f"Executed with {params.value}"}


def test_base_tool_initialization():
    """Test base tool initialization."""
    tool = TestTool(dry_run=True)
    assert tool.dry_run is True
    assert tool.name == "TestTool"
    assert "Test tool implementation" in tool.description


def test_base_tool_safety_check():
    """Test base tool safety check."""
    tool = TestTool()
    params = TestParams(value="test")
    assert tool.safety_check(params) is True


def test_base_tool_execute():
    """Test base tool execute method."""
    tool = TestTool()
    params = TestParams(value="test")
    result = tool.execute(params)
    assert result["result"] == "Executed with test"