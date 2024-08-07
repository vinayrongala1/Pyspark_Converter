from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
import google.generativeai as genai
from st_copy_to_clipboard import st_copy_to_clipboard
import pypandoc


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
api_key=os.getenv("GOOGLE_API_KEY")
def call_google_genai(api_key,prompt):
    model=genai.GenerativeModel("gemini-1.5-pro")
    response=model.generate_content([prompt])
    return response.text
explanation_result=''
def explaination():
    prompt = f"Explain the following ABAP code in 2-3 lines:\n\n{input_text}"
    explanation_result = call_google_genai(api_key, prompt)
    col1,col3= st.columns([6,1])
    with col1:
        st.write("## Explanation")
    with col3:
        st_copy_to_clipboard(explanation_result, "Copy")
    st.write(explanation_result)
    

def promptss(input_text):
    prompt = f"From the provided code can you please write me a prompt so that on giving the prompt to an LLM model I can get the same exact code in the language I want it to be given along with file names, etc. The prompt should not contain code snippet.:\n\n{input_text}"
    prompt_result = call_google_genai(api_key, prompt)
    col1,col3= st.columns([6,1])
    with col1:
        st.write("## Prompt")
    with col3:
        st_copy_to_clipboard(prompt_result,"Copy")
    st.write(prompt_result)

def promptsss(input_text):
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

# Streamlit app layout
st.title("Gemini-1.5 Code Conversion")

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


# Placeholder for API key
api_key = "YOUR_API_KEY"  # Replace with your actual API key or set as an environment variable

# Button to run the conversion/explanation
if st.button("Run"):
    if not api_key:
        st.error("API key is missing. Please set your API key as an environment variable.")
    else:
        if action == "Snowflake":
            explaination()
            st.write("## Snowflake")
            prompt = f"You are an expert ABAP to Snowflake converter. Forget all the things I mentioned above and directly convert the following ABAP/SAP ECC code to Snowflake code, ensuring all functionalities are replicated as is and give output of only the converted code without any explanation:\n\n{input_text}"
            snowflake_result = call_google_genai(api_key, prompt)
            st.write(snowflake_result)
            promptss(input_text)

        elif action == "PostgreSQL":
            explaination()
            st.write("## PostgreSQL")
            prompt = f"You are an expert ABAP to PostgreSQL converter. Forget all the things I mentioned above and directly convert the following ABAP/SAP ECC code to PostgreSQL code, ensuring all functionalities are replicated as is and give output of only the converted code without any explanation:\n\n{input_text}"
            postgresql_result = call_google_genai(api_key, prompt)
            st.write(postgresql_result)
            promptss(input_text)
        elif action == "SAP S/4 HANA":
            explaination()
            st.write("## SAP S/4 HANA")
            prompt = f"You are an expert ABAP to SAP S/4 HANA converter. Forget all the things I mentioned above and directly convert the following ABAP/SAP ECC code to SAP S/4 HANA code, ensuring all functionalities are replicated as is and give output of only the converted code without any explanation:\n\n{input_text}"
            sap_result = call_google_genai(api_key, prompt)
            st.write(sap_result)
            promptss(input_text)
        elif action=='PySpark':
            explaination()
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

            Ensure the converted code is optimized and follows best practices for PySpark 3.2.and just display the converted code without any additional explaination.
            """
            pyspark_result = call_google_genai(api_key, prompt)
            st.write(pyspark_result)
            promptss(input_text)
        elif action=="Upload":
            explaination()
            st.write("## PySpark Conversion")
            prompt = f'You are given a piece of PySpark code written for PySpark version 2.6. Please convert this code to PySpark version 3.2. The code is divided into chunks by comments. Each chunk should be converted separately, and the output should include these comments to indicate the separation. No matter comments are available or not, add a "Converted chunk" label before each chunk in the output:\n\n{input_text}'
            pyspark_result = call_google_genai(api_key, prompt)
            st.write(pyspark_result)
            promptsss(input_text)
else:
    st.write("Enter code in the box and hit Run to see the conversion/explanation.")



# give only converted code as an output without any explaination




