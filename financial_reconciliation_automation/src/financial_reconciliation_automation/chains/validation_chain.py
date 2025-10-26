"""
Data validation chains for the financial reconciliation automation system.
"""

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def create_validation_chain(llm):
    """
    Create a chain for validating financial data.
    
    Args:
        llm: Language model to use for validation
        
    Returns:
        LLMChain: Validation chain
    """
    validation_template = """
    You are a financial data validation expert. Your task is to review financial data and identify any inconsistencies or errors.
    
    Please analyze the following financial data and provide a validation report:
    
    Data to validate:
    {data}
    
    Data type: {data_type}
    
    Your validation report should include:
    1. Overall validation status (Pass/Fail)
    2. List of any errors or inconsistencies found
    3. Recommendations for correcting issues
    4. Summary of data quality assessment
    
    Validation Report:
    """
    
    validation_prompt = PromptTemplate(
        input_variables=["data", "data_type"],
        template=validation_template
    )
    
    return LLMChain(llm=llm, prompt=validation_prompt)


def run_validation_chain(chain, data, data_type):
    """
    Run the validation chain on provided data.
    
    Args:
        chain: Validation chain to run
        data (str): Data to validate
        data_type (str): Type of data being validated
        
    Returns:
        str: Validation results
    """
    return chain.run(data=data, data_type=data_type)