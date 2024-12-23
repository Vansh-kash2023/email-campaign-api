
---

```markdown
# Personalized Email Drip Campaign API

## Overview
The Personalized Email Drip Campaign API is designed to automate the creation of highly personalized email sequences for Account-Based Marketing (ABM) campaigns. The API leverages the Gemini API to generate email content tailored to the specific needs, pain points, and objectives of individual accounts. This project aims to streamline the process of creating effective email campaigns, helping businesses engage with their target audience in a personalized way.

## Features
- Accepts account data, including account name, industry, pain points, and campaign objectives.
- Generates personalized email sequences based on the provided data.
- Supports multiple campaign objectives such as awareness, nurturing, and upselling.
- Provides a flexible solution for generating email campaigns at scale.

## Installation

### Prerequisites
- Python 3.8 or higher
- `pip` (Python package installer)

### Steps to Install

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Vansh-kash2023/email-campaign-api.git
    cd email-campaign-api
    ```

2. **Create and activate a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file** in the project root and add your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

5. **Run the application**:
    ```bash
    uvicorn app.main:app --reload
    ```

   Your FastAPI application will be accessible at `http://127.0.0.1:8000`.

## API Documentation

### Available Endpoints

- **`GET /`**: Displays information about the API on the landing page (HTML).
- **`POST /generate_campaign`**: Accepts account data and generates a personalized email sequence.

### **Request Example**:

```json
{
  "accounts": [
    {
      "account_name": "Company A",
      "industry": "Software",
      "pain_points": ["Lack of integration", "Slow processes"],
      "contacts": [
        {
          "name": "John Doe",
          "email": "john@example.com",
          "job_title": "CEO"
        }
      ],
      "campaign_objective": "nurturing"
    }
  ],
  "number_of_emails": 5
}
```

### **Response Example**:

```json
{
  "campaigns": [
    {
      "account_name": "Company A",
      "emails": [
        {
          "subject": "Subject for email 1",
          "body": "Body content of email 1",
          "call_to_action": "Call to action for email 1"
        }
      ]
    }
  ]
}
```

### **Error Handling**:

If an error occurs (e.g., invalid input), the API will return an error message in the following format:
```json
{
  "error": "Error message"
}
```

## Project Structure

```
<project-directory>/
├── app/
│   ├── main.py           # Main entry point for FastAPI application
│   ├── models.py         # Data models and validation schemas
│   ├── services.py       # Business logic for generating email campaigns
│   └── templates/        # HTML templates for rendering views
├── logs/                 # Directory for storing log files (e.g., error.log)
├── requirements.txt      # List of Python dependencies
├── .env                  # Environment variables (including GEMINI_API_KEY)
└── README.md             # Project documentation
```

## Dependencies

- **FastAPI**: A modern web framework for building APIs with Python 3.7+.
- **Uvicorn**: ASGI server for serving FastAPI applications.
- **Requests**: HTTP library for making requests to external APIs (Gemini in this case).
- **python-dotenv**: A library to load environment variables from a `.env` file.
- **Jinja2**: A templating engine used to render HTML templates for the landing page.

## Error Logging

This application logs errors to a file located at `logs/error.log`. This log will contain details of any issues encountered during the request processing.

## How It Works

1. The user sends a POST request to `/generate_campaign` with account data and the desired number of emails.
2. The API uses the provided account details to generate personalized email content using the Gemini API.
3. The response contains the generated email subjects, bodies, and call-to-action for each email in the sequence.
