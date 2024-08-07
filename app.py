import streamlit as st
from dotenv import load_dotenv
import os
import openai
from st_copy_to_clipboard import st_copy_to_clipboard
import pypandoc
 
# Load environment variables
load_dotenv()
 
# Configuration for Azure OpenAI
deployment_name = "gpt-35-turbo-abb"
openai.api_type = "azure"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("API_BASE")
openai.api_version = "2023-09-15-preview"
 
def call_openai(prompt):
    response = openai.Completion.create(
        engine=deployment_name,
        prompt=prompt,
        temperature=0.7,
        max_tokens=500,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].text.strip()
 
def explanations():
    prompt = f"Explain the following ABAP code in 2-3 lines:\n\n{input_text}"
    result_explanation = call_openai(prompt)
    col1,col3= st.columns([6,1])
    with col1:
        st.write("## Explanation")
    with col3:
        st_copy_to_clipboard(result_explanation, "Copy")
    st.write(result_explanation)
 
def promptss():
    prompt = f"From the provided code, can you please write me a prompt so that on giving the prompt to LLM model, I can get the same exact code in the language I want it to be given along with file names etc. The prompt should not contain code snippets:\n\n{input_text}"
    result_prompt = call_openai(prompt)
    col1,col3= st.columns([6,1])
    with col1:
        st.write("## Prompt")
    with col3:
        st_copy_to_clipboard(result_prompt,"Copy")
    st.write(result_prompt)
 
st.set_page_config(
    page_title="GPT-4 Code Generator",
)
 
# Streamlit app layout
st.title("GPT-4 Code Generator")
 
def promptsss(input_text):
    prompt = f"From the provided code can you please write me a prompt so that on giving the prompt to an LLM model I can get the same exact code in the language I want it to be given along with file names, etc. The prompt should not contain code snippet or any code directly. The code is divided into chunks by comments. Provide detailed prompt for each chunk seperately, and the output should include these comments to indicate the separation. No matter comments are available or not, add a 'Converted prompt' label before each prompt in the output:\n\n{input_text}"
    prompt_result = call_openai(api_key, prompt)
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



# Sidebar radio buttons for different actions
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
    ("Snowflake", "PostgreSQL", "SAP S/4 HANA",'PySpark','Upload'),
    key='radio_buttons'
)

if action == 'Snowflake':
    st.write("### Snowflake with Code Explanation")
    # Text area for user input
    input_text = st.text_area("Enter your code here:")
elif action == 'PostgreSQL':
    st.write("### PostgreSQL with Code Explanation")
    # Text area for user input
    input_text = st.text_area("Enter your code here:")
elif action == 'SAP S/4 HANA':
    st.write("### SAP S/4 HANA with Code Explanation")
    # Text area for user input
    input_text = st.text_area("Enter your code here:")
elif action == 'PySpark':
    st.write("### PySpark with Code Explanation")
    # Text area for user input
    input_text = st.text_area("Enter your code here:")
elif action == 'Upload':
    uploaded_file = st.file_uploader("Upload your RTF or Word file here", type=["rtf", "docx"])
    input_text= ""
    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1]
        input_text= read_file(uploaded_file, file_type)
 
# Button to run the conversion/explanation
if st.button("Run"):
    if input_text.strip() == "":
        st.write("Please enter some text in the input area.")
    else:
        if action == "Snowflake":
            explanations()
            st.write("## Snowflake")
            prompt = f"You are an expert ABAP/SAP ECC to Snowflake converter.Convert the following ABAP/SAP ECC code to Snowflake code, ensuring all functionalities are replicated as is. Provide only the Snowflake code equivalent to the ABAP code. If no direct equivalent exists, provide the best possible replacement code in Snowflake. Do not include any explanations or extra code, only the code.\n\n{input_text}"
            result_snowflake = call_openai(prompt)
            st.code(result_snowflake, language='sql')
            promptss()

        elif action == "PostgreSQL":
            explanations()
            st.write("## PostgreSQL")
            prompt = f"You are an expert ABAP/SAP ECC to PostgreSQL converter.Convert the following ABAP/SAP ECC code to PostgreSQL code, ensuring all functionalities are replicated as is. Provide only the PostgreSQL code equivalent to the ABAP code. If no direct equivalent exists, provide the best possible replacement code in PostgreSQL. Do not include any explanations, only the code.\n\n{input_text}"
            result_postgresql = call_openai(prompt)
            st.code(result_postgresql, language='sql')
            promptss()
        elif action == "SAP S/4 HANA":
            explanations()
            st.write("## SAP S/4 HANA")
            prompt = f"You are an expert ABAP/SAP ECC to SAP S/4 HANA converter.Convert the following ABAP/SAP ECC code to SAP S/4 HANA code, ensuring all functionalities are replicated as is. Provide only the SAP S/4 HANA code equivalent to the ABAP code. If no direct equivalent exists, provide the best possible replacement code in SAP S/4 HANA. Do not include any explanations, only the code.\n\n{input_text}"
            result_s4hana = call_openai(prompt)
            st.code(result_s4hana, language='abap')
            promptss()
        elif action=='PySpark':
            explanations()
            st.write("## Pyspark Conversion")
            prompt = f"""
            I have a code written in PySpark 2.6, and I need it to be converted to PySpark 3.2 accurately without any errors and with 100% accuracy. Below is the PySpark 2.6 code:

            {input_text}

            Please convert this code to PySpark 3.2, ensuring that all functionalities remain the same and any deprecated functions are updated to their modern equivalents. Consider the following aspects:

            1. DataFrame and SQL API Enhancements: Update to use any new functions and methods available in PySpark 3.2.
            2. Pandas UDFs: Convert any UDFs to use the improved pandas UDFs where applicable.
            3. Structured Streaming: Update streaming code to leverage enhancements in PySpark 3.2.
            4. Machine Learning (MLlib): Ensure that all machine learning components are updated to their latest versions.
            5. Deprecations and Removals: Replace any deprecated functions with their recommended alternatives.
            6. Performance Improvements: Utilize any new performance features available in PySpark 3.2.
            7. Error Handling and Logging: Update error handling and logging to reflect improvements in PySpark 3.2.

            Ensure the converted code is optimized and follows best practices for PySpark 3.2.and make it compatible with Databricks.
            """
            result_pyspark = call_openai(prompt)
            st.code(result_pyspark, language='sql')
            promptss()
        elif action=="Upload":
            explanations()
            st.write("## PySpark Conversion")
            prompt = f'You are given a piece of PySpark code written for PySpark version 2.6. Please convert this code to PySpark version 3.2. The code is divided into chunks by comments. Each chunk should be converted separately, and the output should include these comments to indicate the separation. No matter comments are available or not, add a "Converted chunk" label before each chunk in the output:\n\n{input_text}'
            pyspark_result = call_openai(prompt)
            st.write(pyspark_result)
            promptsss(input_text)
else:
    st.write("Enter text in the box and hit Run to see the conversion/explanation.")