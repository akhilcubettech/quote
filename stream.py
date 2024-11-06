import os
import time
import boto3
import streamlit as st
from agent.workflow_manager import WorkflowManager
import pandas as pd


agent= WorkflowManager()

def process_text_input(req: str):
    res = agent.run_text(req)
    return res['items']


def process_file_upload(file):
    textract_client = boto3.client('textract', region_name=os.getenv("AWS_REGION"))
    response = textract_client.detect_document_text(Document={'Bytes': file.read()})
    extracted_text = []
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            extracted_text.append(item['Text'])
    req = "\n".join(extracted_text)
    res = agent.run_text(req)
    return res['items']


st.title("Quote Generator")

with st.container():
    col1, col2 = st.columns(2)


    with col1:
        st.header("Text Input")
        requirements = st.text_area("Enter requirements here", height=100)
        text_button_pressed = st.button("Process Text Input")


    with col2:
        st.header("File Upload")
        uploaded_file = st.file_uploader("Upload a file with requirements", type=["pdf", "jpg", "jpeg"])
        file_button_pressed = st.button("Process Uploaded File")

results_container = st.container()

with results_container:
    if text_button_pressed and requirements:
        with st.spinner("Processing text input..."):
            results = process_text_input(requirements)
            st.success("Text input processed successfully!")


            df = pd.DataFrame(results)


            total_value = df["sub_total"].sum()


            st.subheader("Quotation Summary")
            st.table(df.style.format({
                "product_price": "{:.2f}",
                "sub_total": "{:.2f}"
            }))
            st.markdown(f"**TOTAL: ₹{total_value:.2f}**")

    elif file_button_pressed and uploaded_file:
        with st.spinner("Processing uploaded file..."):
            results = process_file_upload(uploaded_file)
            st.success("File uploaded and processed successfully!")
            df = pd.DataFrame(results)

            total_value = df["sub_total"].sum()

            st.subheader("Quotation Summary")
            st.table(df.style.format({
                "product_price": "{:.2f}",
                "sub_total": "{:.2f}"
            }))
            st.markdown(f"**TOTAL: ₹{total_value:.2f}**")

    elif text_button_pressed and not requirements:
        st.warning("Please enter some requirements to process.")
    elif file_button_pressed and not uploaded_file:
        st.warning("Please upload a file to process.")