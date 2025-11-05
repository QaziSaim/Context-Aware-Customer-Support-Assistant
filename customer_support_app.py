# -*- coding: utf-8 -*-
"""
# 🧠 LLM Case Study: Context-Aware Customer Support Assistant

This Streamlit app demonstrates a context-aware chatbot built using:
- LangChain + LangGraph
- Google Gemini (via langchain-google-vertexai)
- MemorySaver for contextual memory
- Message trimming for token efficiency
- Persona-controlled responses (Elegant English Butler)
"""

import streamlit as st
import os
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import trim_messages
from dotenv import load_dotenv

load_dotenv()

# -------------------------------
# 🌐 API Key Setup
# -------------------------------
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# -------------------------------
# 🧠 Model Initialization
# -------------------------------
model = init_chat_model(model='gemini-2.5-flash', model_provider='google_genai')

# -------------------------------
# ✂️ Trimmer Initialization
# -------------------------------
trimmer = trim_messages(
    max_tokens=100,
    strategy='last',
    token_counter=model,
    allow_partial=False,
    start_on='human'
)

# -------------------------------
# 🧩 Build Graph Workflow
# -------------------------------
workflow = StateGraph(state_schema=MessagesState)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an Elegant Butler from England. Answer all questions with politeness and elegance."),
    MessagesPlaceholder(variable_name='messages')
])

def call_model(state: MessagesState):
    trimmed_messages = trimmer.invoke(state['messages'])
    prompt = prompt_template.invoke({'messages': trimmed_messages})
    response = model.invoke(prompt)
    return {'messages': response}

workflow.add_edge(START, 'model')
workflow.add_node('model', call_model)

memory = MemorySaver()
chatbot = workflow.compile(checkpointer=memory)

# -------------------------------
# 💬 Streamlit UI Setup
# -------------------------------
st.set_page_config(page_title="Context-Aware Support Assistant", page_icon="🤖", layout="centered")

st.title("🤖 Context-Aware Customer Support Assistant")
st.caption("Powered by LangChain + Gemini + LangGraph")

st.markdown("""
This chatbot demonstrates **contextual memory**, **persona control**, and **message trimming**.
Ask follow-up questions and notice how it remembers your context — just like a real support agent.
""")

# -------------------------------
# 💾 Manage Session State
# -------------------------------
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = "session_" + str(os.getpid())

config = {'configurable': {'thread_id': st.session_state["thread_id"]}}

# -------------------------------
# 🗣️ Chat Interface
# -------------------------------
user_input = st.chat_input("Type your message...")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if user_input:
    input_messages = [("user", user_input)]
    output = chatbot.invoke({'messages': input_messages}, config)
    response = output['messages'][-1].content

    st.session_state.chat_history.append(("🧍‍♂️ You", user_input))
    st.session_state.chat_history.append(("🤖 Butler", response))

# -------------------------------
# 💬 Display Chat History
# -------------------------------
for sender, message in st.session_state.chat_history:
    with st.chat_message("user" if sender == "🧍‍♂️ You" else "assistant"):
        st.markdown(f"**{sender}:** {message}")

# -------------------------------
# ✅ Conclusion Section
# -------------------------------
# st.divider()
# st.markdown("""
# ### ✅ Conclusion

# This case study shows a practical use of **LLMs in intelligent customer support systems**:
# - Maintains conversation context with `MemorySaver`
# - Reduces token usage with `trim_messages`
# - Responds with a polite English butler persona

# **Next Steps:**
# - Add persistent memory with Redis or SQLite  
# - Integrate user intent classification  
# - Build a ticketing system backend  

# ---
# Made with ❤️ using **LangChain**, **LangGraph**, and **Streamlit**
# """)
