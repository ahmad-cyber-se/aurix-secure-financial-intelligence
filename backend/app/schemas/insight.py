from pydantic import BaseModel


class InsightResponse(BaseModel):
    portfolio_risk: str
    observation: str
    recommendation: str
    engine: str = "RULE-BASED"
