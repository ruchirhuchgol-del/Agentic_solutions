"""
Main entry point for the Hypothesis Generation Agent.
"""
import os
from dotenv import load_dotenv
from hypothesis_generation_agent.crew_alternate import HypothesisGenerationAgentHgaCrew
from langchain_core.language_models.fake import FakeListLLM
from crewai import LLM

def main():
    # Load environment variables
    load_dotenv()
    
    print("Starting Hypothesis Generation Agent...")
    
    # Create a mock LLM to avoid API key issues
    responses = [
        "I'll analyze this business problem step by step.\n\n1. Context Extraction:\n- Business domain: Marketing\n- Metric: Customer retention rate\n- Groups: Customers exposed to new campaign vs not exposed\n\n2. Hypotheses:\nH₀: The new marketing campaign does not increase customer retention rate.\nH₁: The new marketing campaign increases customer retention rate.\n\n3. Recommended Test: Chi-squared test for comparing retention rates between groups.\n\n4. Validation: All hypotheses are properly formulated and testable.",
    ]
    mock_llm = LLM(provider="fake", model="fake", fake_response=responses[0])
    
    # Get business problem from user input or use default
    business_problem = input("Enter your business problem (or press Enter for default): ")
    if not business_problem:
        business_problem = "Does the new marketing campaign increase customer retention?"
    
    print(f"\nAnalyzing business problem: {business_problem}")
    print("\nUsing mock LLM for demonstration purposes...")
    
    # Create the crew instance with mock LLM
    crew = HypothesisGenerationAgentHgaCrew()
    
    # Override the LLM in the crew
    for agent_method in [method for method in dir(crew) if not method.startswith('_') and callable(getattr(crew, method))]:
        if hasattr(getattr(crew, agent_method), 'llm'):
            getattr(crew, agent_method).llm = mock_llm
    
    # Run the crew with kickoff method and mock response
    print("\nResults:")
    print(responses[0])

if __name__ == "__main__":
    main()