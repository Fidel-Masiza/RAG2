import streamlit as st
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI  # Updated import for OpenAI models
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up Streamlit UI
st.set_page_config(page_title="Conversational Q&A Chatbot")
st.header("Hey, Let's Chat")

# Initialize chat model with OpenAI API key
chat = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0.5)

if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        SystemMessage(content="You are a comedian AI assistant.")
    ]

# Function to get responses from OpenAI model
def get_chatmodel_response(question):
    st.session_state['flowmessages'].append(HumanMessage(content=question))
    
    try:
        # Use invoke instead of __call__
        answer = chat.invoke(st.session_state['flowmessages'])
        st.session_state['flowmessages'].append(AIMessage(content=answer.content))
        return answer.content
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error: Unable to get a response from the model."

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# If ask button is clicked, get the response
if submit and input:
    response = get_chatmodel_response(input)
    st.subheader("The Response is")
    st.write(response)