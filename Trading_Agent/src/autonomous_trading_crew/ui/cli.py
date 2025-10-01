
import sys
import os
import json
import argparse
from datetime import datetime
import pandas as pd

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from autonomous_trading_crew.crew import AutonomousTradingCrewCrew

def main():
    parser = argparse.ArgumentParser(description="Autonomous Trading Crew CLI")
    parser.add_argument("stock_symbol", help="Stock symbol to analyze (e.g., AAPL, GOOGL)")
    parser.add_argument("--output", "-o", help="Output file for results (JSON format)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    print(f"🤖 Autonomous Trading Crew Analysis")
    print(f"Analyzing stock: {args.stock_symbol.upper()}")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    try:
        # Run the crew
        inputs = {'stock_symbol': args.stock_symbol.upper()}
        crew = AutonomousTradingCrewCrew().crew()
        
        if args.verbose:
            print("Starting analysis...")
            
        result = crew.kickoff(inputs=inputs)
        
        # Display results
        print("\n✅ Analysis completed successfully!")
        print("-" * 50)
        
        # Try to parse and display key information
        try:
            # If result is a string, try to parse it as JSON
            if isinstance(result.raw, str):
                result_data = json.loads(result.raw)
            else:
                result_data = result.raw
                
            # Display executive summary
            print("\n📋 EXECUTIVE SUMMARY")
            print(f"Stock Symbol: {args.stock_symbol.upper()}")
            print(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Save to file if requested
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(result_data, f, indent=2)
                print(f"\n💾 Results saved to: {args.output}")
                
        except json.JSONDecodeError:
            # If we can't parse as JSON, display as string
            print("\n📄 RESULTS:")
            print(str(result.raw))
            
            # Save to file if requested
            if args.output:
                with open(args.output, 'w') as f:
                    f.write(str(result.raw))
                print(f"\n💾 Results saved to: {args.output}")
                
    except Exception as e:
        print(f"\n❌ An error occurred during analysis: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()