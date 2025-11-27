from pydantic import BaseModel, Field
from typing import List

class InvestmentMemo(BaseModel):
    """Structure for the final financial analysis report."""
    
    company_name: str = Field(description="The name of the company analyzed.")
    
    summary: str = Field(description="A concise executive summary of the gathered news and data.")
    
    key_pros: List[str] = Field(description="List of 3-5 positive indicators or opportunities.")
    
    key_cons: List[str] = Field(description="List of 3-5 negative risks or challenges.")
    
    risk_score: int = Field(description="A risk score from 1 (Safe) to 10 (High Risk).")
    
    verdict: str = Field(
        description="The final investment recommendation.",
        enum=["Buy", "Hold", "Sell"]
    )
    
    reasoning: str = Field(description="A brief explanation justifying the verdict and risk score.")