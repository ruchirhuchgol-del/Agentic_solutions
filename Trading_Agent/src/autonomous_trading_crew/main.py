#!/usr/bin/env python
import sys
import os
import json
from autonomous_trading_crew.crew import AutonomousTradingCrewCrew

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    # Default stock symbol if none provided
    stock_symbol = "AAPL"
    if len(sys.argv) > 2:
        stock_symbol = sys.argv[2]
    
    inputs = {
        'stock_symbol': stock_symbol
    }
    result = AutonomousTradingCrewCrew().crew().kickoff(inputs=inputs)
    print(result.raw)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'stock_symbol': 'AAPL'
    }
    try:
        AutonomousTradingCrewCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AutonomousTradingCrewCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'stock_symbol': 'AAPL'
    }
    try:
        AutonomousTradingCrewCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        print("Commands:")
        print("  run [<stock_symbol>]    - Run the crew analysis")
        print("  train <iterations> <filename>  - Train the crew")
        print("  replay <task_id>        - Replay a specific task")
        print("  test <iterations> <model_name> - Test the crew")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)