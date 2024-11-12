
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from final import ODMLAssistant
import json

app = Flask(__name__)
# CORS(app)

assistant = ODMLAssistant()

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    def generate():
        response = assistant.generate_response(user_message)
        yield json.dumps({"response": response}) + "\n"

    return Response(generate(), mimetype='application/x-ndjson')

if __name__ == '__main__':
    app.run(debug=True, port=5000)