#!/usr/bin/env python
"""
Demo Script for Autonomous Trading Crew

This script demonstrates how to use the Autonomous Trading Crew system
to analyze stocks and generate trading recommendations.
"""

import sys
import os
import json
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def demo_overview():
    """Print demo overview"""
    print("🤖 Autonomous Trading Crew Demo")
    print("=" * 50)
    print("This demo showcases the capabilities of the Autonomous Trading Crew,")
    print("an AI-powered multi-agent system for stock market analysis.")
    print()

def demo_components():
    """Demonstrate system components"""
    print("🧩 Core Components:")
    print("  1. Market Intelligence Analyst")
    print("  2. Risk Management Officer") 
    print("  3. Trade Execution Specialist")
    print("  4. Explainability Reporter")
    print()

def demo_tools():
    """Demonstrate available tools"""
    print("🛠️  Custom Financial Tools:")
    print("  • Financial Data Tool (market data & technical indicators)")
    print("  • Financial Sentiment Tool (news sentiment analysis)")
    print("  • Risk Assessment Tool (VaR, stress testing)")
    print("  • Predictive Analytics Tool (LSTM, ARIMA, SARIMA)")
    print()

def demo_usage():
    """Demonstrate usage examples"""
    print("🚀 Usage Examples:")
    print("  Command Line: python src/autonomous_trading_crew/main.py run AAPL")
    print("  Web Interface: streamlit run src/autonomous_trading_crew/ui/streamlit_app.py")
    print("  Jupyter Notebook: Open src/autonomous_trading_crew/examples/interactive_analysis.ipynb")
    print()

def demo_features():
    """Demonstrate key features"""
    print("✨ Key Features:")
    print("  • Real-time market data analysis")
    print("  • News sentiment processing with FinBERT")
    print("  • Risk assessment with Value at Risk")
    print("  • Price prediction with LSTM/ARIMA/SARIMA")
    print("  • Comprehensive reporting with explainability")
    print()

def main():
    """Run the demo"""
    demo_overview()
    demo_components()
    demo_tools()
    demo_features()
    demo_usage()
    
    print("📈 To run a full analysis:")
    print("  1. Set up your environment variables (OPENAI_API_KEY, SERPER_API_KEY)")
    print("  2. Install dependencies: pip install -r requirements.txt")
    print("  3. Run analysis: python src/autonomous_trading_crew/main.py run TSLA")
    print()
    print("📄 For detailed information, see:")
    print("  • README.md - Setup and usage instructions")
    print("  • IMPLEMENTATION_SUMMARY.md - Technical details")
    print("  • src/autonomous_trading_crew/examples/interactive_analysis.ipynb - Interactive demo")

if __name__ == "__main__":
    main()