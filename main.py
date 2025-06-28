from summarizer import process_emails

df = process_emails("/Users/akubanychbek/Desktop/MY_WORKSPACE/ticket_project/1test_tickets.csv")
df.to_excel("summarized_output.xlsx", index=False)
print("✅ Email summarization complete. Output saved as summarized_output.xlsx.")
