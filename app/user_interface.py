from agent import DecisionAgent

agent = DecisionAgent()

result = agent.extract_car_parameters(
    "I want to buy a $25,000 car, lease costs $400 per month for 36 months. Maintenance around $500 per year with some variation."
)

print(result)
