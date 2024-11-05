import streamlit as st
import google.generativeai as genai
key="AIzaSyBRpjRT6-mtAmqo7A2rVhEqDa3dna-KNEg"
genai.configure(api_key=key)
model=genai.GenerativeModel('gemini-pro')

def main():
    st.set_page_config(page_title="Text Generator", page_icon=":robot:")
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>Text generator Generator🤖</h1>
            <h3>I can generate text  for you</h3>
           
        </div>
        """,
        unsafe_allow_html=True
    )
    text_input=st.text_area("Enter Your Query here")
    
    submit=st.button("Generate text")
    if submit:
        with st.spinner("generting sql query....."):
            template="""
            creating sql query for your text:'''
            {text_input}'''
            
            
            """
            formatted_template=template.format(text_input=text_input)
            st.write(formatted_template)
            response=model.generate_content(formatted_template)
            sql_query=response.text
            st.write(sql_query)

main()
