from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from st_copy_to_clipboard import st_copy_to_clipboard
 
# Load environment variables
load_dotenv()
 
# Configure API key for generative AI
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
 
# Function to call generative AI model
def call_google_genai(api_key, prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([prompt])
    return response.text
 
# Function to display explanations and prompts
def explanations(input_text):
    prompt_explanation = f"Explain the following ABAP code in 2-3 lines:\n\n{input_text}"
    result_explanation = call_google_genai(api_key, prompt_explanation)
    # st.write("## Explanation")
    # st.write(result_explanation)
    
    return result_explanation
 
def promptss(input_text):
    prompt_prompt = f"From the provided code, can you please write a prompt so that on giving the prompt to LLM model, I can get the same exact code in the language I want, along with file names, etc. The prompt should not contain code snippets:\n\n{input_text}"
    result_prompt = call_google_genai(api_key, prompt_prompt)
    # st.write("## Prompt")
    # st.write(result_prompt)
    
    return result_prompt
 
# Set page configuration
st.set_page_config(
    page_title="Gemini AI Generator",
)
 
# Initialize session state
if 'explanation' not in st.session_state:
    st.session_state['explanation'] = ""
if 'prompt' not in st.session_state:
    st.session_state['prompt'] = ""
if 'conversion' not in st.session_state:
    st.session_state['conversion'] = ""
 
# Streamlit app layout
st.title("Gemini Code Conversion")
 
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
        width: 15%;
    }
    .sidebar-content {
        font-size: 1.2em;
    }
    /* Increase font size for radio buttons */
    .css-18ni7ap .css-qrbaxs {
        font-size: 1.2em;
    }
    .css-1lcbmhc {
        font-size: 1.2em;
    }
    </style>
    """,
    unsafe_allow_html=True
)
action = st.sidebar.radio(
    "Choose an action:",
    ("Snowflake", "PostgreSQL", "SAP S/4 HANA")
)
 
# Text area for user input
input_text = st.text_area("Enter your ABAP or SAP ECC code here:")
 
# Button to run the conversion/explanation
if st.button("Run"):
    if not api_key:
        st.error("API key is missing. Please set your API key as an environment variable.")
    else:
        if action == "Snowflake":
            st.session_state['explanation'] = explanations(input_text)
            # st.write("## Snowflake")
            prompt_snowflake = f"You are an expert ABAP to Snowflake converter. Forget all the things I mentioned above and directly convert the following ABAP/SAP ECC code to Snowflake code, and give only the code equivalent of the provided code. If there is no code equivalent, provide code with which we can replace the provided code in Snowflake without any explanation:\n\n{input_text}"
            st.session_state['conversion'] = call_google_genai(api_key, prompt_snowflake)
            # st.write(st.session_state['conversion'])
            
            st.session_state['prompt'] = promptss(input_text)
 
        elif action == "PostgreSQL":
            st.session_state['explanation'] = explanations(input_text)
            st.write("## PostgreSQL")
            prompt_postgresql = f"You are an expert ABAP to PostgreSQL converter. Forget all the things I mentioned above and directly convert the following ABAP/SAP ECC code to PostgreSQL code, and output only the converted code without any explanation:\n\n{input_text}"
            st.session_state['conversion'] = call_google_genai(api_key, prompt_postgresql)
            st.write(st.session_state['conversion'])
            st_copy_to_clipboard(st.session_state['conversion'], "Copy PostgreSQL Code")
            st.session_state['prompt'] = promptss(input_text)
 
        elif action == "SAP S/4 HANA":
            st.session_state['explanation'] = explanations(input_text)
            st.write("## SAP S/4 HANA")
            prompt_s4hana = f"You are an expert ABAP to SAP S/4 HANA converter. Forget all the things I mentioned above and directly convert the following ABAP/SAP ECC code to SAP S/4 HANA code, and output only the converted code without any explanation:\n\n{input_text}"
            st.session_state['conversion'] = call_google_genai(api_key, prompt_s4hana)
            st.write(st.session_state['conversion'])
            st_copy_to_clipboard(st.session_state['conversion'], "Copy SAP S/4 HANA Code")
            st.session_state['prompt'] = promptss(input_text)
 
# Display previous outputs if available
if st.session_state['explanation']:
    st.write("## Explanation")
    st.write(st.session_state['explanation'])
    st_copy_to_clipboard(st.session_state['explanation'], "Copy")

if st.session_state['conversion']:
    st.write("## Snowflake Code")
    st.write(st.session_state['conversion'])
    st_copy_to_clipboard(st.session_state['conversion'], "Copy Snowflake Code")
 
if st.session_state['prompt']:
    st.write("## Prompt")
    st.write(st.session_state['prompt'])
    st_copy_to_clipboard(st.session_state['prompt'], "Copy")
 

 
# Chatbot functionality
st.write("## Chatbot")

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_question' not in st.session_state:
    st.session_state.user_input = ""

st.markdown("<div class='main-container'>", unsafe_allow_html=True)

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for sender, message in st.session_state.messages:
    if sender == "User":
        st.markdown(f"<div class='user-message'>{message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-message'>{message}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)


user_input = st.text_input("Ask your questions or share your doubts about the code:")
send_button = st.button("Send ➡️")




 





if send_button and user_input:
    st.session_state.messages.append(("User", user_input))
    context = (
            f"User's code input:\n{input_text}\n\n"
            f"Explanation:\n{st.session_state['explanation']}\n\n"
            f"Prompt:\n{st.session_state['prompt']}\n\n"
            f"Conversion:\n{st.session_state['conversion']}\n\n"
            f"User's question:\n{user_input}"
        )
        # Call the generative AI model to get the response
    response = call_google_genai(api_key, context)

    st.session_state.messages.append(("Bot", response))
    st.session_state.user_question = ""
    st.experimental_rerun()

st.markdown("""
    <style>
    .chat-input {
        flex: 1;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
        background-color: #f8d7da; /* Red background for input */
    }
    .send-button {
        padding: 10px 20px;
        border: none;
        background-color: #007bff;
        color: white;
        border-radius: 5px;
        cursor: pointer;
        margin-left: 10px;
    }
    .send-button:hover {
        background-color: #0056b3;
    }
    .user-message {
        background-color: #f8d7da;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        text-align: right;
        word-break: break-word;
        max-width: fit-content;
        float: right;
        clear: both;
    }
    .bot-message {
        background-color: #d4edda;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        word-break: break-word;
        max-width: fit-content;
        float: left;
        clear: both;
    }
    </style>
    """, unsafe_allow_html=True)
