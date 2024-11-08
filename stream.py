import os
import time
import boto3
import streamlit as st
from agent.workflow_manager import WorkflowManager
import pandas as pd
import openai as client
import base64

agent= WorkflowManager()

def process_text_input(req: str):
    res = agent.run_text(req)
    return res


def process_file_upload(file):
    base64_image = base64.b64encode(file.read()).decode('utf-8')
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract the requirements in the image, output only the list of requirements",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
    )

    res = agent.run_text(response.choices[0].message.content)
    return res


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
            df = pd.DataFrame(results['items'],
                              columns=["product_id", "product_name", "product_price", "quantity", "sub_total"])



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
            df = pd.DataFrame(results['items'], columns=["product_id", "product_name", "product_price", "quantity", "sub_total"])
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