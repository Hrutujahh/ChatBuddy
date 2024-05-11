from flask import Flask, render_template, request, jsonify
import requests

RASA_API_URL = 'http://127.0.0.1:5005/webhooks/rest/webhook'
app = Flask(__name__)
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        user_message = request.json['message']
        print("User Message:", user_message)

        rasa_response = requests.post(RASA_API_URL, json={'message': user_message})
        rasa_response_json = rasa_response.json()

        print("Rasa Response:", rasa_response_json)

        bot_response = rasa_response_json[0]['text'] if rasa_response_json else 'Sorry, I didn\'t understand that.'

        return jsonify({'response': bot_response})
    except requests.exceptions.RequestException as e:
        # Handle connection errors gracefully
        error_message = "Error connecting to Rasa server: {}".format(e)
        print(error_message)
        return jsonify({'response': 'An error occurred. Please try again later.'}), 500

if __name__ == "__main__":
    app.run(debug=True, port=3000)
