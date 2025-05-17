# GHOSTED SURVEY RESPONSE PIPELINE

This project is a live, automated psychological analysis pipeline built to cope.

## 🧠 What It Does

- Monitors a Google Form/Sheet for new responses
- Uses GPT-4o to send gaslight-heavy mental health diagnoses to ghosters via email
- Sends ego-padding emotional support texts to ghostee via Twilio
- Logs each processed row in the Google Sheet so nothing re-sends on restart

## 📋 Google Survey Questions

SURVEY TITLE:
Ghosted Survey

SURVEY DESCRIPTION:
If you’re receiving this form, then that means at some point while evaluating {NAME} as a romantic partner, you made the decision to ghost him. We'd like to know why. Please fill out this survey to the best of your ability.

Upon completion of this survey, you will be eligible to enroll for a chance to win one (1) FREE $10 Starbucks gift card. Each survey submission grants the participating party one (1) entry to the $10 Starbucks gift card sweepstakes - drawing to take place September 30th, 2028.

PLEASE READ: {link to OFFICIAL GHOSTED STARBUCKS SWEEPSTAKES PARTICIPATION TERMS AND CONDITIONS}.

SECTION 1

1. What is your age?
2. What is your ethnicity?
3. What is the highest level of education you have received?
4. Why did you ghost {NAME}? (Select all that apply)
5. If "Other" was included in your selected answers to the above question, please elaborate and provide additional details:
6. Would you like to add an additional comment?

SECTION 2 (if opted to leave additional comment): Additional Comments

1. You've opted-in to leave an additional comment! Please include your additional notes or comments below:

SECTION 3: FREE AI-Generated Mental Health Diagnosis

1. Would you like to receive a FREE AI-generated mental health diagnosis based on your answers to this survey?

SECTION 4 (if opted for a FREE AI-generated mental health diagnosis): Contact Information for FREE AI-Generated Mental Health Diagnosis

1. Email Address:

SECTION 5: Thank you for completing this survey!

1. Please submit your answers by clicking "Submit" below.
   NOTE: By submitting this survey, you agree to the {link to OFFICIAL GHOSTED STARBUCKS SWEEPSTAKES PARTICIPATION TERMS AND CONDITIONS}.

## 🧠 FLOW DIAGRAM

📩 **Google Form Submission**
⬇️  
📊 **Google Sheet Populated**
⬇️  
🧼 **Script Checks for Rows Without "Yes" in "Response Sent?"**
⬇️  
🤖 **OpenAI GPT-4o #1**  
🩻 _Generates gaslight-heavy faux clinical diagnosis_  
 ⬇️  
📧 **Email Sent to Ghoster**  
 ⬇️  
✅ **"Yes" Written to Google Sheet (Column K)**  
 ⬇️  
📲 **Twilio Text #1**  
🔔 _"NEW GHOSTED SURVEY RESPONSE SUBMISSION"_  
 ⬇️  
🤖 **OpenAI GPT-4o #2**  
👼 _Generates a self-validating ego massage for user_  
 ⬇️  
📲 **Twilio Text #2**  
🧃 _Emotionally manipulative AI-generated praise reminding you that you are blameless_

🛑 **Loop Waits 10 Seconds Then Repeats**

## ⚙️ HOW TO RUN

```bash
pip install -r requirements.txt
export $(cat .env | xargs)
python ghosted.py
```
