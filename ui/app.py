import streamlit as st
import pandas as pd
import os
import sys

# Ensure access to root project modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.summarizer import process_emails
from utils.tech_list import get_tech_support_names

st.set_page_config(page_title="Email to Ticket Summarizer", layout="centered")
st.title("📬 Email to Ticket Summarizer")

# Dropdown to select tech user
tech_list = get_tech_support_names()
selected_tech = st.selectbox("Select your name (Tech Support):", tech_list)

# File uploader
uploaded_file = st.file_uploader("Upload Email CSV File", type=["csv"])

# Initialize session state
if "processed" not in st.session_state:
    st.session_state["processed"] = False
    st.session_state["output_path"] = ""

# Process file when button clicked
if uploaded_file and selected_tech:
    if st.button("🚀 Process Emails"):
        with st.spinner("Processing and summarizing..."):
            try:
                df = process_emails(uploaded_file)

                os.makedirs("excels", exist_ok=True)
                filename = f"summarized_output_{selected_tech.replace(' ', '_')}.xlsx"
                output_path = os.path.join("excels", filename)

                df.to_excel(output_path, index=False)

                st.session_state["processed"] = True
                st.session_state["output_path"] = output_path

                st.success("✅ Summarization complete!")

            except Exception as e:
                st.error(f"❌ Failed to process file: {e}")

# Show download + automation button if processed
if st.session_state["processed"]:
    with open(st.session_state["output_path"], "rb") as f:
        st.download_button("📥 Download Excel", data=f, file_name=os.path.basename(st.session_state["output_path"]))

    # Placeholder for future automation step
    if st.button("🤖 Run Automation"):
        st.info("🛠️ Automation will be implemented in the next stage.")
