import openai
import os
from dotenv import load_dotenv
from app.models import Account, CampaignResponse, Email

# Load the environment variables (API key)
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_campaign_emails(request):
    # Prepare the request for GPT
    campaign_responses = []

    for account in request.accounts:
        account_name = account.account_name
        emails = []

        # Constructing the prompt for the API
        for i in range(request.number_of_emails):
            prompt = f"Create an email for {account_name} for the campaign objective: {account.campaign_objective}. The target industry is {account.industry} and the pain points are {', '.join(account.pain_points)}. The contacts are {', '.join([contact.name for contact in account.contacts])}."

            # Call OpenAI's API to generate an email
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # Use gpt-3.5-turbo instead of text-davinci-003
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200
                )
                email_content = response.choices[0].message['content'].strip()  # Access message content
                subject = f"Campaign Email for {account_name} - {i+1}"
                body = email_content
                call_to_action = "Learn more"  # You can adjust this depending on your requirements

                email = Email(subject=subject, body=body, call_to_action=call_to_action)
                emails.append(email)
            except Exception as e:
                raise Exception(f"Error generating email: {str(e)}")

        # Create a campaign response
        campaign_responses.append(CampaignResponse(account_name=account_name, emails=emails))

    return campaign_responses
