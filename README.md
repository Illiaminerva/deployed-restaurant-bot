# Restaurant Chatbot Deployment

This repository contains the deployment code for the Restaurant Recommendation Chatbot. The model training and development code can be found in the [training repository](https://github.com/Illiaminerva/yelp-bot).

## Technologies Used

- **Docker** - Application containerization
- **Google Cloud Run** - Serverless container deployment
- **Google Cloud Storage** - Model weights storage
- **Flask** - Web API framework
- **PyTorch** - ML model serving

## Project Structure

```
restaurant-bot/
├── app/
│   ├── flask_app.py      # Main Flask application
│   ├── models/
│   │   └── chatbot.py    # Chatbot model wrapper
│   └── model/           # Directory for downloaded model weights
├── Dockerfile           # Container definition
└── requirements.txt     # Python dependencies
```

## Model Architecture

The chatbot uses a fine-tuned GPT-2 model with:
- Custom sentiment analysis head
- Restaurant-specific training
- Optimized generation parameters

## Deployment

### Local Development

1. Clone this repository:
```bash
git clone https://github.com/Illiaminerva/deployed-restaurant-bot.git
cd deployed-restaurant-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the model:
   - Download the model weights from the training repository
   - Place `best_rl_model.pt` in `app/model/`

4. Run the Flask app:
```bash
python app/flask_app.py
```

### Cloud Deployment

The service is deployed on Google Cloud Run and accessible at:
https://deployed-restaurant-bot-352450963275.us-central1.run.app

Environment Variables:
- `MODEL_URL`: Points to the model weights in Cloud Storage
- `PORT`: Set automatically by Cloud Run

Deployment Process:
- Builds from Dockerfile
- Downloads model weights at startup
- Serves predictions via Flask API

## API Usage

### Chat Endpoint

```bash
curl -X POST https://deployed-restaurant-bot-352450963275.us-central1.run.app/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What's a good Italian restaurant in San Francisco?"}'
```

### Response Format

```json
{
  "response": "Restaurant recommendation with details..."
}
```

## Model Training

For details on model training, data preparation, and evaluation metrics, please refer to the [training repository](https://github.com/Illiaminerva/yelp-bot). The training process includes:
- Data collection and preprocessing
- Fine-tuning on restaurant data
- Reinforcement learning optimization
- Evaluation metrics and testing
