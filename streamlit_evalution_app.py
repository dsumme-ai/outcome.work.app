import streamlit as st
import openai
import os
from dotenv import load_dotenv
import pandas as pd
from PIL import Image
import io

# Load environment variables from .env file if present
load_dotenv()

# Access the environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

if api_key is None:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Function to validate the business idea using a custom GPT model
def validate_idea(idea, model="gpt-3.5-turbo-instruct"):
    response = client.completions.create(
        model=model,
        prompt=f"Validate the following business idea: {idea}",
        max_tokens=150,
        temperature=0
    )
    return response.choices[0].text.strip()

# Function to read the content of uploaded file
def read_file_content(uploaded_file):
    file_type = uploaded_file.type
    if file_type == "text/plain":
        content = uploaded_file.read().decode("utf-8")
    elif file_type == "text/csv":
        df = pd.read_csv(uploaded_file)
        content = df.to_string()
    elif file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(uploaded_file)
        content = df.to_string()
    elif "image" in file_type:
        image = Image.open(io.BytesIO(uploaded_file.read()))
        content = "Image uploaded successfully. Note: Image analysis is not yet supported."
    else:
        content = None
    return content

# Streamlit app layout
st.title("Outcome Work")
st.write("Validate your business idea, and move forward with confidence.")

# Option to upload a file
uploaded_file = st.file_uploader("Upload a file containing your business idea", type=["txt", "csv", "xlsx", "png", "jpg", "jpeg"])

# Text input for business idea
idea = st.text_area("Or, enter your business idea here")

# Validate the idea from file or text input
if st.button("Validate Idea"):
    if uploaded_file is not None:
        # Read the uploaded file content
        idea = read_file_content(uploaded_file)
    
    if idea:
        validation_result = validate_idea(idea)
        st.subheader("Validation Result")
        st.write(validation_result)
    else:
        st.error("Please enter a business idea or upload a file containing it.")
