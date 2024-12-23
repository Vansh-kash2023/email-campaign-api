import openai
import os
from app.models import InputData, Campaign, Email
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_email_campaign(data: InputData):
    """
    Generate email campaigns using OpenAI's API.
    """
    campaigns = []

    for account in data.accounts:
        emails = []
        for i in range(data.number_of_emails):
            prompt = generate_prompt(account, i + 1)
            response = await call_openai(prompt)

            emails.append(
                Email(
                    subject=response["subject"],
                    body=response["body"],
                    call_to_action=response["call_to_action"],
                )
            )

        campaigns.append(Campaign(account_name=account.account_name, emails=emails))

    return campaigns

def generate_prompt(account, email_index):
    """
    Generate a prompt for the GenAI model based on account data.
    """
    return f"""
    You are an expert marketer. Write email {email_index} of a drip campaign for the following account:
    - Account Name: {account.account_name}
    - Industry: {account.industry}
    - Key Pain Points: {", ".join(account.pain_points)}
    - Campaign Objective: {account.campaign_objective}
    - Contact: {account.contacts[0].name}, {account.contacts[0].job_title}

    The email should be personalized, engaging, and align with the campaign objective. Provide:
    1. A subject line.
    2. An email body.
    3. A clear call-to-action.
    """

async def call_openai(prompt):
    """
    Call the OpenAI API with the generated prompt.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    content = response["choices"][0]["message"]["content"]
    lines = content.split("\n")
    return {
        "subject": lines[0].strip(),
        "body": "\n".join(lines[1:-1]).strip(),
        "call_to_action": lines[-1].strip(),
    }
