import requests
import streamlit as st

# get list of models
url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
    "Content-Type": "application/json"
}

models = [model['id'] for model in requests.get(url, headers=headers).json()['data'] if model['context_window'] == 8192 and model['active'] == True] 
