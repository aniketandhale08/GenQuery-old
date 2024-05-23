import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    return model

def generate_sql_query(model, input_prompt):
    template = """
            Create a SQL query snippet using the below text:

            ```
            {text_input}
            ```  
            i just want a Sql query         
    """
    formatted_template = template.format(text_input=input_prompt)
    response = model.generate_content(formatted_template)
    sql_query = response.text.strip().lstrip("```sql").rstrip("```")
    return sql_query

def generate_expected_output(model, sql_query):
    expected_output = """
            What would be the expected response of this SQL query snippet:


            ```
            {sql_query}
            ```  
            Provide sample tabluer Response with No Explanation        
    """
    expected_output_formatted = expected_output.format(sql_query=sql_query)
    response = model.generate_content(expected_output_formatted)
    return response.text

def generate_explanation(model, sql_query):
    explanation = """
            Explain this sql Query:


            ```
            {sql_query}
            ```  
            Please provide with simplest of explanation:      
    """
    explanation_formatted = explanation.format(sql_query=sql_query)
    response = model.generate_content(explanation_formatted)
    return response.text

def main():
    model = configure()
    st.set_page_config(page_title="GenQuery", page_icon="robat:")

    st.markdown(
        """
        <div style="text-align:center;">
        <h1>GenQuery 🤖</h1>
        <h3>Your Personal SQL Query Assistant</h3>
        <p> Welcome to GenQuery! Our project is your personal SQL query assistant powered by Google's Generative AI tools. 
        With GenQuery, you can effortlessly generate SQL queries and receive detailed explanations, simplifying your data retrieval process!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    text_input = st.text_area("Type your desired query below to unlock the power of SQL Query Genie! 💬")

    submit = st.button("Generate SQL Query")

    if submit:
        with st.spinner("Generating SQL Query.."):
            sql_query = generate_sql_query(model, text_input)
            eoutput = generate_expected_output(model, sql_query)
            explanation = generate_explanation(model, sql_query)
            with st.container():
                st.success("Your SQL query has been successfully generated. Feel free to copy and paste it into your database management system to retrieve the requested records.")
                st.code(sql_query, language="sql")

                st.success("Expected output of this SQL Query")
                st.markdown(eoutput)

                st.success("Explanation of SQL Query")
                st.markdown(explanation)

if __name__ == "__main__":
    main()
