from flask import Flask, request, jsonify
from flask import Flask, render_template, request
import requests, json, openai, os, logging, markdown

class Chat():

	def update_history(self):
		with open("history.txt", "w") as f:
			self.history[self.user_id] = self.messages
			f.write(json.dumps(self.history))

	def get_history(self):
		with open("history.txt") as f:
			self.history = json.load(f)
			if self.user_id in self.history:
				return self.history[self.user_id]
			else:
				return [{"role": "system", "content": "You are a helper bot to help user."},]

	def __init__(self):

		self.log = logging.getLogger(__name__)
		self.log.info("="*15 + " Initalizing " + "="*15)

		# Setting user
		self.user_id = str(123456)

		# Setting history file
		if not (os.path.isfile('history.txt')):
			with open("history.txt", "w") as f:
				f.write("{}")

		# Setting the API key to use the OpenAI API
		openai.api_key = ""
		
		self.messages = self.get_history()

		
		self.log.info("Done")

	def talk(self, message):
		self.messages.append({"role": "user", "content": message})
		response = openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			messages=self.messages
		)
		self.messages.append({"role": "assistant", "content": response["choices"][0]["message"].content})
		self.update_history()
		return response["choices"][0]["message"]

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

@app.route('/history', methods=['GET'])
def history():
	history = chat.get_history()		
	return json.dumps(history)

app.run(debug=True)