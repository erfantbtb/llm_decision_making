from agent import LLMAgent
from simulation import MonteCarloSimulation
import streamlit as st
from models.simulation_parameters import CarSimulationParameters
import json 


st.title("Car Consultant Bot")

schema = CarSimulationParameters.model_json_schema()
params = None
keys = ["avg_buy_cost", "avg_lease_cost", "prob_lease_cheaper"]
with open("app/configs/system_prompts.json", "r") as f:
    system_prompt = json.load(f)[0]["content"]

system_prompt = f"""{system_prompt} USE REQUIRED PARAMETER SCHEMA IN (INTERNAL — DO NOT SHOW TO CUSTOMER): {schema}.
                    data_complete is false until all other params are extracted"""

if "messages" not in st.session_state:
    st.session_state.messages = []

llm = LLMAgent(system_prompt=system_prompt)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Welcome to car consultant bot."):    
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt = f"{prompt} if all parameters are extracted, give data in json format which keys are param names and values are the users values"
    st.session_state.messages.append({"role": "user", "content": prompt})


    assistant_json = llm.run(
        st.session_state.messages,
    )
    
    response_json = llm.run(
        st.session_state.messages,
        format=schema
    )

    st.session_state.messages.append({"role": "assistant", "content": assistant_json})
    with st.chat_message("assistant"):
        st.markdown(assistant_json)
        
    params = CarSimulationParameters.model_validate_json(response_json)
    
    if params.data_complete:
        with st.chat_message("assistant"):
            result = MonteCarloSimulation(params).run()
            result_msg = [{
                "role": "user",
                "content": str({k: result[k] for k in keys if k in result})
                }]
            response_result = llm.run(result_msg)
            st.markdown(response_result)

    