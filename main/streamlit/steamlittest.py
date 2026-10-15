# app.py
import streamlit as st
import sys
import os
from langgraph.types import Command

# Add project root (langchain-demo) to sys.path so `supplyChainBot.*` imports resolve
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.append(project_root)

from supplyChainBot.main.graphs.supplyChainGraph import app

st.title("ABC Supply Chain Assistant")

if "history" not in st.session_state:
    st.session_state.history = []



for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if "awaiting_approval" not in st.session_state:
    st.session_state.awaiting_approval = False

if (st.session_state.awaiting_approval == False):
    query = st.chat_input("Enter your query, press exit to quit: ")
    if query:
        st.session_state.history.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.write(query)

        inp = {"messages" : [
                {
                    "role": "user",
                    "content": query
                }
            ]}
        st.session_state.config = {"configurable" : {"thread_id": "test-thread-1"}}

        result = app.invoke(inp, config=st.session_state.config)

        if(result.get("__interrupt__")):
            
            st.session_state.interrupt_payload = result.get("__interrupt__")
            st.session_state.awaiting_approval = True
            
            #st.stop()

        else:
            with st.chat_message("assistant"):
                
                st.write(result["messages"][-1].content)
                with st.expander("Retrieved context (debug)"):
                    st.write(result["messages"])

            st.session_state.history.append({"role": "assistant", "content": result["messages"]})

if st.session_state.awaiting_approval:
    st.write(st.session_state.interrupt_payload)
    approveClicked = st.button("Approve")
    rejectClicked = st.button("Reject")
    if(approveClicked or rejectClicked):
        result = app.invoke(Command(resume=(True if approveClicked else False)), config=st.session_state.config)
        with st.chat_message("assistant"):            
            st.write(result["messages"][-1].content)
            with st.expander("Retrieved context (debug)"):
                st.write(result["messages"])
        st.session_state.awaiting_approval = False
        st.session_state.history.append({"role": "assistant", "content": result["messages"]})
        st.rerun()