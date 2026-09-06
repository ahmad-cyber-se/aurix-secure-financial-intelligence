from decimal import Decimal


def build_portfolio_insight(summary: dict) -> dict:
    precious = summary["allocations"].get("GOLD", Decimal("0")) + summary["allocations"].get("SILVER", Decimal("0"))
    etfs = summary["allocations"].get("ETF", Decimal("0"))

    if precious >= Decimal("60"):
        risk = "High"
        recommendation = "Consider reducing concentration in precious metals and increasing diversified ETF exposure."
    elif precious >= Decimal("40"):
        risk = "Medium"
        recommendation = "Consider increasing geographic and asset-class diversification."
    elif etfs < Decimal("20"):
        risk = "Medium"
        recommendation = "Consider a broader diversified ETF allocation if it fits your investment objectives."
    else:
        risk = "Low"
        recommendation = "Current allocation is relatively diversified; continue monitoring concentration and liquidity."

    return {
        "portfolio_risk": risk,
        "observation": f"{precious:.2f}% of the portfolio is currently allocated to precious metals.",
        "recommendation": recommendation,
        "engine": "RULE-BASED",
    }
