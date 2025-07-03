import streamlit as st
import pandas as pd
import os
import sys
import subprocess
from datetime import datetime

# Ensure access to root project modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.summarizer import process_emails

st.set_page_config(page_title="Email to Ticket Summarizer", layout="centered")
st.title("📬 Email to Ticket Summarizer")

# File uploader
uploaded_file = st.file_uploader("Upload Email CSV File", type=["csv"])

# Initialize session state
if "processed" not in st.session_state:
    st.session_state["processed"] = False
    st.session_state["output_path"] = ""

# Process file when button clicked
if uploaded_file:
    if st.button("🚀 Process Emails"):
        with st.spinner("Processing and summarizing..."):
            try:
                # Process emails
                df = process_emails(uploaded_file)

                # Save summarized Excel file with timestamp
                os.makedirs("excels", exist_ok=True)
                timestamp = datetime.now().strftime("%B_%d")  # e.g., July_03
                filename = f"summarized_output_{timestamp}.xlsx"
                output_path = os.path.join("excels", filename)

                df.to_excel(output_path, index=False)

                # Store in session state
                st.session_state["processed"] = True
                st.session_state["output_path"] = output_path

                st.success("✅ Summarization complete!")

            except Exception as e:
                st.error(f"❌ Failed to process file: {e}")

# Show download + automation button if processed
if st.session_state["processed"]:
    with open(st.session_state["output_path"], "rb") as f:
        st.download_button("📥 Download Excel", data=f, file_name=os.path.basename(st.session_state["output_path"]))

    if st.button("🤖 Run Automation"):
        with st.spinner("Running automation..."):
            try:
                result = subprocess.run(
                    ["python3", "-m", "behave", "automation/features/"],
                    env={**os.environ, "PYTHONPATH": "."},
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    st.success("🎉 Automation completed successfully!")
                else:
                    st.error("❌ Automation failed. See logs below.")
                    st.code(result.stdout + "\n" + result.stderr)

            except Exception as e:
                st.error(f"❌ Error running automation: {e}")
