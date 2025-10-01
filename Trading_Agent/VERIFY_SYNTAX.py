"""
Verify syntax of all Python files without requiring dependencies
"""

import sys
import os
import ast

def check_syntax(file_path):
    """Check syntax of a Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Error reading file: {e}"

def verify_tools():
    """Verify syntax of all tool files"""
    print("Verifying tool files...")
    tools_dir = "src/autonomous_trading_crew/tools"
    if not os.path.exists(tools_dir):
        print(f"❌ Tools directory not found: {tools_dir}")
        return False
        
    tool_files = [f for f in os.listdir(tools_dir) if f.endswith('.py')]
    all_good = True
    
    for tool_file in tool_files:
        file_path = os.path.join(tools_dir, tool_file)
        success, error = check_syntax(file_path)
        if success:
            print(f"✅ {tool_file}: Syntax OK")
        else:
            print(f"❌ {tool_file}: Syntax Error - {error}")
            all_good = False
            
    return all_good

def verify_agents():
    """Verify syntax of all agent files"""
    print("\nVerifying agent files...")
    agents_dir = "src/autonomous_trading_crew/agents"
    if not os.path.exists(agents_dir):
        print(f"❌ Agents directory not found: {agents_dir}")
        return False
        
    agent_files = [f for f in os.listdir(agents_dir) if f.endswith('.py')]
    all_good = True
    
    for agent_file in agent_files:
        file_path = os.path.join(agents_dir, agent_file)
        success, error = check_syntax(file_path)
        if success:
            print(f"✅ {agent_file}: Syntax OK")
        else:
            print(f"❌ {agent_file}: Syntax Error - {error}")
            all_good = False
            
    return all_good

def verify_models():
    """Verify syntax of all model files"""
    print("\nVerifying model files...")
    models_dir = "models"
    if not os.path.exists(models_dir):
        print(f"⚠️  Models directory not found: {models_dir}")
        return True  # Not critical for now
        
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.py')]
    all_good = True
    
    for model_file in model_files:
        file_path = os.path.join(models_dir, model_file)
        success, error = check_syntax(file_path)
        if success:
            print(f"✅ {model_file}: Syntax OK")
        else:
            print(f"❌ {model_file}: Syntax Error - {error}")
            all_good = False
            
    return all_good

def main():
    """Run all syntax verification checks"""
    print("🔍 Syntax Verification for Autonomous Trading Crew")
    print("=" * 50)
    
    tools_ok = verify_tools()
    agents_ok = verify_agents()
    models_ok = verify_models()
    
    print(f"\n🏁 Verification Results:")
    if tools_ok and agents_ok and models_ok:
        print("🎉 All files have correct syntax!")
        return 0
    else:
        print("⚠️  Some files have syntax errors. Please check above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())