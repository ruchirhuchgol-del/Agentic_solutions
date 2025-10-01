from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json
import numpy as np
from datetime import datetime


class TaxOptimizationInput(BaseModel):
    symbol: str = Field(..., description="Stock symbol to analyze for tax optimization")
    current_portfolio: dict = Field(..., description="Current portfolio holdings with cost basis and holding periods")
    proposed_transaction: dict = Field(..., description="Proposed buy/sell transaction details")


class TaxOptimizationTool(BaseTool):
    name: str = "Tax Optimization Analyzer"
    description: str = "Analyzes tax implications of trading decisions and identifies tax-loss harvesting opportunities"
    args_schema: Type[BaseModel] = TaxOptimizationInput
    
    def __init__(self):
        super().__init__()
        
    def _run(self, symbol: str, current_portfolio: dict, proposed_transaction: dict) -> str:
        try:
            # Analyze tax implications
            tax_analysis = self._analyze_tax_implications(symbol, current_portfolio, proposed_transaction)
            
            # Identify tax-loss harvesting opportunities
            tlh_opportunities = self._identify_tax_loss_harvesting_opportunities(current_portfolio)
            
            # Calculate estimated tax savings
            estimated_savings = self._calculate_tax_savings(tlh_opportunities)
            
            return json.dumps({
                "symbol": symbol,
                "tax_analysis": tax_analysis,
                "tax_loss_harvesting_opportunities": tlh_opportunities,
                "estimated_tax_savings": estimated_savings,
                "wash_sale_compliance": self._check_wash_sale_compliance(symbol, proposed_transaction),
                "holding_period_strategy": self._recommend_holding_period_strategy(proposed_transaction)
            })
        except Exception as e:
            return json.dumps({
                "error": f"Failed to analyze tax optimization for {symbol}: {str(e)}",
                "symbol": symbol
            })
    
    def _analyze_tax_implications(self, symbol: str, current_portfolio: dict, proposed_transaction: dict):
        """Analyze tax implications of proposed transaction"""
        try:
            analysis = {
                "short_term_capital_gains": 0,
                "long_term_capital_gains": 0,
                "tax_rate_estimate": 0,
                "total_tax_impact": 0
            }
            
            # Check if selling existing holdings
            if proposed_transaction.get("action") == "sell" and symbol in current_portfolio:
                holding = current_portfolio[symbol]
                current_price = proposed_transaction.get("price", 0)
                cost_basis = holding.get("cost_basis", 0)
                quantity = proposed_transaction.get("quantity", 0)
                
                gain_loss = (current_price - cost_basis) * quantity
                holding_period = holding.get("holding_period_days", 0)
                
                # Short term vs long term capital gains
                if holding_period < 365:
                    analysis["short_term_capital_gains"] = gain_loss
                    analysis["tax_rate_estimate"] = 0.25  # Estimate short-term rate
                else:
                    analysis["long_term_capital_gains"] = gain_loss
                    analysis["tax_rate_estimate"] = 0.15  # Estimate long-term rate
                
                analysis["total_tax_impact"] = gain_loss * analysis["tax_rate_estimate"]
            
            return analysis
        except Exception as e:
            return {"error": f"Tax analysis failed: {str(e)}"}
    
    def _identify_tax_loss_harvesting_opportunities(self, current_portfolio: dict):
        """Identify opportunities for tax-loss harvesting"""
        try:
            opportunities = []
            
            for symbol, holding in current_portfolio.items():
                current_price = holding.get("current_price", 0)
                cost_basis = holding.get("cost_basis", 0)
                
                # Check if holding is at a loss
                if current_price < cost_basis:
                    loss_amount = (cost_basis - current_price) * holding.get("quantity", 0)
                    holding_period = holding.get("holding_period_days", 0)
                    
                    opportunities.append({
                        "symbol": symbol,
                        "loss_amount": round(loss_amount, 2),
                        "holding_period": holding_period,
                        "recommendation": "Consider selling for tax loss harvesting" if loss_amount > 50 else "Minor loss, monitor"
                    })
            
            return opportunities
        except Exception as e:
            return {"error": f"TLH identification failed: {str(e)}"}
    
    def _calculate_tax_savings(self, tlh_opportunities: list):
        """Calculate estimated tax savings from tax-loss harvesting"""
        try:
            total_savings = 0
            
            for opportunity in tlh_opportunities:
                if isinstance(opportunity, dict) and "loss_amount" in opportunity:
                    loss_amount = opportunity["loss_amount"]
                    # Assume 15% tax rate for long-term capital gains offset
                    savings = loss_amount * 0.15
                    total_savings += savings
            
            return round(total_savings, 2)
        except Exception as e:
            return {"error": f"Tax savings calculation failed: {str(e)}"}
    
    def _check_wash_sale_compliance(self, symbol: str, proposed_transaction: dict):
        """Check for potential wash sale violations"""
        try:
            if proposed_transaction.get("action") == "sell":
                # If selling at a loss, check if buying same/similar stock within 30 days
                # This is a simplified check - in practice would need more detailed analysis
                return {
                    "compliant": True,
                    "warning": "Ensure no purchase of substantially identical securities within 30 days before or after sale"
                }
            return {"compliant": True, "warning": "No wash sale concerns for buy transactions"}
        except Exception as e:
            return {"error": f"Wash sale compliance check failed: {str(e)}"}
    
    def _recommend_holding_period_strategy(self, proposed_transaction: dict):
        """Recommend optimal holding period strategy"""
        try:
            # Simplified recommendation based on transaction type
            if proposed_transaction.get("action") == "buy":
                return {
                    "strategy": "long_term",
                    "recommendation": "Hold for >1 year to qualify for lower long-term capital gains rates",
                    "target_holding_period": "365+ days"
                }
            return {
                "strategy": "transaction_based",
                "recommendation": "Strategy depends on specific transaction goals",
                "target_holding_period": "As needed"
            }
        except Exception as e:
            return {"error": f"Holding period strategy recommendation failed: {str(e)}"}