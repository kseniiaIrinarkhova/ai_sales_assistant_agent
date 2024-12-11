# Import libraries
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.chains import LLMChain, SequentialChain
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
main_prompt = """
    You are a helpful AI Sales assistant. Your job is to analyze the provided data to generate insights. Focus on company strategy, competitor analysis, and leadership info and using optional information if provided. 
    Provide reports based on provided structure:

    1. ## Company Strategy: Insights into the company/'s activities and priorities from company_data.
    2. ## Competitor Mentions: Mentions of competitors from competitors_data.
    2.1 ### Competitor Analysis: Insights into competitors from competitors_data.
    2.2 ### Competitor Comparison: Comparison of the company with competitors from competitors_data.
    3. ## Leadership Information: Relevant leaders and their roles.
    4. ## Product/Strategy Summary: Insights from product_data.
    5. ## Target Market: Proc and cons of launching the product into a target market from target_market.
    3. ##References: Links to articles, press releases, or other sources.

    Create an email template to target_customer from company Leadership based on report. Emphasize the benefits of the product and the company's strengths. Include optional information if provided.

    Input variables:
    - company_name: {company_name}
    - company_data: {company_data}
    - product_name: {product_name}
    - product_category: {product_category}
    - product_data: {product_data}
    - competitors_data: {competitors_data}
    - target_market: {target_market}
    - target_customer: {target_customer}
    - optional: {optional}

    """
# prompt template
# main_prompt_template = ChatPromptTemplate([('system',main_prompt)])
main_prompt_template = ChatPromptTemplate.from_template(main_prompt)



product_prompt = """
    You are a helpful AI assistant. 
    Your job is to analyse provided {company_data} and find information about {product_name}. 
    Include information about {product_category} and {product_description} if provided. 
    If you can not find information about product, return its name and category.
"""
product_prompt_template = PromptTemplate.from_template(template=  product_prompt)
# product_chain = LLMChain(llm = llm,
#                          prompt = product_prompt_template,
#                          output_key = 'product_data')

product_chain =  product_prompt_template | llm | parser

# analysis_chain = LLMChain(llm = llm,
#                          prompt = main_prompt_template,
#                          output_key = 'insights')
analysis_chain = main_prompt_template | llm | parser
# chain
# chain = main_prompt_template | llm | parser
# full_chain = SequentialChain(
#     chains = [product_chain, analysis_chain],
#     input_variables = ['company_name', 'company_data', 'product_name', 'product_category', 'product_description',  'competitors_data', 'target_customer', 'target_market', 'optional'],
#     output_variables = ['product_data', 'insights']
#     )

with st.form("product_research", clear_on_submit=True):
    product_name = st.text_input("Product")
    product_category = st.text_input("Product Category")
    product_description = st.text_area("Product Description")
    company_name = st.text_input("Company Name")
    company_website = st.text_input("Company Website")    
    competitors = st.text_area("Competitors")
    target_market = st.text_input("Target Market")
    target_customer = st.text_input("Target Customer Name")
    optional = st.text_area("Optional")
    submit_button = st.form_submit_button(label='Submit')
    insights = ""
    if submit_button:
        if company_name and product_name:
            with st.spinner("Analyzing the data..."):
                if company_website:
                    company_data = search.invoke(company_website)

                else:
                    company_data = f"Company: {company_name}"
                # product_data = f"Product: {product_name}, Category: {product_category}"
                product_data = product_chain.invoke({'company_data': company_data, 'product_name': product_name, 'product_category': product_category, 'product_description':product_description})
                competitors_data = competitors
                # target_customer = target_customer
                # optional = optional

                # insights = chain.invoke({'company_name': company_name, 'company_data': company_data, 'product_name': product_name, 'product_category': product_category, 'product_data': product_data, 'competitors_data': competitors_data, 'target_customer': target_customer,'target_market': target_market,'optional': optional})
                # insights = full_chain({'company_name': company_name, 'company_data': company_data, 'product_name': product_name, 'product_category': product_category, 'product_description':product_description, 'competitors_data': competitors_data, 'target_customer': target_customer,'target_market': target_market,'optional': optional})
                insights = analysis_chain.invoke({'company_name': company_name, 'company_data': company_data, 'product_name': product_name, 'product_category': product_category, 'product_data':product_data, 'competitors_data': competitors_data, 'target_customer': target_customer,'target_market': target_market,'optional': optional})

if insights:
    st.markdown("### Product Data")
    st.markdown(product_data)
    st.markdown("### Product Insights")
    st.markdown(insights)
