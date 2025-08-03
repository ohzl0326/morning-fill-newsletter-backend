# The Morning Fill Newsletter Backend

A robust backend system for "The Morning Fill" financial newsletter by Meridius Labs.

## 🚀 Quick Start

### 1. Initialize the Database
```bash
python3 initialize_db.py
```

### 2. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Start the API Server
```bash
python3 app.py
```

The API will be available at `http://localhost:5000`

## 📊 Database Schema

### Subscribers Table
- `id`: Auto-incrementing primary key
- `email`: Unique email address (required)
- `first_name`: Optional first name
- `last_name`: Optional last name
- `company_name`: Optional company name
- `job_title`: Optional job title
- `subscription_date`: Auto-timestamp when subscribed
- `consent_given`: Boolean consent flag (required)
- `status`: Subscription status (active/unsubscribed/pending)

### Newsletter Content Table
- `id`: Auto-incrementing primary key
- `generation_date`: Date newsletter was generated
- `edition`: Newsletter edition (morning/afternoon)
- `pipeline_step`: AI generation step name
- `content`: Raw AI-generated content
- `reviewed_content`: Final reviewed content
- `llm_model_used`: AI model name
- `prompt_key`: Prompt file/key used
- `created_at`: Auto-timestamp when created

## 🔌 API Endpoints

### POST /subscribe
Add a new subscriber to the database.

**Request Body:**
```json
{
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "company_name": "Company Inc",
    "job_title": "Manager",
    "consent_given": true
}
```

**Response:**
```json
{
    "success": true,
    "message": "Subscriber added successfully",
    "subscriber_id": 1,
    "email": "user@example.com"
}
```

### GET /health
Health check endpoint for monitoring.

### GET /
API information and available endpoints.

## 🔄 Zapier Email Parser Workflow

### Overview
Since your B12 website doesn't support webhooks, we use Zapier's Email Parser to automate subscriber data ingestion.

### Step-by-Step Workflow

#### 1. Initial Setup
- **Zapier Email Parser**: Create a unique email address (e.g., `subscribe@yourdomain.com`)
- **B12 Form**: Configure your newsletter signup form to send email notifications to this address

#### 2. Zapier Trigger
- **App**: Email Parser by Zapier
- **Event**: New Email
- **Email Address**: Your unique parser email address

#### 3. Email Parsing
- **Parser Setup**: Configure Zapier to extract form fields from the email:
  - Email address
  - First name
  - Last name
  - Company name
  - Job title
  - Consent checkbox

#### 4. API Bridge
- **Why Needed**: Zapier cannot directly connect to local SQLite files
- **Solution**: Flask API serves as a "front door" to your database
- **Deployment**: Host your Flask app on a service like:
  - Heroku
  - Railway
  - DigitalOcean App Platform
  - AWS Elastic Beanstalk

#### 5. Zapier Action
- **App**: Webhooks by Zapier
- **Event**: POST
- **URL**: Your API endpoint (e.g., `https://your-api.herokuapp.com/subscribe`)
- **Payload**: JSON data from parsed email
- **Headers**: `Content-Type: application/json`

#### 6. API Processing
Your Flask API (`/subscribe` endpoint) will:
1. Receive JSON data from Zapier
2. Validate required fields (email)
3. Check for duplicate emails
4. Insert new subscriber into SQLite database
5. Return success/error response to Zapier

### Data Flow
```
B12 Form → Email → Zapier Parser → Webhook → Flask API → SQLite Database
```

## 🛠️ Development

### Project Structure
```
├── database/
│   ├── schema.sql          # Database schema
│   └── database.db         # SQLite database (created by initialize_db.py)
├── app.py                  # Flask API application
├── initialize_db.py        # Database initialization script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### Testing the API
```bash
# Test the subscribe endpoint
curl -X POST http://localhost:5000/subscribe \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "consent_given": true
  }'

# Check health status
curl http://localhost:5000/health

# Test with python3 (alternative to curl)
python3 -c "
import requests
import json

data = {
    'email': 'test@example.com',
    'first_name': 'John',
    'last_name': 'Doe',
    'consent_given': True
}

response = requests.post('http://localhost:5000/subscribe', json=data)
print('Status:', response.status_code)
print('Response:', response.json())
"
```

## 🔧 Configuration

### Environment Variables
For production deployment, consider setting:
- `FLASK_ENV`: Set to `production`
- `DATABASE_URL`: If using external database
- `SECRET_KEY`: For Flask security

### Database Backup
```bash
# Backup SQLite database
cp database/database.db database/backup_$(date +%Y%m%d_%H%M%S).db
```

## 📈 Monitoring

- **Health Check**: Use `/health` endpoint for monitoring
- **Logs**: Check Flask application logs for errors
- **Database**: Monitor subscriber count and growth

## 🚀 Production Deployment

1. **Choose Platform**: Heroku, Railway, DigitalOcean, AWS
2. **Set Environment**: Configure production settings
3. **Database**: Consider PostgreSQL for production scale
4. **Monitoring**: Set up logging and health checks
5. **SSL**: Ensure HTTPS for secure data transmission

---

**Built for Meridius Labs - The Morning Fill Newsletter** 