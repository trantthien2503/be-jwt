from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from firebase_service import FirestoreCollection

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/content', methods=['POST'])
def content():
    if request.headers['Content-Type'] != 'application/json':
        return Response('Unsupported Media Type', status=415)
    text = request.get_json().get('content')
    content = {
        "content": text,
    }
    fire = FirestoreCollection("content")
    update_data = fire.update_data("oHPGhzaABpTSzbglG1in",content)
    response_data = {"data": update_data}
    return jsonify(response_data)

@app.route('/get-content', methods=['GET'])
def getContent():
    if request.headers['Content-Type'] != 'application/json':
        return Response('Unsupported Media Type', status=415)
    fire = FirestoreCollection("content")
    all_data = fire.get_all_data()
    response_data = {"data": all_data['data'][0]['content']}
    return jsonify(response_data)


@app.route('/stream')
def stream():
    def generate():
        fire = FirestoreCollection("content")
        all_data = fire.get_all_data()
        yield f"data: {all_data['data'][0]['content']}\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    
    app.run(debug=True)