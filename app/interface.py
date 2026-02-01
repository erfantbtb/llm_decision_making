from agent import LLMAgent
from simulation import MonteCarloSimulation
import streamlit as st
from models.simulation_parameters import CarSimulationParameters
from ollama import chat
import json 


st.title("Car Consultant Bot")

schema = CarSimulationParameters.model_json_schema()
params = None

with open("app/configs/system_prompts.json", "r") as f:
    system_prompt = json.load(f)[0]["content"]

system_prompt = f"""{system_prompt} USE REQUIRED PARAMETER SCHEMA IN (INTERNAL — DO NOT SHOW TO CUSTOMER): {schema}.
                    data_complete is false until all other params are extracted"""

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

llm = LLMAgent(system_prompt=system_prompt)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Welcome to car consultant bot."):
    # Show user message
    
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt = f"{prompt} if all parameters are extracted, give data in json format which keys are param names and values are the users values"
    st.session_state.messages.append({"role": "user", "content": prompt})


    assistant_json = llm.run(
        st.session_state.messages,
        # format=schema
    )
    
    response_json = llm.run(
        st.session_state.messages,
        format=schema
    )

    st.session_state.messages.append({"role": "assistant", "content": assistant_json})
    with st.chat_message("assistant"):
        st.markdown(assistant_json)
        
    try:
        params = CarSimulationParameters.model_validate_json(response_json)
        all_params_collected = True
        print(params)

    except:
        all_params_collected = False 
        

