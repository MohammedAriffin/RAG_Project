from flask import Flask, request, Response, stream_with_context
import json
import time
import uuid
app = Flask(__name__)

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data["messages"]

    def generate():
        for message in messages:
            # Simulate processing the message
            print(f"Processing message: {message}")
            yield f"data: {json.dumps(message)}\n\n"
            print("response stream")
            response = {
                "id": str(uuid.uuid4()),
                "createdAt": time.time(),
                "content": f"You said: {message['content']}. Let me think about that...",
                "role": "assistant"
            }
            yield f"data: {json.dumps(response)}\n\n"
            # time.sleep(1) 
            
        print("All messages processed")
        yield "data: [DONE]\n\n"

    return Response(stream_with_context(generate()), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)