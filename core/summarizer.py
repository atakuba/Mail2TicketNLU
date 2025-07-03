import os
import re
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

1. A concise **Subject** summarizing the main issue.
2. A professional, detailed **Body Summary** that includes:
   - Who experienced the issue and what it was
   - Any relevant steps taken (e.g., Zoom meeting, password reset, system check)
   - How it was resolved (mention if the user confirmed resolution)
3. A clear **Description** of the issue (DO NOT mention resolution).
4. A very concise **Short Description** summarizing the issue in 10–12 words (NO resolution details).
5. The **User Email** of the person who received help (try to get @nl.edu or @my.nl.edu emails if possible).
6. The correct **Business Service (BS)** and **Category** based on this list:

Choose the closest match based on context:

- **Hardware / Software Support**  
  - Computer  
  - Virus/Malware

- **Help Desk**  
  - Drop Call  
  - General Inquiry

- **Accounts and Access**  
  - Email  
  - Portal  
  - LMS (Learning Management System)

- **Student Services**  
  - Admissions  
  - Financial Aid  
  - Bursar/Student Accounts

7. Ensure a clear, professional, and easy-to-read tone.

Format your response exactly like this:

Subject: ...
Summary: ...
Description: ...
Short Description: ...
Business Service: ...
Category: ...

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
        max_tokens=600
    )

    content = response.choices[0].message.content

    # Extract fields using regex
    subject = re.search(r"Subject:\s*(.*)", content)
    summary = re.search(r"Summary:\s*(.*?)(?:\n[A-Z][a-z]+|$)", content, re.DOTALL)
    description = re.search(r"Description:\s*(.*?)(?:\n[A-Z][a-z]+|$)", content, re.DOTALL)
    short_desc = re.search(r"Short Description:\s*(.*)", content)
    user_email = re.search(r"User Email:\s*(.*)", content)
    business_service = re.search(r"Business Service:\s*(.*)", content)
    category = re.search(r"Category:\s*(.*)", content)

    # Clean and fallback
    subject = subject.group(1).strip() if subject else "Support Request"
    summary = summary.group(1).strip() if summary else "Summary not available."
    description = description.group(1).strip() if description else "Description not available."
    short_description = short_desc.group(1).strip() if short_desc else "Short description not available."
    user_email_text = user_email.group(1).strip() if user_email else ""
    business_service = business_service.group(1).strip() if business_service else "Not available"
    category = category.group(1).strip() if category else "Not available"

   

    return subject, summary, description, short_description, user_email_text, business_service, category

def process_emails(input_csv_path):
    df = pd.read_csv(input_csv_path)
    updated_data = []

    for _, row in df.iterrows():
        body = row['Body']

        # Get all fields from AI
        subject_generated, body_summary, description, short_description, user_email, bs, category = ai_generate_subject_and_summary(body)

        # Extract date and time
        # datetime_obj = extract_date_time_flexible(body)
        # date_str = datetime_obj.strftime('%Y-%m-%d') if datetime_obj else ""
        # time_str = datetime_obj.strftime('%H:%M') if datetime_obj else ""

        updated_data.append({
            "subject": subject_generated,
            "body": body_summary,
            "description": description,
            "short_description": short_description,
            # "user_first_name": first_name,
            # "user_last_name": last_name,
            "user_email": user_email,
            "business_service": bs,
            "category": category,
            # "to": "akubanychbek",
            # "date": date_str,
            # "time": time_str
        })

    final_df = pd.DataFrame(updated_data)
    final_df.rename(columns={
        "subject": "Subject",
        "body": "Body Summary",
        "description": "Description",
        "short_description": "Short Description",
        # "user_first_name": "User First Name",
        # "user_last_name": "User Last Name",
        "user_email": "User Email",
        "business_service": "Business Service",
        "category": "Category",
        # "to": "To",
        # "date": "Date",
        # "time": "Time"
    }, inplace=True)

    return final_df
