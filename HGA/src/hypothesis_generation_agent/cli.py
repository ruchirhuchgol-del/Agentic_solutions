# src/hypothesis_generation_agent/cli.py

import sys
import click
import logging

from .crew import HypothesisGenerationAgentHgaCrew
from .config import setup_logging

# Setup logging for the entire application
setup_logging()
logger = logging.getLogger(__name__)

@click.group()
def cli():
    """Hypothesis Generation Agent (HGA) - A CLI tool to automate statistical hypothesis generation."""
    pass

@cli.command()
@click.option(
    '--problem', 
    '-p', 
    prompt='Business Problem',
    help='The business problem you want to analyze (e.g., "Does the new UI increase user engagement?").'
)
def run(problem: str):
    """Run the hypothesis generation crew for a given business problem."""
    click.echo(click.style("--- Starting HGA Analysis ---", fg='blue', bold=True))
    try:
        inputs = {'business_problem': problem}
        crew = HypothesisGenerationAgentHgaCrew()
        result = crew.kickoff(inputs=inputs)
        
        click.echo(click.style("\n--- Analysis Complete ---", fg='green', bold=True))
        click.echo(result)

    except Exception as e:
        click.echo(click.style(f"\nAn error occurred: {e}", fg='red', bold=True))
        logger.error("CLI run failed", exc_info=True)
        sys.exit(1)

@cli.command()
@click.argument('n_iterations', type=int)
@click.argument('filename', type=str)
def train(n_iterations: int, filename: str):
    """Train the crew for a given number of iterations."""
    click.echo(f"Training crew for {n_iterations} iterations. Output will be saved to {filename}.")
    try:
        inputs = {'business_problem': 'Sample business problem for training.'}
        crew = HypothesisGenerationAgentHgaCrew()
        crew.crew().train(n_iterations=n_iterations, filename=filename, inputs=inputs)
        click.echo(click.style("Training complete.", fg='green'))
    except Exception as e:
        click.echo(click.style(f"An error occurred during training: {e}", fg='red'))
        sys.exit(1)

@cli.command()
@click.argument('task_id', type=str)
def replay(task_id: str):
    """Replay the crew execution from a specific task."""
    click.echo(f"Replaying crew execution from task ID: {task_id}")
    try:
        crew = HypothesisGenerationAgentHgaCrew()
        result = crew.crew().replay(task_id=task_id)
        click.echo(result)
    except Exception as e:
        click.echo(click.style(f"An error occurred during replay: {e}", fg='red'))
        sys.exit(1)

@cli.command()
@click.argument('n_iterations', type=int)
@click.argument('model_name', type=str)
def test(n_iterations: int, model_name: str):
    """Test the crew execution and returns the results."""
    click.echo(f"Testing crew for {n_iterations} iterations using model: {model_name}")
    try:
        inputs = {'business_problem': 'Sample business problem for testing.'}
        crew = HypothesisGenerationAgentHgaCrew()
        crew.crew().test(n_iterations=n_iterations, openai_model_name=model_name, inputs=inputs)
        click.echo(click.style("Testing complete.", fg='green'))
    except Exception as e:
        click.echo(click.style(f"An error occurred during testing: {e}", fg='red'))
        sys.exit(1)

def main():
    """Entry point for the CLI."""
    cli()
