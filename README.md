# Restaurant Chatbot

A GPT-2 based restaurant recommendation chatbot with sentiment analysis capabilities.

## API Endpoints

- `GET /` - Health check endpoint
- `POST /chat` - Chat with the bot
  - Request body: `{"query": "your question here"}`
  - Response: `{"response": "bot's response"}`

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python app/flask_app.py
```

## Deployment

The application is configured to run on DigitalOcean App Platform. 