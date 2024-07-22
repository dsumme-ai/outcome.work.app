import streamlit as st
import openai
import pandas as pd
from PIL import Image
# import io

# Set up the OpenAI API key
openai.api_key = 'your_openai_api_key'  # Replace with your actual OpenAI API key

# Function to validate the business idea using OpenAI API
def validate_idea(idea):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Validate the following business idea: {idea}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Function to read the content of uploaded file
def read_file_content(uploaded_file):
    if uploaded_file.type == "text/plain":
        content = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
        content = df.to_string()
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(uploaded_file)
        content = df.to_string()
    elif "image" in uploaded_file.type:
        image = Image.open(uploaded_file)
        content = "Image uploaded successfully."
    else:
        content = None
    return content

# Streamlit app layout
st.title("Business Idea Validator")
st.write("Enter your business idea below, or upload a file containing your idea (text, CSV, Excel, image), and we'll validate it using OpenAI's GPT-3 model.")

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

# Run the Streamlit app (this line is for local execution)
# if __name__ == "__main__":
#     st.run()
