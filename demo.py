from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
api_key=os.getenv("GOOGLE_API_KEY")
def call_google_genai(api_key,prompt):
    model=genai.GenerativeModel("gemini-1.5-pro")
    response=model.generate_content([prompt])
    return response.text


st.set_page_config(
        page_title="Gemini AI Generator",
)

# # Text area for user input
# input_text = st.text_area("Enter your ABAP or SAP ECC code here:")

# Sidebar radio buttons for different actions
st.sidebar.title("Actions")
action = st.sidebar.radio(
    "Choose an action:",
    ("Snowflake","PostgreSQL", "SAP S/4 HANA")
)

# Text area for user input
input_text = st.text_area("Enter your code:")

# Button to run the conversion/explanation
if st.sidebar.button("Run"):
    if not api_key:
        st.error("API key is missing. Please set your API key as an environment variable.")
    else:
        if action == "Snowflake":
            prompt = f"Convert the following Powerbi code to Tableau code:\n\n{input_text}"
            result = call_google_genai(api_key, prompt)
            st.write(result)