"""
Main entry point for the GitHub Profile Optimizer.

Provides command-line interface for running profile optimization tasks.
"""

import sys
import os
from src.github_profile_optimizer.crew import GithubProfileOptimizerCrew
from src.github_profile_optimizer.config.settings import settings
from src.github_profile_optimizer.utils.logger import get_logger
from src.github_profile_optimizer.auth.tenant_manager import tenant_manager
from src.github_profile_optimizer.utils.cache_manager import cache_manager
from src.github_profile_optimizer.utils.rate_limiter import rate_limiter

logger = get_logger("main")


def run():
    """
    Run the crew with extended options.
    """
    inputs = {
        'github_handle': os.getenv('GITHUB_HANDLE', 'sample_value'),
        'target_roles': os.getenv('TARGET_ROLES', 'sample_value'),
        'repos_scope': os.getenv('REPOS_SCOPE', 'sample_value'),
        'dry_run': os.getenv('DRY_RUN', 'sample_value'),
        'limits': os.getenv('LIMITS', 'sample_value')
    }
    
    logger.info("Starting GitHub Profile Optimizer", inputs=inputs)
    
    try:
        result = GithubProfileOptimizerCrew().crew().kickoff(inputs=inputs)
        logger.info("Optimization completed successfully")
        return result
    except Exception as e:
        logger.error("Error during optimization", error=str(e))
        raise


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'github_handle': os.getenv('GITHUB_HANDLE', 'sample_value'),
        'target_roles': os.getenv('TARGET_ROLES', 'sample_value'),
        'repos_scope': os.getenv('REPOS_SCOPE', 'sample_value'),
        'dry_run': os.getenv('DRY_RUN', 'sample_value'),
        'limits': os.getenv('LIMITS', 'sample_value')
    }
    
    logger.info("Training crew", iterations=sys.argv[1] if len(sys.argv) > 1 else "unknown")
    
    try:
        GithubProfileOptimizerCrew().crew().train(
            n_iterations=int(sys.argv[1]), 
            filename=sys.argv[2], 
            inputs=inputs
        )
        logger.info("Training completed successfully")
    except Exception as e:
        logger.error("Error during training", error=str(e))
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    logger.info("Replaying crew execution", task_id=sys.argv[1] if len(sys.argv) > 1 else "unknown")
    
    try:
        result = GithubProfileOptimizerCrew().crew().replay(task_id=sys.argv[1])
        logger.info("Replay completed successfully")
        return result
    except Exception as e:
        logger.error("Error during replay", error=str(e))
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'github_handle': os.getenv('GITHUB_HANDLE', 'sample_value'),
        'target_roles': os.getenv('TARGET_ROLES', 'sample_value'),
        'repos_scope': os.getenv('REPOS_SCOPE', 'sample_value'),
        'dry_run': os.getenv('DRY_RUN', 'sample_value'),
        'limits': os.getenv('LIMITS', 'sample_value')
    }
    
    logger.info("Testing crew", iterations=sys.argv[1] if len(sys.argv) > 1 else "unknown")
    
    try:
        result = GithubProfileOptimizerCrew().crew().test(
            n_iterations=int(sys.argv[1]), 
            openai_model_name=sys.argv[2], 
            inputs=inputs
        )
        logger.info("Testing completed successfully")
        return result
    except Exception as e:
        logger.error("Error during testing", error=str(e))
        raise Exception(f"An error occurred while testing the crew: {e}")


def analyze():
    """
    Analyze a GitHub profile without making changes.
    """
    inputs = {
        'github_handle': os.getenv('GITHUB_HANDLE', 'sample_value'),
        'analysis_only': 'true'
    }
    
    logger.info("Analyzing GitHub profile", handle=inputs['github_handle'])
    
    try:
        # For analysis, we would create a specialized crew or modify the existing one
        # This is a placeholder for the analysis functionality
        result = GithubProfileOptimizerCrew().crew().kickoff(inputs=inputs)
        logger.info("Analysis completed successfully")
        return result
    except Exception as e:
        logger.error("Error during analysis", error=str(e))
        raise


def list_tenants():
    """List all configured tenants."""
    try:
        tenants = tenant_manager.list_tenants()
        print("Configured Tenants:")
        for tenant in tenants:
            print(f"  - {tenant}")
        return tenants
    except Exception as e:
        logger.error("Error listing tenants", error=str(e))
        raise


def show_cache_stats():
    """Show cache statistics."""
    try:
        # This is a simplified view - in reality, we'd have more detailed stats
        print("Cache Statistics:")
        print(f"  L1 (Memory) cache size: {len(cache_manager.l1_cache)}")
        print(f"  L2 (Redis) available: {cache_manager.l2_cache is not None}")
        print(f"  L3 (Disk) cache directory: {cache_manager.l3_cache.cache_dir}")
    except Exception as e:
        logger.error("Error showing cache stats", error=str(e))
        raise


def show_rate_limit_stats():
    """Show rate limit statistics."""
    try:
        remaining = rate_limiter.get_remaining_calls()
        print("Rate Limit Statistics:")
        print(f"  Remaining API calls: {remaining}")
        print(f"  Total capacity: {rate_limiter.capacity}")
    except Exception as e:
        logger.error("Error showing rate limit stats", error=str(e))
        raise


def show_help():
    """Show help information."""
    help_text = """
GitHub Profile Optimizer CLI

Usage: python -m src.github_profile_optimizer.main <command> [<args>]

Commands:
  run                Run the crew
  train              Train the crew for a given number of iterations
  replay             Replay the crew execution from a specific task
  test               Test the crew execution
  analyze            Analyze a GitHub profile without making changes
  list-tenants       List all configured tenants
  cache-stats        Show cache statistics
  rate-limit-stats   Show rate limit statistics
  help               Show this help message

Environment Variables:
  GITHUB_TOKEN       GitHub personal access token (required)
  OPENAI_API_KEY     OpenAI API key (required)
  GITHUB_HANDLE      GitHub username to optimize
  TARGET_ROLES       Target job roles
  REPOS_SCOPE        Repository scope (public/private/all)
  DRY_RUN            Whether to run in dry-run mode
  LIMITS             Optimization level (minimal/moderate/comprehensive)

Examples:
  python -m src.github_profile_optimizer.main run
  python -m src.github_profile_optimizer.main analyze
  python -m src.github_profile_optimizer.main list-tenants
  python -m src.github_profile_optimizer.main help
"""
    print(help_text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
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
    elif command == "analyze":
        analyze()
    elif command == "list-tenants":
        list_tenants()
    elif command == "cache-stats":
        show_cache_stats()
    elif command == "rate-limit-stats":
        show_rate_limit_stats()
    elif command == "help":
        show_help()
    else:
        print(f"Unknown command: {command}")
        show_help()
        sys.exit(1)