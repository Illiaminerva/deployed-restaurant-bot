import os
from flask import Flask, jsonify, request
import torch
import numpy as np
from pathlib import Path
from models.chatbot import RestaurantChatbot

app = Flask(__name__)

# Load model
device = 'cpu'
model = RestaurantChatbot(device=device)
model_path = os.path.join("model", "best_rl_model.pt")
model.load_state_dict(torch.load(model_path, map_location=device))
model.eval()

@app.route('/health', methods=['GET'])
def health_check():
    model_status = "loaded" if model is not None else "not loaded"
    return jsonify({
        "status": "healthy",
        "model_status": model_status
    })

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 503
    
    try:
        data = request.get_json()
        
        if 'input' not in data:
            return jsonify({"error": "No input provided"}), 400

        # Process input and get prediction
        # Note: You'll need to adjust this part based on your model's expected input format
        input_text = data['input']
        
        # TODO: Add your model's preprocessing steps here
        
        with torch.no_grad():
            # TODO: Add your model's inference steps here
            # This is a placeholder - you'll need to modify based on your model's architecture
            output = "Sample response"  # Replace with actual model output processing
        
        return jsonify({
            "input": input_text,
            "prediction": output
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to the Restaurant Bot API",
        "endpoints": {
            "/predict": "POST - Make a prediction",
            "/health": "GET - Check API health"
        }
    })

@app.route("/", methods=["GET"])
def index():
    return "🤖 Restaurant Chatbot is running!"

@app.route("/chat", methods=["POST"])
def chat():
    query = request.json.get("query", "")
    response = model.generate_response(query, max_length=100)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
