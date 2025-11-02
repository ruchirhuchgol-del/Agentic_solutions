

import logging
import os
from typing import Dict, Any, List

from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)

# Define the base directory for schema files
SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "..", "config", "schemas")

def validate_json_schema(data: Dict[str, Any], schema_name: str) -> bool:
    """
    Validates a data dictionary against a JSON schema file.

    Args:
        data (Dict[str, Any]): The data to validate.
        schema_name (str): The filename of the schema (e.g., "final_output.json").

    Returns:
        bool: True if validation is successful, False otherwise.
    """
    schema_path = os.path.join(SCHEMA_DIR, schema_name)
    if not os.path.exists(schema_path):
        logger.error(f"Schema file not found: {schema_path}")
        return False

    try:
        with open(schema_path, 'r') as f:
            schema = f.read()
        # Assuming schema is stored as a JSON string. If it's a dict, adjust accordingly.
        import json
        schema_dict = json.loads(schema)
        
        validate(instance=data, schema=schema_dict)
        logger.info(f"Validation successful against schema: {schema_name}")
        return True
    except ValidationError as e:
        logger.error(f"JSON validation failed against schema '{schema_name}': {e.message}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred during validation: {e}")
        return False

def validate_extracted_context(context: Dict[str, Any]) -> List[str]:
    """
    Validates the output of the context extraction task.

    Checks for required keys and basic data type correctness.

    Args:
        context (Dict[str, Any]): The context dictionary to validate.

    Returns:
        List[str]: A list of validation error messages. Empty if valid.
    """
    errors = []
    required_keys = ["groups", "metric", "metric_type", "group_relationship", "number_of_groups"]
    
    for key in required_keys:
        if key not in context:
            errors.append(f"Missing required key: '{key}'")
    
    if "number_of_groups" in context and not isinstance(context["number_of_groups"], int):
        errors.append(f"'number_of_groups' must be an integer, got {type(context['number_of_groups']).__name__}")
        
    if "metric_type" in context:
        valid_types = ["continuous", "categorical", "binary"]
        if context["metric_type"] not in valid_types:
            errors.append(f"'metric_type' must be one of {valid_types}, got '{context['metric_type']}'")
            
    if errors:
        logger.warning(f"Context validation failed: {errors}")
    else:
        logger.info("Context validation successful.")
        
    return errors

def validate_business_problem_input(problem: str) -> List[str]:
    """
    Validates the initial business problem input from the user.

    Args:
        problem (str): The user's input string.

    Returns:
        List[str]: A list of validation error messages. Empty if valid.
    """
    errors = []
    if not isinstance(problem, str):
        errors.append("Input must be a string.")
    elif not problem.strip():
        errors.append("Input cannot be empty.")
    elif len(problem.strip()) < 10:
        errors.append("Input is too short. Please provide more detail.")
        
    if errors:
        logger.warning(f"Business problem validation failed: {errors}")
    else:
        logger.info("Business problem validation successful.")
        
    return errors

# Example usage
if __name__ == "__main__":
    # Test context validation
    good_context = {"groups": ["A", "B"], "metric": "revenue", "metric_type": "continuous", "group_relationship": "independent", "number_of_groups": 2}
    bad_context = {"groups": ["A"], "metric": "revenue", "metric_type": "text", "group_relationship": "independent"}
    
    print(validate_extracted_context(good_context)) # Should print []
    print(validate_extracted_context(bad_context))  # Should print errors

    # Test input validation
    print(validate_business_problem_input("This is a valid problem description.")) # Should print []
    print(validate_business_problem_input("short")) # Should print errors