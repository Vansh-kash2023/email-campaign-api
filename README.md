## **Personalized Email Drip Campaign API**

### **Overview**

This project provides an API for generating personalized email sequences for Account-Based Marketing (ABM) campaigns. It uses Gemini to generate email content based on provided data, including account details, pain points, and campaign objectives. The API is built with FastAPI and is ready for deployment using Gunicorn with Uvicorn workers.

### **Features**

- Generate personalized email campaigns.
- Supports multiple email generations for each account.
- Provides endpoints for health checks and campaign generation.

### **Folder Structure**

```
app/
├── __init__.py
├── config.py
├── utils.py
├── main.py
├── models.py
└── services.py
logs/
└── error.log
templates/
└── index.html
tests/
├── test_main.py
├── test_services.py
└── test_utils.py
Procfile
README.md
requirements.txt
.gitignore
.env
```

### **Packages Used**

- **aiohttp, aiosignal, async-timeout**: Required for asynchronous I/O operations.
- **FastAPI**: Modern web framework for building APIs with Python 3.7+.
- **gunicorn**: A WSGI HTTP server for running Python web applications.
- **Jinja2**: Templating engine for Python, used to render HTML templates.
- **Gemini**: Utilized to generate email content. Adjust the prompt for better personalization.
- **pydantic**: Used for request and response models.
- **python-dotenv**: For configuration management using environment variables.
- **pytest, pytest-asyncio**: Testing libraries for writing unit and async tests.

### **How to Clone and Run the Project**

#### **Cloning the Repository**

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Vansh-kash2023/email-campaign-api.git
   cd email-campaign-api
   ```

#### **Setting Up the Environment**

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables. Create a `.env` file in the root of the project directory and add the following:

   ```plaintext
   GEMINI_API_KEY=<your_gemini_api_key>
   ```

#### **Running the Application Locally**

1. Run the application using Uvicorn for local development:

   ```bash
   uvicorn app.main:app --reload
   ```

2. The application will be accessible at `http://127.0.0.1:8000/`. You can access the health check endpoint at `http://127.0.0.1:8000/health`.

#### **Customizing the Gemini Prompt**
To adjust the prompt sent to Gemini for better personalization, edit the prompt template in the services module. For example, in `app/services.py` locate the prompt configuration and modify it as needed:
```python
# ...existing code...
prompt_template = "Hello, {customer_name}! Customize this message for a more personalized experience."
# ...existing code...
```

#### **Deployment**

This application can be deployed on cloud platforms like Railway. It uses a `Procfile` to specify the server setup.

1. To deploy, connect the repository to your Railway project.
2. Railway will automatically use the `Procfile` to start the app with Gunicorn and Uvicorn workers.

#### **Endpoints**

1. **GET /**  
   Returns a basic information page about the API.

2. **POST /generate_campaign**  
   Generates personalized email campaigns based on the input data.  
   **Request Body** (example):
   ```json
   {
     "accounts": [
       {
         "account_name": "Example Corp",
         "industry": "Software",
         "pain_points": ["Scaling issues", "Tech debt"],
         "contacts": [
           {
             "name": "John Doe",
             "email": "john.doe@example.com",
             "job_title": "CEO"
           }
         ],
         "campaign_objective": "nurturing"
       }
     ],
     "number_of_emails": 3
   }
   ```

   **Response**:
   ```json
   {
     "campaigns": [
       {
         "account_name": "Example Corp",
         "emails": [
           {
             "subject": "Subject Line 1",
             "body": "Email body content",
             "call_to_action": "Schedule a demo"
           },
           ...
         ]
       }
     ]
   }
   ```

3. **GET /health**  
   Returns the health status of the API. Useful for monitoring.

---
