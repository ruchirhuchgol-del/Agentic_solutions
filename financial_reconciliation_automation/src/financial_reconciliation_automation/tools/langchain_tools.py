"""
LangChain-integrated tools for enhanced AI capabilities using real LLM reasoning.
"""

from typing import Type
from pydantic import BaseModel, Field
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


# --------------------------- INPUT SCHEMAS ---------------------------

class DiscrepancyAnalysisInput(BaseModel):
    """Input for discrepancy analysis."""
    unmatched_items: str = Field(..., description="List of unmatched transactions or invoices")
    context: str = Field(..., description="Additional context about the financial period")


class TransactionCategorizationInput(BaseModel):
    """Input for transaction categorization."""
    transactions: str = Field(..., description="List of transactions to categorize")
    categories: str = Field(..., description="Available categories for classification")


# --------------------------- TOOL 1: DISCREPANCY ANALYZER ---------------------------

class DiscrepancyAnalysisTool:
    """Tool for analyzing financial discrepancies using an LLM."""
    
    def __init__(self):
        self.name = "discrepancy_analyzer"
        self.description = "Analyzes financial discrepancies and provides insights."

    def _run(self, unmatched_items: str, context: str) -> str:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

        prompt = ChatPromptTemplate.from_template("""
        You are a financial analyst AI. Analyze the following unmatched financial items
        and provide potential reasons and recommendations.

        Unmatched Items:
        {unmatched_items}

        Context:
        {context}

        Provide your response with the following structure:
        1. Potential Reasons
        2. Recommendations
        """)

        chain = prompt | llm
        response = chain.invoke({
            "unmatched_items": unmatched_items,
            "context": context
        })

        return response.content


# --------------------------- TOOL 2: TRANSACTION CATEGORIZER ---------------------------

class TransactionCategorizationTool:
    """Tool for categorizing financial transactions using an LLM."""
    
    def __init__(self):
        self.name = "transaction_categorizer"
        self.description = "Categorizes financial transactions using AI."

    def _run(self, transactions: str, categories: str) -> str:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

        prompt = ChatPromptTemplate.from_template("""
        You are a financial data assistant. Categorize the following transactions
        into one of the provided categories. If unsure, assign the most relevant one.

        Transactions:
        {transactions}

        Categories:
        {categories}

        Return the result in a concise, human-readable format such as:

        Category: X
        - Transaction 1
        - Transaction 2

        Category: Y
        - Transaction 3
        """)

        chain = prompt | llm
        response = chain.invoke({
            "transactions": transactions,
            "categories": categories
        })

        return response.content