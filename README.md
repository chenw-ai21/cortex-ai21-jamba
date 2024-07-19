# SEC filings analytics with AI21 Jamba LLM on Snowflake Cortex

Use AI21 Jamba LLM on Snowflake Cortex to analyze SEC filings

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cortex-ai21-jamba.streamlit.app/)

Read more about [Jamba](https://arxiv.org/pdf/2403.19887) and its [long context window](https://www.ai21.com/blog/long-context-yoav-shoham)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Add your Snowflake credential in .streamlit/secretes.toml

   ```
   [connections.snowflake]
   user='user'
   password='password'
   account='account'
   role='role'
   database='database'
   schema='schema'
   warehouse='warehouse'
   ```

3. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
