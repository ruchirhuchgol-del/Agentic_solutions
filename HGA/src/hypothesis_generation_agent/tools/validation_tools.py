

import logging
from typing import Type, Dict, Any, List
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class ValidateHypothesisTestAlignmentToolInput(BaseModel):
    """Input schema for the ValidateHypothesisTestAlignmentTool."""
    hypotheses: Dict[str, Any] = Field(..., description="The complete set of hypotheses (H0 and H1 variants).")
    test_recommendation: Dict[str, Any] = Field(..., description="The primary and alternative statistical test recommendations.")
    context: Dict[str, Any] = Field(..., description="The extracted context, including metric_type and group_relationship.")

class ValidateHypothesisTestAlignmentTool(BaseTool):
    name: str = "Validate Hypothesis-Test Alignment"
    description: str = (
        "Performs programmatic checks to validate the alignment between hypotheses and the recommended statistical test. "
        "Checks for obvious misalignments, such as using a mean-based test for a proportion or a categorical test for continuous data. "
        "This provides a deterministic validation layer to complement the LLM's reasoning."
    )
    args_schema: Type[BaseModel] = ValidateHypothesisTestAlignmentToolInput

    def _run(self, hypotheses: Dict[str, Any], test_recommendation: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Runs the validation checks."""
        validation_report = {
            "status": "PASSED",
            "checks_performed": [],
            "issues_found": []
        }

        metric_type = context.get("metric_type", "").lower()
        primary_test = test_recommendation.get("primary_test", "").lower()
        
        # Check 1: Notation vs. Metric Type
        h0_notation = hypotheses.get("null", {}).get("notation", "")
        if metric_type == "categorical" or metric_type == "binary":
            if "μ" in h0_notation:
                validation_report["status"] = "FAILED"
                validation_report["issues_found"].append("Mean notation (μ) used for a categorical/binary metric. Proportion notation (p) is expected.")
        elif metric_type == "continuous":
            if "p" in h0_notation and "μ" not in h0_notation: # Avoid flagging 'p-value'
                validation_report["status"] = "FAILED"
                validation_report["issues_found"].append("Proportion notation (p) used for a continuous metric. Mean notation (μ) is expected.")
        validation_report["checks_performed"].append("Notation vs. Metric Type")

        # Check 2: Test vs. Data Type
        if "chi-squared" in primary_test and metric_type == "continuous":
            validation_report["status"] = "FAILED"
            validation_report["issues_found"].append("Chi-squared test recommended for a continuous metric. It is typically used for categorical data.")
        if "t-test" in primary_test and metric_type == "categorical":
            validation_report["status"] = "FAILED"
            validation_report["issues_found"].append("T-test recommended for a categorical metric. It is typically used for continuous data.")
        validation_report["checks_performed"].append("Test vs. Data Type")

        # Check 3: Test vs. Group Count
        num_groups = context.get("number_of_groups", 0)
        if "anova" in primary_test and num_groups <= 2:
            validation_report["status"] = "FAILED"
            validation_report["issues_found"].append("ANOVA recommended for 2 or fewer groups. It is typically used for comparing 3 or more groups.")
        if "t-test" in primary_test and num_groups > 2:
            validation_report["status"] = "FAILED"
            validation_report["issues_found"].append("T-test recommended for more than 2 groups. ANOVA or multiple t-tests might be more appropriate.")
        validation_report["checks_performed"].append("Test vs. Group Count")

        logger.info(f"Programmatic validation completed with status: {validation_report['status']}")
        return json.dumps(validation_report, indent=2)