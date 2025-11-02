"""
Simple Hypothesis Generation Demo
This script demonstrates hypothesis generation without complex dependencies.
"""
from langchain_core.language_models.fake import FakeListLLM
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def main():
    print("Starting Simple Hypothesis Generation Demo...")
    
    # Create a mock LLM with predefined responses
    responses = [
        "I'll generate 3 testable hypotheses for the marketing campaign:\n\n1. Customers exposed to the new marketing campaign have a 15% higher 90-day retention rate compared to those not exposed.\n\n2. The new marketing campaign increases customer engagement (measured by app usage frequency) by at least 20%.\n\n3. Customers acquired through the new marketing campaign have a 10% higher lifetime value than those acquired through previous campaigns.",
        "Validation Report: All three hypotheses are well-formulated and align with business objectives. They are specific, measurable, and testable."
    ]
    mock_llm = FakeListLLM(responses=responses)
    
    # Create tools for the agent
    def generate_hypotheses(problem_statement):
        """Generate testable hypotheses for a given business problem."""
        return responses[0]
    
    def validate_hypotheses(hypotheses):
        """Validate the hypotheses and ensure they align with business goals."""
        return responses[1]
    
    tools = [
        Tool(
            name="HypothesisGenerator",
            func=generate_hypotheses,
            description="Generate testable hypotheses for a business problem"
        ),
        Tool(
            name="HypothesisValidator",
            func=validate_hypotheses,
            description="Validate hypotheses and ensure they align with business goals"
        )
    ]
    
    # Create a prompt template
    prompt = PromptTemplate.from_template(
        """You are a hypothesis generation agent.
        
        You have access to the following tools:
        {tools}
        
        Use the following format:
        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question
        
        Begin!
        
        Question: {input}
        {agent_scratchpad}"""
    )
    
    # Create the agent
    agent = create_react_agent(mock_llm, tools, prompt)
    
    # Create the agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    # Run the agent
    problem_statement = "Does the new marketing campaign increase customer retention?"
    print(f"\nProblem Statement: {problem_statement}")
    
    result = agent_executor.invoke({"input": f"Generate and validate hypotheses for the business problem: '{problem_statement}'"})
    
    print("\nResults:")
    print(result["output"])

if __name__ == "__main__":
    main()