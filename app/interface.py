from agent import LLMAgent
import streamlit as st
from models.simulation_parameters import CarSimulationParameters
from ollama import chat

st.title("🔍 Parameter Extraction Bot")
system_prompt = """
You are a strict information extraction assistant.

Extract car-related financial parameters from the conversation.

Required parameters:
- purchase_price
- monthly_lease
- duration_months
- estimated_maintenance_avg

Rules:
- If ANY required parameter is missing or unclear, set data_complete to false.
- If ALL required parameters are present and numeric, set data_complete to true.
- Return ONLY valid JSON that matches the provided schema.
- Do NOT explain anything.
"""

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

llm = LLMAgent(system_prompt=system_prompt)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Describe your car decision"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    schema = CarSimulationParameters.model_json_schema()

    try:
        # Extract parameters
        response_json = llm.run(
            st.session_state.messages,
            format=schema
        )

        params = CarSimulationParameters.model_validate_json(response_json)

        # If missing data → ask follow-up
        if not params.data_complete:
            follow_up_messages = [
                {
                    "role": "system",
                    "content": "Ask ONLY for missing numeric parameters. Be concise."
                },
                {
                    "role": "user",
                    "content": f"Extracted so far: {params.model_dump_json()}"
                }
            ]

            resp = chat(
                model="gemma3",
                messages=follow_up_messages,
                stream=False
            )

            reply = resp["message"]["content"]

            with st.chat_message("assistant"):
                st.markdown(reply)

            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )

        # Data complete → just show JSON
        else:
            with st.chat_message("assistant"):
                st.markdown("✅ **All parameters extracted successfully**")
                st.json(params.model_dump())

            st.session_state.messages.append({
                "role": "assistant",
                "content": params.model_dump_json(indent=2)
            })

    except Exception as e:
        with st.chat_message("assistant"):
            st.error(f"Extraction error: {e}")
