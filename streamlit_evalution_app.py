import streamlit as st
from openai import OpenAI
import requests
import os
from dotenv import load_dotenv
import pandas as pd
from PIL import Image
import io

# Load environment variables from .env file if present
load_dotenv()

# Access the environment variable
api_key = os.getenv('OPENAI_API_KEY')

if api_key is None:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Function to get evaluation from custom GPT endpoint
def get_evaluation(idea):
    url = "https://chatgpt.com/g/g-uN3d1mxV6-vc-evaluation-model"
    headers = {
        "Authorization": f"Bearer {api_key}",  # Replace with the required header if needed
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo-instruct",
        "prompt": f"Evaluate the following business idea: {idea}",
        "max_tokens": 150,
        "temperature": 0
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Error occurred: {req_err}")
    except ValueError as json_err:
        st.error(f"JSON
