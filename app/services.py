import requests
from app.models import InputData, Campaign, Email
import logging

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Gemini API endpoint and API key (replace with your actual API key)
GEMINI_API_KEY = "AIzaSyCduDg8TcCuba9od_VU6ElOlOHIsvnHmT4"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"  # Replace with the correct URL
  # Replace with your actual API key

def generate_prompt(account, email_index):
    """
    Generate a prompt for Gemini API based on account data.
    """
    return f"""
    You are a marketing expert specializing in the software industry. Write email {email_index} of a nurturing drip campaign for Example Corp, a software company facing challenges with scaling and tech debt.

    * Target audience: John Doe, CEO of Example Corp
    * Goal: Nurture the lead and educate them about the benefits of your product/service in overcoming scaling issues and tech debt.

    *Body:*

    * Briefly introduce yourself and your company.
    * Acknowledge the common challenges faced by software companies like scaling and tech debt.
    * Explain how your product/service can help Example Corp address these challenges with specific examples.
    * Use a positive and confident tone, highlighting the value proposition of your offering.

    *Call to action:*

    * Include a clear call to action, such as scheduling a demo or requesting a free consultation, to learn more about how your product/service can benefit Example Corp.

    *Sign-off:*

    Thank John Doe for his time and consideration. Include your contact information.

    The tone should be professional, friendly, and personalized.
    """

async def call_gemini(prompt):
    """
    Generate text using the Gemini API.
    """
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "max_length": 1500,
        "temperature": 0.9,
        "top_p": 0.95,
        "do_sample": True
    }

    logging.debug(f"Prompt: {prompt}")

    # Make the request to the Gemini API
    response = requests.post(GEMINI_API_URL, json=payload, headers=headers)

    # Check for successful response
    if response.status_code != 200:
        logging.error(f"Error generating text with Gemini: {response.text}")
        return {}

    # Parse the response
    generated_text = response.json().get("generated_text", "")
    logging.debug(f"Generated Text: {generated_text}")

    # Parsing the generated response into structured content
    lines = generated_text.split("\n")

    subject = ""
    body = []
    call_to_action = ""

    for line in lines:
        line = line.strip()
        if line.lower().startswith("subject:"):
            subject = line.replace("Subject:", "").strip()
        elif line.lower().startswith("body:"):
            body.append(line.replace("Body:", "").strip())
        elif line.lower().startswith("call to action:"):
            call_to_action = line.replace("Call to action:", "").strip()

    body_content = " ".join(body).strip()

    return {
        "subject": subject,
        "body": body_content,
        "call_to_action": call_to_action
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

            # Append the generated emails
            emails.append(
                Email(
                    subject=response.get("subject", ""),
                    body=response.get("body", ""),
                    call_to_action=response.get("call_to_action", ""),
                )
            )

        # Append campaign data for the account
        campaigns.append(Campaign(account_name=account.account_name, emails=emails))

    return campaigns