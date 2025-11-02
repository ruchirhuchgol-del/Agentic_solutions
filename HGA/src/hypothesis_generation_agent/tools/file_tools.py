

import os
import logging
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from crewai_tools import FileReadTool as CrewAIFileReadTool

logger = logging.getLogger(__name__)

class CustomFileReadToolInput(BaseModel):
    """Input schema for the CustomFileReadTool."""
    file_path: str = Field(..., description="The absolute or relative path to the file to be read.")

class CustomFileReadTool(BaseTool):
    name: str = "Read a File"
    description: str = (
        "Reads the entire content of a specified file. "
        "Use this to access knowledge base documents, configuration files, "
        "or any other text-based file needed for context."
    )
    args_schema: Type[BaseModel] = CustomFileReadToolInput

    def _run(self, file_path: str) -> str:
        """
        Executes the tool to read the content of a file.

        Args:
            file_path (str): The path to the file.

        Returns:
            str: The content of the file or an error message.
        """
        try:
            # Use CrewAI's built-in tool for robustness
            # We wrap it to add logging and custom error messages
            crew_tool = CrewAIFileReadTool()
            content = crew_tool.run(file_path)
            logger.info(f"Successfully read file: {file_path}")
            return content
        except FileNotFoundError:
            error_msg = f"Error: The file at '{file_path}' was not found."
            logger.error(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"An unexpected error occurred while reading '{file_path}': {e}"
            logger.error(error_msg)
            return error_msg