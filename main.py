from flask import Flask, request, jsonify
from flask import Flask, render_template, request
import requests, json, openai, os, logging, markdown
from core.chat import Chat


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

chat = Chat()
app = Flask("ChatBot")

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
	message = request.json['message']
	reply = chat.talk(message)
	reply['content'] = markdown.markdown(json.dumps(reply['content']), extensions=['fenced_code', 'codehilite', 'toc'])
	# print(reply)
	return reply

@app.route('/history', methods=['POST'])
def history():
	chat_id = request.json['chat_id']
	chat.chat_id = chat_id
	history = chat.get_history()
	return json.dumps(history)

@app.route('/chats', methods=['GET'])
def chats():
	chats = chat.get_chats()
	print(chats)
	return json.dumps(chats)

app.run(debug=True)