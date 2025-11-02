

import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

def format_final_output_as_json(
    business_problem: str,
    context: Dict[str, Any],
    hypotheses: Dict[str, Any],
    test_recommendation: Dict[str, Any],
    validation_report: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Assembles the raw outputs from the crew into a structured final JSON object.

    Args:
        business_problem (str): The original user input.
        context (Dict[str, Any]): The extracted context from the context extractor.
        hypotheses (Dict[str, Any]): The generated hypotheses from the hypothesis generator.
        test_recommendation (Dict[str, Any]): The test recommendation from the test recommender.
        validation_report (Dict[str, Any]): The report from the statistical validator.

    Returns:
        Dict[str, Any]: A structured dictionary representing the final output.
    """
    logger.info("Formatting final output as JSON.")
    
    final_output = {
        "business_problem": business_problem,
        "timestamp": datetime.utcnow().isoformat(),
        "summary": f"Analysis for comparing {context.get('number_of_groups')} groups on the metric '{context.get('metric')}'.",
        "extracted_context": context,
        "hypotheses": hypotheses,
        "test_recommendation": test_recommendation,
        "validation": validation_report,
        "confidence_metrics": {
            "extraction_confidence": context.get("confidence_level"),
            "validation_score": validation_report.get("confidence_score"),
            "overall_status": validation_report.get("status")
        },
        "next_steps": "Proceed with data collection and run the recommended statistical test."
    }
    return final_output

def generate_markdown_summary(final_json_output: Dict[str, Any]) -> str:
    """
    Generates a clean, human-readable Markdown summary from the structured JSON output.

    Args:
        final_json_output (Dict[str, Any]): The final structured output from the crew.

    Returns:
        str: A formatted Markdown string.
    """
    logger.info("Generating Markdown summary.")
    
    md = []
    md.append("# Hypothesis Generation Analysis Report")
    md.append(f"**Generated on:** {final_json_output.get('timestamp')}")
    md.append("")
    
    md.append("## 1. Business Problem")
    md.append(final_json_output.get('business_problem'))
    md.append("")
    
    md.append("## 2. Summary")
    md.append(final_json_output.get('summary'))
    md.append("")
    
    md.append("## 3. Extracted Context")
    context = final_json_output.get('extracted_context', {})
    md.append(f"- **Groups:** {', '.join(context.get('groups', []))}")
    md.append(f"- **Metric:** {context.get('metric')}")
    md.append(f"- **Metric Type:** {context.get('metric_type')}")
    md.append(f"- **Group Relationship:** {context.get('group_relationship')}")
    md.append(f"- **Extraction Confidence:** {context.get('confidence_level')}")
    md.append("")
    
    md.append("## 4. Statistical Hypotheses")
    hypotheses = final_json_output.get('hypotheses', {})
    md.append(f"### Null Hypothesis (H₀)")
    md.append(f"- **Notation:** `{hypotheses.get('null', {}).get('notation')}`")
    md.append(f"- **Plain English:** {hypotheses.get('null', {}).get('plain_english')}")
    md.append("")
    
    md.append("### Alternative Hypotheses (H₁)")
    for h_type, h_data in hypotheses.items():
        if h_type.startswith('h1_') or h_type == 'alternative':
            md.append(f"#### {h_data.get('type', 'Alternative')}")
            md.append(f"- **Notation:** `{h_data.get('notation')}`")
            md.append(f"- **Plain English:** {h_data.get('plain_english')}")
    md.append("")
    
    md.append("## 5. Recommended Statistical Test")
    test_rec = final_json_output.get('test_recommendation', {})
    md.append(f"- **Primary Test:** {test_rec.get('primary_test')}")
    md.append(f"- **Justification:** {test_rec.get('primary_justification')}")
    if test_rec.get('alternative_tests'):
        md.append(f"- **Alternatives:** {', '.join(test_rec.get('alternative_tests'))}")
    md.append("")
    
    md.append("## 6. Validation & Confidence")
    validation = final_json_output.get('validation', {})
    md.append(f"- **Validation Status:** `{validation.get('validation_status')}`")
    if validation.get('identified_issues'):
        md.append("- **Issues Found:**")
        for issue in validation.get('identified_issues'):
            md.append(f"  - {issue}")
    md.append("")
    
    confidence = final_json_output.get('confidence_metrics', {})
    md.append(f"- **Overall Confidence Score:** {confidence.get('validation_score')}/10")
    md.append("")
    
    md.append("## 7. Next Steps")
    md.append(final_json_output.get('next_steps'))
    
    return "\n".join(md)

# Example usage
if __name__ == "__main__":
    mock_json = {
        "business_problem": "Test if new UI is better.",
        "timestamp": "2023-10-27T10:00:00",
        "summary": "Analysis for 2 groups.",
        "extracted_context": {"groups": ["A", "B"], "metric": "revenue", "metric_type": "continuous", "confidence_level": "HIGH"},
        "hypotheses": {"null": {"notation": "H₀: μ_A = μ_B", "plain_english": "No difference."}},
        "test_recommendation": {"primary_test": "t-test", "primary_justification": "Compares two means."},
        "validation": {"validation_status": "APPROVED", "confidence_score": 9},
        "next_steps": "Run the test."
    }
    print(generate_markdown_summary(mock_json))