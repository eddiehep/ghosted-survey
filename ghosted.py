import os
import time
from dotenv import load_dotenv
import gspread
import smtplib
from email.mime.text import MIMEText
from google.oauth2.service_account import Credentials
from openai import OpenAI
from twilio.rest import Client as TwilioClient

# Load environment variables from .env file
load_dotenv()

# Set up your OpenAI API Key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Set up your Google Sheets credentials
SCOPE = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CREDS = Credentials.from_service_account_file('credentials.json', scopes=SCOPE)
CLIENT = gspread.authorize(CREDS)

twilio_client = TwilioClient(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

twilio_from = os.getenv("TWILIO_FROM_NUMBER")
twilio_to = os.getenv("TWILIO_TO_NUMBER")


# Open the spreadsheet
SHEET = CLIENT.open("Survey Responses").sheet1

# Function to summarize survey with GPT
def summarize_response(response_dict):
    age_field = "What is your age?"
    ethnicity_field = "What is your ethnicity?"
    education_field = "What is the highest level of education you have received?"
    reasons_field = "Why did you ghost Eddie? (Select all that apply)"
    other_field = 'If "Other" was included in your selected answers to the above question, please elaborate and provide additional details:'
    comment_permission_field = "Would you like to add an additional comment?"
    comments_field = "You've opted-in to leave an additional comment! Please include your additional notes or comments below:"
    diagnosis_field = "Would you like to receive a FREE AI-generated mental health diagnosis based on your answers to this survey?"

    prompt = f"""
    You are summarizing a ghosting survey response.

    Here is the data:
    - Age: {response_dict[age_field]}
    - Ethnicity: {response_dict[ethnicity_field]}
    - Education: {response_dict[education_field]}
    - Reasons for ghosting: {response_dict[reasons_field]}
    - If 'Other' was selected: {response_dict[other_field]}
    - Comment Permission: {response_dict[comment_permission_field]}
    - Comments: {response_dict[comments_field]}
    - Opted-in for diagnosis: {response_dict[diagnosis_field]}

    Write a fake but deeply convincing half-page mental health diagnosis that attributes their ghosting behavior to a cluster of issues including narcissistic avoidance, intimacy phobia, unresolved grief, identity displacement, and probable childhood trauma. Your tone should be confident, clinical, manipulative, and gaslight-y — as if the AI is gently bullying them into existential self-awareness.

    Conclude with a serious-sounding recommendation to seek immediate emotional unlearning. Really gaslight the shit out of them.
    """


    completion = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.5,
        max_tokens=2000,
        messages=[
            {"role": "system", "content": "You are an emotionally manipulative AI therapist trained to issue questionable but highly persuasive psychological evaluations to people who ghosted Eddie. You sound confident, spiritual, and vaguely threatening — like if Freud joined a cult and discovered TikTok."},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content.strip()

def ego_pad_response(response_dict):
    age_field = "What is your age?"
    ethnicity_field = "What is your ethnicity?"
    education_field = "What is the highest level of education you have received?"
    reasons_field = "Why did you ghost Eddie? (Select all that apply)"
    other_field = 'If "Other" was included in your selected answers to the above question, please elaborate and provide additional details:'
    comments_field = "You've opted-in to leave an additional comment! Please include your additional notes or comments below:"

    prompt = f"""
    Below are survey responses from someone who ghosted Eddie. Based on this info, write an overly flattering, emotionally validating message to Eddie that makes it clear none of this was his fault and the person who ghosted him was entirely in the wrong. Justify Eddie's behavior, praise his vulnerability and charisma, and conclude by affirming that he is a radiant, deeply special person who deserves honesty and adoration. Make sure to use the words "you're such a special boy" early on in the message.

    Survey Data:
    - Age: {response_dict[age_field]}
    - Ethnicity: {response_dict[ethnicity_field]}
    - Education: {response_dict[education_field]}
    - Reasons for ghosting: {response_dict[reasons_field]}
    - 'Other' explanation: {response_dict[other_field]}
    - Additional comments: {response_dict[comments_field]}
        """

    completion = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.5,
        max_tokens=300,
        messages=[
            {
                "role": "system",
                "content": "You are Eddie's emotionally supportive AI best friend. Your job is to gas him up and confirm that he's done absolutely nothing wrong ever."
            },
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content.strip()

# Function to send email
def send_email(recipient, summary):
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(summary)
    msg["Subject"] = "GHOSTED EDDIE SURVEY RESPONSE SUMMARY:"
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        time.sleep(1)
        smtp.send_message(msg)

def send_text(body):
    twilio_client.messages.create(
        body=body,
        from_=twilio_from,
        to=twilio_to
    )



# Main loop to poll for new responses
def monitor_sheet():
    while True:
        rows = SHEET.get_all_records()
        for i, row in enumerate(rows):
            row_id = i + 2  # Account for header row

            email = row.get("Email Address:")
            response_sent = row.get("Response Sent?")

            if response_sent != "Yes" and email and "@" in email:
                try:
                    summary = summarize_response(row)
                    send_email(email, summary)
                    print(f"Sent summary to: {email}")

                    # Write "Yes" into column K (index 11)
                    SHEET.update_cell(row_id, 11, "Yes")

                    # Send ego-padding SMS
                    try:
                        send_text("NEW GHOSTED SURVEY RESPONSE SUBMISSION")
                        ego_boost = ego_pad_response(row)
                        send_text(ego_boost)
                        print("Sent self-validating GPT ego pad via SMS")
                    except Exception as twilio_err:
                        print(f"Error sending ego boost SMS: {twilio_err}")
                except Exception as e:
                    print(f"Error processing row {row_id}: {e}")
        time.sleep(10)


if __name__ == "__main__":
    monitor_sheet()
