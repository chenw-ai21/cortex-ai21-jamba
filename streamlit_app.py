import streamlit as st 
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.session import Session
import snowflake.connector
import pandas as pd

conn = st.connection("snowflake")
session = conn.session()

pd.set_option("max_colwidth",None)

def doc_select(form, company, date):
    doc_sql = """
    SELECT VALUE FROM SEC_FILINGS WHERE FORM_TYPE = (?) AND COMPANY_NAME = (?) AND PERIOD_END_DATE = (?)
    """
    doc = session.sql(doc_sql, params = [form, company, date]).collect()
    doc = str(doc)
    return doc

def complete(prompt):    
    cmd = f"""
             SELECT SNOWFLAKE.CORTEX.COMPLETE('jamba-instruct', ?) as response
           """
    
    response = session.sql(cmd, params=[prompt]).collect()
    return response[0].RESPONSE

def summarize(form, company, date):
    doc = doc_select(form, company, date)
    prompt = 'You are an expert of financial market. Summarize top 3 key takeaways of the following SEC filing document for a financial analyst in bullet points: ' + doc

    res_text = complete(prompt)
    return res_text

def qna(question, form, company, date):
    doc = doc_select(form, company, date)
    prompt = 'You are an expert of financial market. Answer the following question, based on the following SEC filing document. Question: ' + question + ' Please answer the question only based on information from the following SEC filling document: ' + doc
    
    res_text = complete(prompt)
    return res_text

def extract(entity, form, company, date):
    doc = doc_select(form, company, date)
    prompt = 'You are an expert of financial market. Here is the SEC filing document we should use: ' + doc + 'Extract ' + entity + ', based on the provide document above. The answer should be complete with value and units.'
    
    res_text = complete(prompt)
    return res_text

#Main code

primary_color = "#f4bab4"
hover_color="#D70040"
secondary_color = "#dddddd"
secondary_hover_color="#aaaaaa"
custom_css = f"""
<style>
    .stButton > button {{
        border: 2px solid {primary_color};
        border-radius: 20px;
        color: black;
        background-color: {primary_color};
    }}
    .stButton > button:hover {{
        border: 2px solid {hover_color};
        color: black;
        background-color: {hover_color};
    }}
    .stButton > button.download {{
        border: 2px solid {secondary_color};
        border-radius: 20px;
        color: white;
        background-color: {secondary_color};
    }}
    .stButton > button.download:hover {{
        border: 2px solid {secondary_hover_color};
        color: white;
        background-color: {secondary_hover_color};
    }}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
st.image("https://upload.wikimedia.org/wikipedia/commons/e/e5/AI21-Labs-Logo.jpg")


st.title("SEC filings Analytics with Jamba")

#Here you can choose what LLM to use. Please note that they will have different cost & performance
company = st.sidebar.selectbox('Select company:',(
    'SNOWFLAKE INC.', 'TESLA, INC.', 'NVIDIA CORP', 'INTERNATIONAL BUSINESS MACHINES CORP', 'MICROSOFT CORP', 'APPLE INC', 'ALLBIRDS, INC.'))

form = st.sidebar.selectbox('Select form type:',(
    '10-K', '10-Q', '8-K'))

with st.sidebar:
    selectbox_sql = """
        SELECT PERIOD_END_DATE
        FROM SEC_FILINGS WHERE FORM_TYPE = (?) AND COMPANY_NAME = (?)
        ORDER BY PERIOD_END_DATE DESC
        """
    #COLLECT THE DATA VALUES INTO A DF
    selectbox_df = session.sql(selectbox_sql, params=[form, company])
    date = st.sidebar.selectbox('Select doc:', selectbox_df)

st.header('1. Summarize SEC filings', divider='rainbow')

if st.button('Summarize'): 
    st.session_state['summary'] = summarize(form, company, date)
    st.text_area("Summary:", st.session_state['summary'], key='text1', height=300)

st.header('2. Q&A with SEC filings', divider='rainbow')
st.write("""
Some example questions to ask about SEC filings:
- How has the company revenue and profit changed over the years?
- How has the company market share in its primary industries changed?
- What major acquisitions has the company engaged in?
- What are actions taken by the company about sustainability?
- What are the main business risks for the company?
- What are the key financial metrics of the company?
""")
st.write("""Your question:""")
question = st.text_input("Enter question", placeholder="Did the company have a cybersecurity incident based on the following SEC filing document?", label_visibility="collapsed")

if st.button('Answer'):
    answer = qna(question, form, company, date)
    st.text_area("Answer:", answer, height=300)

st.header('3. Information retrieval from SEC filings', divider='rainbow')
entity = st.text_input("Entity:", placeholder="revenue")
if st.button('Extract'):
    info = extract(entity, form, company, date)
    st.text_area("Result:", info, height=20)


