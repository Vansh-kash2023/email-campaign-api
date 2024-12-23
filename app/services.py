import os
import re
from dotenv import load_dotenv
import google.generativeai as genai
from app.models import InputData, Campaign, Email
import logging
import asyncio

# Load environment variables from the .env file
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Configure the Gemini API using the API key from the environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set the generation configuration for Gemini API
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

def generate_prompt(account, email_index):
    """
    Generate a prompt for Gemini API based on account data.
    """
    # Prepare pain points for the email content
    pain_points = ", ".join(account.pain_points)

    # Adjust the prompt based on the campaign objective
    if account.campaign_objective == "nurturing":
        campaign_goal = "nurture the lead and educate them about the benefits of your product/service"
    elif account.campaign_objective == "upselling":
        campaign_goal = "upsell your product or service"
    else:
        campaign_goal = "raise awareness about your offerings"

    return f"""
    You are a marketing expert specializing in the software industry. Write email {email_index} of a {account.campaign_objective} drip campaign for {account.account_name}, a software company facing challenges with {pain_points}.

    * Target audience: {account.contacts[0].name}, {account.contacts[0].job_title} of {account.account_name}
    * Goal: {campaign_goal}
    
    *Body:* 
    * Briefly introduce yourself and your company.
    * Acknowledge the common challenges faced by software companies like {pain_points}.
    * Explain how your product/service can help {account.account_name} address these challenges with specific examples.
    * Use a positive and confident tone, highlighting the value proposition of your offering.

    *Call to action:* 
    * Include a clear call to action, such as scheduling a demo or requesting a free consultation, to learn more about how your product/service can benefit {account.account_name}.

    *Sign-off:* 
    Thank {account.contacts[0].name} for their time and consideration. Include your contact information.

    The tone should be professional, friendly, and personalized.
    """

async def call_gemini(prompt):
    """
    Generate text using the Gemini API.
    """
    try:
        # Start a chat session with Gemini
        chat_session = model.start_chat(history=[])

        # Send the generated prompt to Gemini and get the response
        response = chat_session.send_message(prompt)

        # Extract the generated text from the response
        generated_text = response.text
        logging.debug(f"Generated Text: {generated_text}")

        # Clean up and parse the response
        return clean_and_parse_response(generated_text)

    except Exception as e:
        logging.error(f"Error generating text with Gemini: {str(e)}")
        return {}

def clean_and_parse_response(generated_text):
    """
    Clean up and parse the response from Gemini API.
    """
    # Regular expressions to capture sections
    subject_regex = r"Subject:\s*(.*?)(?=\n|$)"
    body_regex = r"Body:\s*(.*?)(?=Call to action:|$)"
    call_to_action_regex = r"Call to action:\s*(.*?)(?=\n|$)"

    # Extract subject, body, and call to action using regex
    subject = re.search(subject_regex, generated_text, re.DOTALL)
    body = re.search(body_regex, generated_text, re.DOTALL)
    call_to_action = re.search(call_to_action_regex, generated_text, re.DOTALL)

    # Clean up the extracted content (strip unnecessary whitespace or explanation text)
    subject_text = subject.group(1).strip() if subject else ""
    body_text = body.group(1).strip() if body else ""
    call_to_action_text = call_to_action.group(1).strip() if call_to_action else ""

    # Log the cleaned sections for debugging
    logging.debug(f"Cleaned Subject: {subject_text}")
    logging.debug(f"Cleaned Body: {body_text}")
    logging.debug(f"Cleaned Call to Action: {call_to_action_text}")

    # Check if the email has valid content
    if not subject_text or not body_text or not call_to_action_text:
        logging.warning("One of the sections is empty. Skipping this email.")
        return {}

    # Return structured response
    return {
        "subject": subject_text,
        "body": body_text,
        "call_to_action": call_to_action_text
    }

async def generate_email_campaign(data: InputData):
    """
    Generate email campaigns using Gemini API.
    """
    campaigns = []

    # Loop through each account to generate emails
    for account in data.accounts:
        emails = []

        for i in range(data.number_of_emails):
            # Generate the prompt for each email
            prompt = generate_prompt(account, i + 1)
            response = await call_gemini(prompt)

            # Check for valid response
            if response:
                finish_reason = response.get("finish_reason")
                if finish_reason == "RECITATION":
                    logging.warning(f"Email {i+1} for {account.account_name} was a recitation, skipping.")
                    continue

                subject = response.get("subject")
                body = response.get("body")
                call_to_action = response.get("call_to_action")

                # Check if the necessary fields are populated
                if subject and body and call_to_action:
                    emails.append(
                        Email(
                            subject=subject,
                            body=body,
                            call_to_action=call_to_action,
                        )
                    )
                else:
                    logging.warning(f"Email {i+1} for {account.account_name} is missing required fields, skipping.")
            else:
                logging.warning(f"Email {i+1} for {account.account_name} generated empty response, skipping.")

        # Append campaign data for the account
        if emails:  # Only append campaigns that have valid emails
            campaigns.append(Campaign(account_name=account.account_name, emails=emails))

    return campaigns  # Directly return the list of campaigns
