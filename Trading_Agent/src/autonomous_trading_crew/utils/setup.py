import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    import sys
    if sys.version_info < (3, 10) or sys.version_info >= (3, 14):
        print("Warning: Python version should be >=3.10 and <3.14 for optimal compatibility")
        return False
    return True

def install_dependencies():
    """Install required dependencies"""
    try:
        # Try using uv first (faster)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "uv"])
        subprocess.check_call(["uv", "pip", "install", "-e", "."])
        print("Dependencies installed successfully using uv")
        return True
    except:
        try:
            # Fallback to pip
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
            print("Dependencies installed successfully using pip")
            return True
        except Exception as e:
            print(f"Failed to install dependencies: {e}")
            return False

def check_api_keys():
    """Check if required API keys are set"""
    required_keys = ["OPENAI_API_KEY", "SERPER_API_KEY"]
    missing_keys = []
    
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    if missing_keys:
        print("Warning: The following API keys are missing:")
        for key in missing_keys:
            print(f"  - {key}")
        print("Please set these in your environment or .env file")
        return False
    
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_path = Path(".env")
    example_path = Path(".env.example")
    
    if not env_path.exists() and example_path.exists():
        with open(example_path, "r") as example_file:
            with open(env_path, "w") as env_file:
                env_file.write(example_file.read())
        print(".env file created from .env.example")
        print("Please update the .env file with your actual API keys")
        return True
    elif not env_path.exists():
        with open(env_path, "w") as env_file:
            env_file.write("# API Keys\n")
            env_file.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            env_file.write("SERPER_API_KEY=your_serper_api_key_here\n")
        print(".env file created")
        print("Please update the .env file with your actual API keys")
        return True
    
    return True

def setup_project():
    """Main setup function"""
    print("🤖 Setting up Autonomous Trading Crew...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        print("Warning: Python version may not be compatible")
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    print("Installing dependencies...")
    if not install_dependencies():
        print("Failed to install dependencies")
        return False
    
    # Check API keys
    check_api_keys()
    
    print("\n✅ Setup completed!")
    print("\nNext steps:")
    print("1. Update the .env file with your actual API keys")
    print("2. Run 'crewai run' to start the analysis")
    print("3. Or run 'streamlit run src/autonomous_trading_crew/ui/streamlit_app.py' for the web interface")
    
    return True

if __name__ == "__main__":
    setup_project()