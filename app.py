# Import libraries
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools import TavilySearchResults
from models import models
import re

# set default states
if 'default_model' not in st.session_state:
    st.session_state['default_model'] = 'llama3-8b-8192'\

if 'temperature' not in st.session_state:
    st.session_state['temperature'] = 0.5

# Model and Agent Tools
llm = ChatGroq(
    api_key=st.secrets['GROQ_API_KEY'],
    model=st.session_state['default_model'],
    temperature=st.session_state['temperature']
    )
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
# prompts
#prompt for sales analysis
analysis_prompt = """
    You are a helpful AI Sales assistant. Your job is to analyze the provided data to generate insights. Focus on company strategy, competitor analysis, and leadership info and using optional information if provided. 
    Create a report based on provided structure:
    # Product report
    1. ## Company Strategy: Insights into the company/'s activities and priorities from company_data.
    2. ## Competitor Mentions: Mentions of competitors from competitors_data.
    2.1 ### Competitor Analysis: Insights into competitors from competitors_data.
    2.2 ### Competitor Comparison: Comparison of the company with competitors from competitors_data using value_proposition if they provided as main advantages.
    3. ## Leadership Information: Relevant leaders and their roles.
    4. ## Product/Strategy Summary: Insights from product_data.
    5. ## Target Market: Proc and cons of launching the product into a target market from target_market.
    3. ##References: Links to articles, press releases, or other sources.

    # Email template
    Based on report, create an email template to target_customer. Emphasize the benefits of the product and the company's strengths. Include optional information if provided. 
    Sing the imail with the name of company CEO if it was mentioned in Leadership Information from report.

    Input variables:
    - company_name: {company_name}
    - company_data: {company_data}
    - product_name: {product_name}
    - product_category: {product_category}
    - product_data: {product_data}
    - value_proposition: {value_proposition}
    - competitors_data: {competitors_data}
    - target_market: {target_market}
    - target_customer: {target_customer}
    - optional: {optional}

    """

#prompt for product data creation
product_prompt = """
    You are a helpful AI assistant. 
    Your job is to analyse provided {company_data} and find information about {product_name}. 
    Include information about {product_category} and {value_proposition} if provided. 
    If you can not find information about product, return its name and category.
    """

# prompt templates

analysis_prompt_template = ChatPromptTemplate.from_template(analysis_prompt)
product_prompt_template = PromptTemplate.from_template(template=  product_prompt)

#chains

product_chain =  product_prompt_template | llm | parser
analysis_chain = analysis_prompt_template | llm | parser

# Main form
with st.form("product_research", clear_on_submit=True):
    # form fields
    product_name = st.text_input("Product")
    product_category = st.text_input("Product Category")
    value_proposition = st.text_area("Value Proposition")
    company_name = st.text_input("Company Name")
    company_website = st.text_input("Company Website")    
    competitors = st.text_area("Competitors")
    target_market = st.text_input("Target Market")
    target_customer = st.text_input("Target Customer Name")
    optional = st.text_area("Optional")
    submit_button = st.form_submit_button(label='Submit')

    # Output data
    insights = ""
    product_data = ""
    note =""

    # Check if the form is submitted
    if submit_button:
        if company_name and product_name:
            with st.spinner("Analyzing the data..."):
                if company_website:
                    if company_website.startswith('http'):
                        company_data = search.invoke(company_website)
                    else:
                        company_data = f"Company: {company_name}"
                        st.warning(f'Could not find data for company website: **{company_website}**. Analysis would be provided based on input data')
                else:
                    company_data = f"Company: {company_name}"
                # getting product data
                product_data = product_chain.invoke({'company_data': company_data, 'product_name': product_name, 'product_category': product_category, 'value_proposition':value_proposition})
                # getting competitors data
                competitors_list = list(filter(lambda competitor: competitor.startswith('http'),re.split(r"[ ,\n]\s*", competitors)))
                # get all data about competitors based on web sites
                competitors_data = " ".join([f"{competitor}: {search.invoke(competitor)[0]['content']}" for competitor in competitors_list])
                # getting insights
                insights = analysis_chain.invoke({'company_name': company_name, 'company_data': company_data, 'product_name': product_name, 'product_category': product_category, 'product_data':product_data, 'value_proposition':value_proposition, 'competitors_data': competitors_data, 'target_customer': target_customer,'target_market': target_market,'optional': optional})
        else:
            st.error('Please provide the company name and product name')


if product_data:
    st.markdown("### Product Data")
    st.markdown(product_data)

if insights:
    st.markdown("### Product Insights")
    st.markdown(insights)
