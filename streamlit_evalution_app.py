import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Access the environment variable for API key if needed
api_key = os.getenv('API_KEY')  # Replace 'API_KEY' with the actual key if needed

# Function to get evaluation from custom GPT endpoint
def get_evaluation(idea):
    url = "https://chatgpt.com/g/g-uN3d1mxV6-vc-evaluation-model"
    headers = {
        "Authorization": f"Bearer {api_key}"  # Replace with the required header if needed
    }
    data = {
        "model": "gpt-3.5-turbo-instruct",
        "prompt": f"Evaluate the following business idea: {idea}",
        "max_tokens": 150,
        "temperature": 0
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to get response from the API.")
        return None

# Function to format the results
def format_results(results):
    st.subheader("Evaluation Results")
    for section in results.get('sections', []):
        st.markdown(f"### {section['title']}")
        st.markdown(f"<h2 style='font-size:36px; color:blue;'>{section['score']}</h2>", unsafe_allow_html=True)
        st.write(section['content'])
        st.markdown("---")

# Streamlit app layout
st.title("Business Idea Evaluation")
st.write("Validate your business idea and get detailed feedback.")

# Text input for business idea
idea = st.text_area("Enter your business idea here")

# Validate the idea
if st.button("Evaluate Idea"):
    if idea:
        evaluation_results = get_evaluation(idea)
        if evaluation_results:
            format_results(evaluation_results)
    else:
        st.error("Please enter a business idea.")

# To run the Streamlit app, use the command:
# streamlit run app.py
