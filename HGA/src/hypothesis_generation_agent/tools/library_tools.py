

import json
import os
import uuid
import logging
from datetime import datetime
from typing import Type, Dict, Any, List
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# Define the path for the hypothesis library
LIBRARY_PATH = os.path.join(os.getcwd(), "data", "hypothesis_library")
os.makedirs(LIBRARY_PATH, exist_ok=True)

class StoreHypothesisToolInput(BaseModel):
    """Input schema for the StoreHypothesisTool."""
    hypothesis_record: Dict[str, Any] = Field(..., description="The complete, validated hypothesis record in JSON format.")
    tags: List[str] = Field(..., description="A list of tags for categorizing and searching the hypothesis.")

class StoreHypothesisTool(BaseTool):
    name: str = "Store Hypothesis in Library"
    description: str = (
        "Saves a validated hypothesis formulation to the centralized hypothesis library. "
        "This creates a permanent, searchable record of the analysis for future reuse. "
        "Input should be the final JSON output from the reviewer agent."
    )
    args_schema: Type[BaseModel] = StoreHypothesisToolInput

    def _run(self, hypothesis_record: Dict[str, Any], tags: List[str]) -> str:
        """Stores the hypothesis in a JSON file."""
        try:
            # Create a unique entry
            entry = {
                "unique_id": str(uuid.uuid4()),
                "timestamp": datetime.utcnow().isoformat(),
                "tags": tags,
                "record": hypothesis_record
            }

            # Save to a file named with the unique ID
            file_path = os.path.join(LIBRARY_PATH, f"{entry['unique_id']}.json")
            with open(file_path, 'w') as f:
                json.dump(entry, f, indent=2)

            logger.info(f"Successfully stored hypothesis with ID {entry['unique_id']} to {file_path}")
            return f"Hypothesis successfully stored in the library with ID: {entry['unique_id']}"
        except Exception as e:
            error_msg = f"Failed to store hypothesis: {e}"
            logger.error(error_msg, exc_info=True)
            return error_msg

class SearchHypothesisLibraryToolInput(BaseModel):
    """Input schema for the SearchHypothesisLibraryTool."""
    query: str = Field(..., description="A keyword or phrase to search for in hypothesis tags, summaries, or content.")
    limit: int = Field(default=5, description="The maximum number of results to return.")

class SearchHypothesisLibraryTool(BaseTool):
    name: str = "Search Hypothesis Library"
    description: str = (
        "Searches the centralized hypothesis library for past analyses. "
        "Use this to find similar problems, reuse existing formulations, or check if a hypothesis has been tested before."
    )
    args_schema: Type[BaseModel] = SearchHypothesisLibraryToolInput

    def _run(self, query: str, limit: int) -> str:
        """Searches through stored hypothesis files."""
        try:
            results = []
            query_lower = query.lower()
            files = [f for f in os.listdir(LIBRARY_PATH) if f.endswith('.json')]

            for filename in files:
                file_path = os.path.join(LIBRARY_PATH, filename)
                with open(file_path, 'r') as f:
                    entry = json.load(f)

                # Simple keyword search in tags and summary
                searchable_text = " ".join(entry.get('tags', [])).lower()
                summary = entry.get('record', {}).get('summary', '').lower()
                
                if query_lower in searchable_text or query_lower in summary:
                    results.append({
                        "id": entry.get('unique_id'),
                        "timestamp": entry.get('timestamp'),
                        "tags": entry.get('tags'),
                        "summary": entry.get('record', {}).get('summary'),
                    })
                    if len(results) >= limit:
                        break
            
            if not results:
                return f"No hypotheses found matching the query: '{query}'"

            return json.dumps(results, indent=2)

        except Exception as e:
            error_msg = f"An error occurred while searching the library: {e}"
            logger.error(error_msg, exc_info=True)
            return error_msg