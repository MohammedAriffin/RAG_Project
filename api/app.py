from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from final import ODMLAssistant
import time
import json

app = Flask(__name__)
CORS(app)

assistant = ODMLAssistant()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Handle both form data and JSON
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Get response directly without streaming
        response = assistant.generate_response(user_message)
        # time.sleep(5)
        # response = "Suvan : Hi, How can I help you?"
        return jsonify({"response": response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)