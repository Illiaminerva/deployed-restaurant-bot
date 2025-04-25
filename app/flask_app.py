import os
from flask import Flask, jsonify, request, render_template_string
import torch
import numpy as np
from pathlib import Path
from models.chatbot import RestaurantChatbot
import requests

app = Flask(__name__)

# Initialize model
device = 'cpu'
model = None

def download_model():
    global model
    try:
        # Create model directory if it doesn't exist
        os.makedirs("model", exist_ok=True)
        
        # Try to load model from local path first
        model_path = os.path.join("model", "best_rl_model.pt")
        if not os.path.exists(model_path):
            print("Model not found locally, downloading from Cloud Storage...")
            url = os.environ.get('MODEL_URL')
            if not url:
                raise ValueError("MODEL_URL environment variable not set")
            
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(model_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Model downloaded successfully")
        
        # Load model with original parameters
        model = RestaurantChatbot(device=device)
        model.load_state_dict(torch.load(model_path, map_location=device))
        model.eval()
        print("Model loaded successfully")
        return True
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return False

# Download model on startup
download_model()

# HTML template for the chat interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Restaurant Chatbot</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .chat-container { margin-top: 20px; }
        input[type="text"] { width: 80%; padding: 10px; margin-right: 10px; }
        button { padding: 10px 20px; background: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background: #45a049; }
        #response { margin-top: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>🤖 Restaurant Chatbot</h1>
    <div class="chat-container">
        <input type="text" id="query" placeholder="Ask about restaurants...">
        <button onclick="sendMessage()">Send</button>
    </div>
    <div id="response"></div>

    <script>
    function sendMessage() {
        const query = document.getElementById('query').value;
        if (!query) return;

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({query: query})
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('response').innerText = data.response;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('response').innerText = 'Error: Could not get response';
        });
    }

    // Allow Enter key to send message
    document.getElementById('query').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    </script>
</body>
</html>
"""

@app.route('/health', methods=['GET'])
def health_check():
    model_status = "loaded" if model is not None else "not loaded"
    return jsonify({
        "status": "healthy",
        "model_status": model_status
    })

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    if model is None:
        if not download_model():
            return jsonify({"error": "Model not loaded"}), 503
    
    try:
        query = request.json.get("query", "")
        # Use original generation parameters that worked well
        response = model.generate_response(
            query,
            max_length=150,  # Increased for more complete responses
            temperature=0.8,  # Original temperature
            top_p=0.92,
            top_k=50,
            do_sample=True
        )
        # Clean up response
        response = response.replace("Assistant:", "").strip()
        if len(response.strip()) < 10:
            response = "I apologize, but I need more information to provide a good restaurant recommendation. Could you please provide more details about what you're looking for?"
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
