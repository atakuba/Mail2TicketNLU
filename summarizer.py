import os
from dotenv import load_dotenv
load_dotenv()  

from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  

import pandas as pd
import re
from datetime import datetime


# Load the OpenAI API key securely from .env
load_dotenv()
print("✅ Key found:", os.getenv("OPENAI_API_KEY") is not None)

def extract_date_time_flexible(text):
    pattern = r"(Sent|Date):\s*\w+,\s*(\w+\s+\d{1,2},\s+\d{4})\s+(?:at\s+)?(\d{1,2}:\d{2})\s*([APMapm]{2})"
    match = re.search(pattern, text)
    if match:
        _, date_str, time_str, ampm = match.groups()
        full_datetime = f"{date_str} {time_str} {ampm.upper()}"
        try:
            return datetime.strptime(full_datetime, "%B %d, %Y %I:%M %p")
        except ValueError:
            return None
    return None

def ai_generate_subject_and_summary(body_text):
    prompt = f"""
You are an assistant summarizing customer support emails.

Given the email content below, extract and generate the following:

1. A concise **Subject** that summarizes the main issue.
2. A detailed **Body Summary** that includes:
   - Who experienced the issue and what it was about
   - Any relevant steps taken (e.g., if they met over Zoom, mention it)
   - How the issue was resolved
3. A professional and easy-to-read tone throughout.
4. A clear **Description** of the issue.
5. A concise **Short Description** summarizing the issue in 1–2 lines.

Format your response like this:

Subject: ...
Summary: ...
Description: ...
Short Description: ...

Email content:
{body_text}
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional email summarizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=500
    )

    content = response.choices[0].message.content

    # Use regex to extract all four parts
    subject_match = re.search(r"Subject:\s*(.*)", content)
    summary_match = re.search(r"Summary:\s*(.*?)(?:\n|$)", content, re.DOTALL)
    description_match = re.search(r"Description:\s*(.*?)(?:\n|$)", content, re.DOTALL)
    short_desc_match = re.search(r"Short Description:\s*(.*)", content)

    subject = subject_match.group(1).strip() if subject_match else "Support Request"
    summary = summary_match.group(1).strip() if summary_match else "Summary not available."
    description = description_match.group(1).strip() if description_match else "Description not available."
    short_description = short_desc_match.group(1).strip() if short_desc_match else "Short description not available."

    return subject, summary, description, short_description

def process_emails(input_csv_path):
    df = pd.read_csv(input_csv_path)
    updated_data = []

    for _, row in df.iterrows():
        body = row['Body']

        # Get all four fields from the AI function
        subject_generated, body_summary, description, short_description = ai_generate_subject_and_summary(body)

        # Extract date and time
        datetime_obj = extract_date_time_flexible(body)
        date_str = datetime_obj.strftime('%Y-%m-%d') if datetime_obj else ""
        time_str = datetime_obj.strftime('%H:%M') if datetime_obj else ""

        # Extract sender
        from_match = re.search(r"From:\s*(.*)", body)
        from_user = from_match.group(1).strip() if from_match else ""

        # Append updated row
        updated_data.append({
            "subject": subject_generated,
            "body": body_summary,
            "description": description,
            "short_description": short_description,
            "from": from_user,
            "to": "akubanychbek",
            "date": date_str,
            "time": time_str
        })

    # Create DataFrame and optionally rename columns for Excel
    final_df = pd.DataFrame(updated_data)

    final_df.rename(columns={
        "subject": "Subject",
        "body": "Body Summary",
        "description": "Description",
        "short_description": "Short Description",
        "from": "From",
        "to": "To",
        "date": "Date",
        "time": "Time"
    }, inplace=True)

    return final_df

