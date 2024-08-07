from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from st_copy_to_clipboard import st_copy_to_clipboard
import pypandoc

# Ensure pandoc is installed
try:
    pypandoc.get_pandoc_version()
except OSError:
    # If pandoc is not installed, download it
    pypandoc.download_pandoc()

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
api_key = os.getenv("GOOGLE_API_KEY")

def call_google_genai(api_key, prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([prompt])
    return response.text

def explaination(input_text):
    prompt = f"Explain the following ABAP code in 2-3 lines:\n\n{input_text}"
    explanation_result = call_google_genai(api_key, prompt)
    col1, col3 = st.columns([6, 1])
    with col1:
        st.write("## Explanation")
    with col3:
        st_copy_to_clipboard(explanation_result, "Copy")
    st.write(explanation_result)

def promptss(input_text):
    prompt = f"From the provided code can you please write me a prompt so that on giving the prompt to an LLM model I can get the same exact code in the language I want it to be given along with file names, etc. The prompt should not contain code snippet or any code directly. The code is divided into chunks by comments. Provide detailed prompt for each chunk seperately, and the output should include these comments to indicate the separation. No matter comments are available or not, add a 'Converted prompt' label before each prompt in the output:\n\n{input_text}"
    prompt_result = call_google_genai(api_key, prompt)
    col1, col3 = st.columns([6, 1])
    with col1:
        st.write("## Prompt")
    with col3:
        st_copy_to_clipboard(prompt_result, "Copy")
    st.write(prompt_result)

def read_file(file, file_type):
    if file_type == "rtf":
        return pypandoc.convert_text(file.getvalue().decode(), 'plain', format='rtf')
    elif file_type == "docx":
        return pypandoc.convert_text(file.getvalue(), 'plain', format='docx')
    else:
        return ""

st.set_page_config(
    page_title="Gemini-1.5 AI Generator",
)

st.title("Gemini-1.5 Code Conversion")

st.sidebar.title("Actions")
st.sidebar.markdown(
    """
    <style>
    div[data-testid="stSidebar"] {
        min-width: 200px;
        max-width: 200px;
    }
    .stButton button {
        width: 20%;
    }
    .sidebar-content {
        font-size: 1.2em;
    }
    </style>
    """,
    unsafe_allow_html=True
)
action = st.sidebar.radio(
    "Choose an action:",
    ("Snowflake", "PostgreSQL", "SAP S/4 HANA", 'PySpark'),
    key='radio_buttons'
)

uploaded_file = st.file_uploader("Upload your RTF or Word file here", type=["rtf", "docx"])

input_text = ""
if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1]
    input_text = read_file(uploaded_file, file_type)

if input_text:
    if action == 'Snowflake':
        st.write("### Snowflake with Code Explanation")
    elif action == 'PostgreSQL':
        st.write("### PostgreSQL with Code Explanation")
    elif action == 'SAP S/4 HANA':
        st.write("### SAP S/4 HANA with Code Explanation")
    elif action == 'PySpark':
        st.write("### PySpark with Code Explanation")

if st.button("Run"):
    if not api_key:
        st.error("API key is missing. Please set your API key as an environment variable.")
    else:
        if action == "Snowflake":
            explaination(input_text)
            st.write("## Snowflake")
            prompt = f"You are an expert ABAP to Snowflake converter. Forget all the things I mentioned above and directly convert the following ABAP/SAP ECC code to Snowflake code, ensuring all functionalities are replicated as is and give output of only the converted code without any explanation:\n\n{input_text}"
            snowflake_result = call_google_genai(api_key, prompt)
            st.write(snowflake_result)
            promptss(input_text)

        elif action == "PostgreSQL":
            explaination(input_text)
            st.write("## PostgreSQL")
            prompt = f"You are an expert ABAP to PostgreSQL converter. Forget all the things I mentioned above and directly convert the following ABAP/SAP ECC code to PostgreSQL code, ensuring all functionalities are replicated as is and give output of only the converted code without any explanation:\n\n{input_text}"
            postgresql_result = call_google_genai(api_key, prompt)
            st.write(postgresql_result)
            promptss(input_text)
        elif action == "SAP S/4 HANA":
            explaination(input_text)
            st.write("## SAP S/4 HANA")
            prompt = f"You are an expert ABAP to SAP S/4 HANA converter. Forget all the things I mentioned above and directly convert the following ABAP/SAP ECC code to SAP S/4 HANA code, ensuring all functionalities are replicated as is and give output of only the converted code without any explanation:\n\n{input_text}"
            sap_result = call_google_genai(api_key, prompt)
            st.write(sap_result)
            promptss(input_text)
        elif action == 'PySpark':
            explaination(input_text)
            st.write("## PySpark Conversion")
            prompt = f'You are given a piece of PySpark code written for PySpark version 2.6. Please convert this code to PySpark version 3.2. The code is divided into chunks by comments. Each chunk should be converted separately, and the output should include these comments to indicate the separation. No matter comments are available or not, add a "Converted chunk" label before each chunk in the output:\n\n{input_text}'
            pyspark_result = call_google_genai(api_key, prompt)
            st.write(pyspark_result)
            promptss(input_text)
else:
    st.write("Upload an RTF or Word file and hit Run to see the conversion/explanation.")
