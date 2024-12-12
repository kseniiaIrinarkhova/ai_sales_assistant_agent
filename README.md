# Sales Assistant Agent

# Distinctiveness and Complexity
Streamlit based AI sales assistant. Created using **Python**, **Streamlit**, **Groq**, **LangChain**, and **PyPDF2**.
Deployed project : [ai-sales-assistant-agent](https://ai-sales-assistant-agent.streamlit.app/)

# Technical documentation of the project
## Files structure in :
- **app.py** - main program
- **requirements.txt** - list of libs
- **.streamlit/secrets.toml.example** - example of sectrets settings
- **models.py** - helper for getting models from Groq API

## Installation

1. Copy repository.
2. Create Python Environment (venv) in VS Code. 
3. Register in [Groq.com](https://console.groq.com/) and create an API key
4. Register in [Tavily.com](https://tavily.com/) and create an API key
5. Rename **secrets.toml.example** to **secrets.toml**
6. Save your API keys in **secrets.toml**
7. Install the packages: `pip install -r requiements.txt`
8. Run the app: `streamlit run app.py`

# User Guide
User could choose  temperature of AI model responces and one of the models provided by Groq API on the side bar of application.

After that, user should provide **Product Name** and **Company Name** for analysis. These are obligatory fields. 
To get more pricies analysis and all additional information user can provide these information:
- Product category
- Product description. There are 3 types of sources for description:
   1. Product description URL
   2. Text area for product description
   3. Grag and frop field to upload PDF file with product description
- Value Preposition
- Company website
- Competitors. User could provide as many competitors' URL links as they want. If user provide only name of competitor - assistant would not analyse it.
- Target market
- Target Customer Name - would be used as recipient of email
- any additional information in "Optional" field

Next user should push "Generate analysis" button to receive information from assistant.
User get 2 types of information:
- product data
- product insights
- email draft
Each information user could download as .TXT file.

# Author
Project prepared as a capstone project for **AI Prompt Engineering** course at *Per Scholas* by [Kseniia Irinarkhova](https://www.linkedin.com/in/kseniia-irinarkhova/).