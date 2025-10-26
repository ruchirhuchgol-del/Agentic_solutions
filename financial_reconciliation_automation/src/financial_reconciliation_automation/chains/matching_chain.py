"""
Transaction matching chains for the financial reconciliation automation system.
"""

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def create_matching_chain(llm):
    """
    Create a chain for matching financial transactions.
    
    Args:
        llm: Language model to use for matching
        
    Returns:
        LLMChain: Matching chain
    """
    matching_template = """
    You are a financial reconciliation expert. Your task is to match transactions with invoices based on the provided data.
    
    Please analyze the following transactions and invoices and identify matches:
    
    Transactions:
    {transactions}
    
    Invoices:
    {invoices}
    
    Your matching analysis should include:
    1. List of matched transaction-invoice pairs with confidence scores
    2. List of unmatched transactions with possible reasons
    3. List of unmatched invoices with possible reasons
    4. Summary of matching accuracy
    
    Matching Analysis:
    """
    
    matching_prompt = PromptTemplate(
        input_variables=["transactions", "invoices"],
        template=matching_template
    )
    
    return LLMChain(llm=llm, prompt=matching_prompt)


def run_matching_chain(chain, transactions, invoices):
    """
    Run the matching chain on provided data.
    
    Args:
        chain: Matching chain to run
        transactions (str): Transactions data
        invoices (str): Invoices data
        
    Returns:
        str: Matching results
    """
    return chain.run(transactions=transactions, invoices=invoices)