from typing import List

RULES = [
    {
        "keywords": ["cash flow", "cashflow", "liquidity", "runway"],
        "solution": "Implement automated cash-flow forecasting and scenario modeling with rolling weekly reports.",
    },
    {
        "keywords": ["bookkeeping", "accounts", "reconciliation", "ledger"],
        "solution": "Use a centralized bookkeeping workflow with bank feed syncing and expense categorization automation.",
    },
    {
        "keywords": ["invoice", "billing", "payments", "collections"],
        "solution": "Add invoice management and payment reminders so customers pay on time and overdue balances are tracked automatically.",
    },
    {
        "keywords": ["forecast", "budget", "planning", "projection"],
        "solution": "Provide budget planning dashboards and variance alerts so the business can act before targets slip.",
    },
    {
        "keywords": ["report", "reporting", "dashboard", "insights"],
        "solution": "Create executive dashboards with KPI tracking, trend analysis, and one-click financial summaries.",
    },
    {
        "keywords": ["manual", "spreadsheet", "excel", "csv"],
        "solution": "Streamline operations by uploading financial data once and generating structured business insights automatically.",
    },
    {
        "keywords": ["growth", "scale", "expansion"],
        "solution": "Build growth playbooks that combine customer, sales, and cash metrics to reveal the highest-impact next steps.",
    },
    {
        "keywords": ["tax", "compliance", "audit", "regulation"],
        "solution": "Bundle compliance checks and tax-ready reports so the business is prepared for audits and filings.",
    },
    {
        "keywords": ["customer", "churn", "retention", "satisfaction"],
        "solution": "Add customer retention analytics and proactive alerts when revenue risks are rising.",
    },
]

FALLBACK_SOLUTIONS = [
    "Start with a short survey of the business and build a tailored roadmap for cash, reporting, and operational efficiency.",
    "Centralize financial data in one place, then generate automated weekly insights for better decision-making.",
]


def generate_solutions(pain_points: List[str]) -> List[str]:
    text = " ".join(pain_points).lower()
    recommendations = []

    for rule in RULES:
        if any(keyword in text for keyword in rule["keywords"]):
            recommendations.append(rule["solution"])

    if not recommendations:
        recommendations = FALLBACK_SOLUTIONS

    # Remove duplicates while preserving order
    seen = set()
    unique = []
    for solution in recommendations:
        if solution not in seen:
            seen.add(solution)
            unique.append(solution)

    return unique
