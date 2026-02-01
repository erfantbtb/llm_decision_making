from pydantic import BaseModel
from typing import List
from agent import LLMAgent
import json

with open("app/configs/system_prompts.json", "r") as f:
    file = json.load(f)
    
# class SimulationParameters(BaseModel):
#     purchase_price: float
#     monthly_lease: float
#     duration_months: int
#     estimated_maintenance_avg: float
#     maintenance_std_dev: float 
    


# user_input = "I'm looking at a car for $30,000. Or I can lease it for $400/mo for 3 years. I expect maintenance to be about $100 a month but it might vary by $50."
# llm = LLMAgent()
# ans = llm.run([{"role": "user", "content": f"Extract lease vs buy variables from this: {user_input}"}],
#         SimulationParameters.model_json_schema())
# params = SimulationParameters.model_validate_json(ans)

