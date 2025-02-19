import os
import re
import logging
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai
from app.models import InputData, Campaign, Email

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

def generate_prompt(account, email_index):
    """
    Generate a prompt for Gemini API based on account data.
    """
    pain_points = ", ".join(account.pain_points)
    campaign_goals = {
        "nurturing": "nurture the lead and educate them about your product/service",
        "upselling": "upsell your product or service",
        "awareness": "raise awareness about your offerings"
    }
    campaign_goal = campaign_goals.get(account.campaign_objective, "engage potential clients")

    return f"""
    You are a marketing expert specializing in the software industry. Write email {email_index} of a {account.campaign_objective} campaign for {account.account_name}, a software company facing {pain_points}.
    
    Target: {account.contacts[0].name}, {account.contacts[0].job_title} at {account.account_name}
    Goal: {campaign_goal}
    
    Body:
    - Brief introduction and problem acknowledgment
    - How your product/service helps solve {pain_points}
    - Provide value-driven insight
    - Donot make anything bold in the content.
    - The company name which is sending the mail is VKDeveloper. and the person name is Vansh Kashyap. Also dont provide any suggestion in [] instead apply the suggestions and provide a proper meaningfull final email
    
    Call to action:
    - Encourage scheduling a demo or a free consultation
    
    Sign-off: Thank the recipient and provide contact information.
    """

async def call_gemini(prompt):
    """
    Generate text using Gemini API asynchronously.
    """
    try:
        chat_session = model.start_chat(history=[])
        response = await asyncio.to_thread(chat_session.send_message, prompt)
        generated_text = response.text if response else ""
        logging.debug(f"Generated Text: {generated_text}")
        return clean_and_parse_response(generated_text)
    except Exception as e:
        logging.error(f"Error generating text with Gemini: {str(e)}")
        return {}

def clean_and_parse_response(generated_text):
    """
    Extract structured content from the Gemini response.
    """
    subject_match = re.search(r"Subject:\s*(.*?)\n", generated_text, re.DOTALL)
    call_to_action_match = re.search(r"(?:Call to action:|CTA:)\s*(.*?)\n", generated_text, re.DOTALL)
    
    subject = subject_match.group(1).strip() if subject_match else "No Subject"
    body = re.sub(r"Subject:.*?\n", "", generated_text, flags=re.DOTALL).strip()
    body = re.sub(r"\[.*?\]", "", body)  # Remove placeholder suggestions
    body = re.sub(r"\n|\t", " ", body).strip()
    body = re.sub(r"[*]", "", body)  # Remove asterisks for bold formatting
    body = re.sub(r"\/", "", body)  # Remove slashes
    body = re.sub(r"VKDeveloper", "VKDeveloper", body)  # Fix company name
    call_to_action = call_to_action_match.group(1).strip() if call_to_action_match and call_to_action_match.group(1).strip() else "Schedule a demo or free consultation."
    
    logging.debug(f"Parsed Email -> Subject: {subject}, CTA: {call_to_action}")
    return {"subject": subject, "body": body, "call_to_action": call_to_action} if subject and body else {}

async def generate_email_campaign(data: InputData):
    """
    Generate email campaigns using Gemini API.
    """
    campaigns = []
    for account in data.accounts:
        emails = []
        for i in range(data.number_of_emails):
            prompt = generate_prompt(account, i + 1)
            response = await call_gemini(prompt)
            
            if response:
                emails.append(Email(
                    subject=response["subject"],
                    body=response["body"],
                    call_to_action=response["call_to_action"]
                ))
            else:
                logging.warning(f"Skipping email {i+1} for {account.account_name} due to empty response.")
        
        if emails:
            campaigns.append(Campaign(account_name=account.account_name, emails=emails))
    
    return campaigns
