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

# LLM settup
# prompt
prompt = """
    You are a helpful AI Sales assistant. Your job is to analyze the provided data, to generate insights. Focus on company strategy, competitor analysis, and leadership info and using optional information if provided. Provide:

    1. ## Company Strategy: Insights into the company/'s activities and priorities from company_data.
    2. ## Competitor Mentions: Mentions of competitors from competitors_data.
    2.1 ### Competitor Analysis: Insights into competitors from competitors_data.
    2.2 ### Competitor Comparison: Comparison of the company with competitors from competitors_data.
    3. ## Leadership Information: Relevant leaders and their roles.
    4. ## Product/Strategy Summary: Insights from product_data.
    5. ## Target Customer: Insights into the target customer from target_customer.
    3. ##References: Links to articles, press releases, or other sources.

    Input variables:
    - company_name: {company_name}
    - company_data: {company_data}
    - product_name: {product_name}
    - product_category: {product_category}
    - product_data: {product_data}
    - competitors_data: {competitors_data}
    - target_customer: {target_customer}
    - optional: {optional}

    """
# prompt template
prompt_template = ChatPromptTemplate([('system',prompt)])
# chain
chain = prompt_template | llm | parser


with st.form("product_research", clear_on_submit=True):
    company_name = st.text_input("Enter your company name")
    company_website = st.text_input("Enter your company website")
    product_name = st.text_input("Enter your product name")
    product_category = st.text_input("Enter your product category")
    competitors = st.text_area("Enter your competitors")
    target_customer = st.text_input("Enter your target customer")
    optional = st.text_area("optional")
    submit_button = st.form_submit_button(label='Submit')
    insights = ""
    if submit_button:
        if company_name and product_name:
            with st.spinner("Analyzing the data..."):
                if company_website:
                    company_data = search.invoke(company_website)
                else:
                    company_data = f"Company: {company_name}"
                product_data = f"Product: {product_name}, Category: {product_category}"
                competitors_data = competitors
                target_customer = target_customer
                optional = optional
                insights = chain.invoke({'company_name': company_name, 'company_data': company_data, 'product_name': product_name, 'product_category': product_category, 'product_data': product_data, 'competitors_data': competitors_data, 'target_customer': target_customer, 'optional': optional})

if insights:
    st.markdown("### Product Insights")
    st.markdown(insights)
