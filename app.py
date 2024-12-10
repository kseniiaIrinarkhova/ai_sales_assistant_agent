# Import libraries
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools import TavilySearchResults
from models import models

# set default model
if 'default_model' not in st.session_state:
    st.session_state['default_model'] = 'llama3-8b-8192'

# Model and Agent Tools
llm = ChatGroq(api_key=st.secrets['GROQ_API_KEY'])
parser = StrOutputParser()
search = TavilySearchResults(max_results=2)

# function to change default LLM
def change_model():
    st.session_state['default_model'] = st.session_state.model
    return

# Page Config
st.set_page_config(page_title="AI Sales Assistant")

# Sidebar
st.sidebar.title("AI Sales Assistant settings")
temperature = st.sidebar.slider('Temperature', min_value=0.0, max_value=1.0, value=0.5, step=0.01, key='temperature')
st.sidebar.selectbox('Model', models, index=models.index(st.session_state['default_model']), key='model', on_change=change_model)


# Main Page
st.title('AI Sales Assistant')
st.text(f"AI Sales Assistant Powered by Groq. Settings: LLM **{st.session_state.default_model}**, temperature **{temperature}**.")
st.markdown("### Help sales teams gather insights about their products, competitors, and target customers.")

with st.form("product_research", clear_on_submit=True):
    company_name = st.text_input("Enter your company name")
    company_website = st.text_input("Enter your company website")
    product_name = st.text_input("Enter your product name")
    product_category = st.text_input("Enter your product category")
    competitors = st.text_area("Enter your competitors")
    target_customer = st.text_input("Enter your target customer")
    optional = st.text_area("optional")
    submit_button = st.form_submit_button(label='Submit')