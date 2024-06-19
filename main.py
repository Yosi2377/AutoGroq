import streamlit as st
import requests
import os

# Function to get the Cohere API key
def get_api_key():
    if 'api_key' in st.session_state and st.session_state.api_key:
        return st.session_state.api_key
    elif "COHERE_API_KEY" in os.environ:
        return os.environ["COHERE_API_KEY"]
    else:
        return None

# Function to display the API key input field
def display_api_key_input():
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ''
    
    api_key = st.text_input("Enter your Cohere API Key:", type="password", value=st.session_state.api_key, key="api_key_input")
    
    if api_key:
        st.session_state.api_key = api_key
        st.success("API key entered successfully.")
    return api_key

# Function to make a request to the Cohere API
def get_cohere_response(prompt, api_key):
    url = "https://api.cohere.ai/generate"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "xlarge",
        "prompt": prompt,
        "max_tokens": 150,
        "temperature": 0.75
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get('generations')[0].get('text')
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

# Main function to set up the Streamlit application
def main():
    st.set_page_config(page_title="ChatGPT-like App with Cohere", page_icon="🤖", layout="wide")
    
    st.markdown("""
        <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
        }
        .sidebar .sidebar-content {
            background-color: #ffffff !important;
            padding: 20px !important;
            border-radius: 5px !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        }
        .sidebar .st-emotion-cache-k7vsyb h1 {
            font-size: 12px !important;
            font-weight: bold !important;
            color: #007bff !important;
        }
        .sidebar h2 {
            font-size: 16px !important;
            color: #666666 !important;
        }
        .sidebar .stButton button {
            display: block !important;
            width: 100% !important;
            padding: 10px !important;
            background-color: #007bff !important;
            color: #ffffff !important;
            text-align: center !important;
            text-decoration: none !important;
            border-radius: 5px !important;
            transition: background-color 0.3s !important;
        }
        .sidebar .stButton button:hover {
            background-color: #0056b3 !important;
        }
        .sidebar a {
            display: block !important;
            color: #007bff !important;
            text-decoration: none !important;
        }
        .sidebar a:hover {
            text-decoration: underline !important;
        }
        .main .stTextInput input {
            width: 100% !important;
            padding: 10px !important;
            border: 1px solid #cccccc !important;
            border-radius: 5px !important;
        }
        .main .stTextArea textarea {
            width: 100% !important;
            padding: 10px !important;
            border: 1px solid #cccccc !important;
            border-radius: 5px !important;
            resize: none !important;
        }
        .main .stButton button {
            padding: 10px 20px !important;
            background-color: #dc3545 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 5px !important;
            cursor: pointer !important;
            transition: background-color 0.3s !important;
        }
        .main .stButton button:hover {
            background-color: #c82333 !important;
        }
        .main h1 {
            font-size: 32px !important;
            font-weight: bold !important;
            color: #007bff !important;
        }
        .main .stSelectbox select {
            width: 100% !important;
            padding: 10px !important;
            border: 1px solid #cccccc !important;
            border-radius: 5px !important;
        }
        .main .stAlert {
            color: #dc3545 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("ChatGPT-like App with Cohere")
    
    api_key = get_api_key()
    if api_key is None:
        api_key = display_api_key_input()
        if api_key is None:
            st.warning("Please enter your Cohere API Key to use the app.")
            return
    
    user_input = st.text_area("Enter your message:", height=100)
    
    if st.button("Send"):
        if user_input:
            with st.spinner("Generating response..."):
                response = get_cohere_response(user_input, api_key)
                if response:
                    st.text_area("Response:", value=response, height=200)
        else:
            st.warning("Please enter a message to send.")

if __name__ == "__main__":
    main()

