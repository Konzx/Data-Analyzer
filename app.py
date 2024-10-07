from dotenv import load_dotenv
import os
import io
import pandas as pd  # For handling Excel files
import google.generativeai as genai
import streamlit as st

# Load environment variables
load_dotenv()

# Configure API key
genai.configure(api_key=st.secrets["API_KEY"])

# Define functions
def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([prompt])
    return response.text

def process_excel(uploaded_file):
    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error processing Excel file: {e}")
        return None



# Streamlit UI
st.set_page_config(page_title="Data Insights Expert")
st.header("Supreme Data Insights")

uploaded_file = st.file_uploader("Upload your Excel dataset (XLSX)...", type=["csv"])

if uploaded_file is not None:
    st.success("Excel file uploaded successfully!")
    df = process_excel(uploaded_file)
    
    if df is not None:
        st.subheader("Dataset Preview")
        st.dataframe(df.head())  # Show first few rows of the dataset
        
        # Generate a dataset summary (basic description)
        summary = df.describe(include='all').to_string()
        # Define prompts for insights
        input_prompt1 = """
        You are a data analyst. Please provide a detailed analysis of the following dataset. 
        Highlight key trends, patterns, and any anomalies you observe. Suggest actionable insights based on the data.
        """

        input_prompt2 = """
        You are a data scientist specializing in predictive analytics. Based on the following dataset, 
        identify potential factors that could influence the target variable and suggest possible predictive models.
        """

        input_prompt3 = """
        You are an expert in data visualization. Recommend the most effective types of charts or graphs to represent the insights 
        derived from the following dataset. Explain why these visualizations are suitable.
        """

        # Buttons for different insights
        submit1 = st.button("Provide Detailed Analysis")
        submit2 = st.button("Identify Predictive Factors")
        submit3 = st.button("Recommend Visualizations")

        if submit1:
            prompt = input_prompt1 + f"\n\nDataset Summary:\n{summary}"
            response = get_gemini_response(prompt)
            st.subheader("Detailed Analysis")
            st.write(response)

        if submit2:
            prompt = input_prompt2 + f"\n\nDataset Summary:\n{summary}"
            response = get_gemini_response(prompt)
            st.subheader("Predictive Factors and Models")
            st.write(response)

        if submit3:
            prompt = input_prompt3 + f"\n\nDataset Summary:\n{summary}"
            response = get_gemini_response(prompt)
            st.subheader("Recommended Visualizations")
            st.write(response)

else:
    st.info("Awaiting for an Excel file to be uploaded.")
