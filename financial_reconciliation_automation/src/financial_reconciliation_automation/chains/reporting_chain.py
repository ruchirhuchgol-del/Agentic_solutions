"""
Report generation chains for the financial reconciliation automation system.
"""

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def create_reporting_chain(llm):
    """
    Create a chain for generating financial reconciliation reports.
    
    Args:
        llm: Language model to use for report generation
        
    Returns:
        LLMChain: Reporting chain
    """
    reporting_template = """
    You are a financial reporting expert. Your task is to generate a comprehensive reconciliation report based on the provided matching results.
    
    Please create a detailed report with the following sections:
    
    Matching Results:
    {matching_results}
    
    The report should include:
    1. Executive Summary
    2. Key Metrics (match rate, discrepancy count, etc.)
    3. Detailed Analysis of Unmatched Items
    4. Recommendations for Resolution
    5. Next Steps
    
    Format the report in clear, professional language suitable for financial professionals.
    
    Financial Reconciliation Report:
    """
    
    reporting_prompt = PromptTemplate(
        input_variables=["matching_results"],
        template=reporting_template
    )
    
    return LLMChain(llm=llm, prompt=reporting_prompt)


def run_reporting_chain(chain, matching_results):
    """
    Run the reporting chain on provided matching results.
    
    Args:
        chain: Reporting chain to run
        matching_results (str): Matching results data
        
    Returns:
        str: Generated report
    """
    return chain.run(matching_results=matching_results)