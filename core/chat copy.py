import requests, json, openai, os
import logging
from core.database import Database

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class Chat:

	def __init__(self):

		self.log = logging.getLogger(__name__)
		self.log.info("Initalizing")
		self.ai_model = "gpt-3.5-turbo"
		self.db = Database()
		self.maximum_number_of_dialogues = 20
		
		self.user_id = None
		self.conv_id = None

		self.log.info(f"Max dialogues: {self.maximum_number_of_dialogues}")
		self.log.info("Done")



	def new_conversation(self):
		self.chat_id = self.__next_chat_id__()
		self.messages = self.get_history()

	def update_history(self):
		self.db.update_chat(self.user_id, self.chat_id, self.messages)

	def get_history(self):
		history = self.db.get_chat(self.user_id, self.chat_id)
		if history:
			return history
		else:
			# self.db.add_chat(self.user_id, self.chat_id, [{"role": "system", "content": "You are a helper bot to help user."},])
			return [{"role": "system", "content": "You are a helper bot to help user."},]

	def get_chats(self):
		
		chats = []
		print(self.user_id)
		chats_js = self.db.get_chats(self.user_id)
		if not chats_js:
			return None

		for chat_id, user_id, chat_name in [chat for chat in chats_js]:
			chats.append((chat_id, chat_name))

		return chats

	def talk(self, message):
		print(message)
		self.messages.append({"role": "user", "content": message})
		if (len(self.messages) > self.maximum_number_of_diogues):
			response = openai.ChatCompletion.create(
				model=self.ai_model,
				messages=self.messages[-1 * self.maximum_number_of_diogues:]
			)
		else:
			response = openai.ChatCompletion.create(
				model=self.ai_model,
				messages=self.messages
			)
		self.messages.append({"role": "assistant", "content": response["choices"][0]["message"].content})
		self.update_history()
		return response["choices"][0]["message"]
