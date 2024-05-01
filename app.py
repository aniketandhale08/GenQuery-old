import streamlit as st
import google.generativeai as genai

def main():
    st.set_page_config(page_title="GenQuery", page_icon=":robot:")

    st.markdown(
        """
        <div style="text-align:center;">
        <h1>GenQuery 🤖</h1>
        <h3>Your Personal SQL Query Assistant</h3>
        <p> Welcome to GenQuery! Our project is your personal SQL query assistant powered by Google's Generative AI tools. With GenQuery, you can effortlessly generate SQL queries and receive detailed explanations, simplifying your data retrieval process!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    text_input = st.text_area("Type your desired query below to unlock the power of SQL Query Genie! 💬")

    submit = st.button("Generate SQL Query")

    if submit:
        with st.spinner("Generating SQL Query.."):
            # Retrieve the API key from Streamlit Secrets
            GOOGLE_API_KEY = st.secrets["google_api"]["api_key"]
            
            # Configure the Generative AI model with the API key
            genai.configure(api_key=GOOGLE_API_KEY)
            model = genai.GenerativeModel("gemini-pro")

            # Generate SQL query
            template = """
                    Create a SQL query snippet using the below text:

                    ```
                    {text_input}
                    ```  
                    i just want a Sql query         
            """
            formatted_template = template.format(text_input=text_input)
            response = model.generate_content(formatted_template)
            sql_query = response.text.strip().lstrip("```sql").rstrip("```")

            # Generate expected output
            expected_output = """
                    What would be the expected response of this SQL query snippet:

                    ```
                    {sql_query}
                    ```  
                    Provide sample tabluer Response with No Explanation        
            """
            expected_output_formatted = expected_output.format(sql_query=sql_query)
            eoutput = model.generate_content(expected_output_formatted)
            eoutput = eoutput.text

            # Generate explanation
            explanation = """
                    Explain this SQL Query:

                    ```
                    {sql_query}
                    ```  
                    Please provide with simplest of explanation:      
            """
            explanation_formatted = explanation.format(sql_query=sql_query)
            explanation = model.generate_content(explanation_formatted)
            explanation = explanation.text
            
            # Display results
            with st.container():
                st.success("Your SQL query has been successfully generated. Feel free to copy and paste it into your database management system to retrieve the requested records.")
                st.code(sql_query, language="sql")

                st.success("Expected output of this SQL Query")
                st.markdown(eoutput)

                st.success("Explanation of SQL Query")
                st.markdown(explanation)

if __name__ == "__main__":
    main()
