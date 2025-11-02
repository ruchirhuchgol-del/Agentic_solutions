"""
Simplified demo of the Hypothesis Generation Agent.
This script demonstrates the core functionality without complex dependencies.
"""
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    print("Starting Hypothesis Generation Agent Demo...")
    
    # Use mock LLM for demonstration purposes
    print("Using mock LLM for demonstration")
    from langchain_core.language_models.fake import FakeListLLM
    responses = [
        "Here are 3 testable hypotheses for the marketing campaign:\n\n1. Customers exposed to the new marketing campaign have a 15% higher 90-day retention rate compared to those not exposed.\n\n2. The new marketing campaign increases customer engagement (measured by app usage frequency) by at least 20%.\n\n3. Customers acquired through the new marketing campaign have a 10% higher lifetime value than those acquired through previous campaigns.",
        "Validation Report:\nAll three hypotheses are well-formulated and align with business objectives. They are specific, measurable, and testable. The first hypothesis directly addresses retention, the second focuses on engagement as a leading indicator, and the third examines long-term value. I recommend proceeding with testing all three hypotheses."
    ]
    llm = FakeListLLM(responses=responses)
    
    # Create the agents
    data_scientist = Agent(
        role="Data Scientist",
        goal="Generate statistically sound hypotheses",
        backstory="You are an expert data scientist with years of experience in hypothesis formulation.",
        verbose=True,
        llm=llm
    )
    
    business_analyst = Agent(
        role="Business Analyst",
        goal="Ensure hypotheses align with business objectives",
        backstory="You understand business metrics and how to translate them into testable hypotheses.",
        verbose=True,
        llm=llm
    )
    
    # Create the tasks
    hypothesis_task = Task(
        description="Generate 3 testable hypotheses for the business problem: 'Does the new marketing campaign increase customer retention?'",
        agent=data_scientist,
        expected_output="A list of 3 well-formulated hypotheses"
    )
    
    validation_task = Task(
        description="Validate the hypotheses and ensure they align with business goals and are testable.",
        agent=business_analyst,
        expected_output="Validation report on the hypotheses"
    )
    
    # Create the crew
    hypothesis_crew = Crew(
        agents=[data_scientist, business_analyst],
        tasks=[hypothesis_task, validation_task],
        verbose=True
    )
    
    # Run the crew
    result = hypothesis_crew.kickoff()
    
    print("\nResults:")
    print(result)

if __name__ == "__main__":
    main()