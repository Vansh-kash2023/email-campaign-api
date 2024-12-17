import google.generativeai as genai
import os
from dotenv import load_dotenv
from app.models import Account, CampaignResponse, Email

# Load the environment variables (API key)
load_dotenv()

# Set the Gemini AI API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def generate_campaign_emails(request):
    # Prepare the response for all accounts
    campaign_responses = []

    for account in request.accounts:
        account_name = account.account_name
        emails = []

        # Generate the prompt for the API
        for i in range(request.number_of_emails):
            prompt = f"""
            Create a professional and engaging email for the account "{account_name}".
            Campaign Objective: {account.campaign_objective}
            Target Industry: {account.industry}
            Pain Points: {', '.join(account.pain_points)}
            Contacts: {', '.join([contact.name for contact in account.contacts])}.

            The email should:
            1. Have a clear subject line.
            2. Include a body with value propositions or relevant content.
            3. End with a strong call-to-action.
            """

            # Call the Gemini AI API
            try:
                response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
                email_content = response.text.strip()

                # Extract subject, body, and CTA (simple split for demo purposes)
                subject = f"Campaign Email for {account_name} - {i+1}"
                body = email_content
                call_to_action = "Click here to learn more."

                # Create the Email model
                email = Email(subject=subject, body=body, call_to_action=call_to_action)
                emails.append(email)
            except Exception as e:
                raise Exception(f"Error generating email: {str(e)}")

        # Create a campaign response for the account
        campaign_responses.append(CampaignResponse(account_name=account_name, emails=emails))

    return campaign_responses
