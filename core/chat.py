import requests, json, openai, os
import logging
from core.database import Database
from chatsmith_ai import chat as chatsmith

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class Chat:

	def __init__(self):

		self.log = logging.getLogger(__name__)
		self.log.info("Initalizing")
		self.db = Database()
		self.maximum_number_of_diogues = 20
				
		self.user_id = self.db.get_user_id("Human")
		self.bot_id = self.db.get_user_id("Bot")
		self.log.info("Done")

	def display(self):
		''' For CLI
		'''
		for item in [obj for obj in self.history]:
			text = self.__format_msg__(item['role'], item['content'])
			print(text)

	def __format_msg__(self, role, message):
		''' For CLI
		'''
		max_length = 80
		sender_header = ">>>"
		reciver_header = "<<<"

		header_space = max(len(sender_header), len(reciver_header)) + 1
		message_area = max_length - header_space
		chunks = len(message)

		msg = ""
		if role == 'user': msg += sender_header + '\n'
		else: msg += reciver_header + '\n'

		for item in [ ' ' * header_space + message[i:i+message_area] for i in range(0, chunks, message_area) ]:
			# print(item)
			msg += item

		return msg

	def __next_chat_id__(self):
		chats = self.db.get_chats(self.user_id)
		if not chats:
			return 1
		next_chat_id = 0
		for chat_id, _, _ in [chat for chat in chats]:
			next_chat_id = max(next_chat_id, chat_id)

		last_chat = self.db.get_chat(self.user_id, next_chat_id)
		if len(last_chat) <= 1:
			return next_chat_id

		return next_chat_id + 1
	
	def new_chat(self, message, about):
		self.db.start_new_conversation(sender_id=self.user_id, receiver_id=self.bot_id, about=about, message_text=message)

	def update_history(self):
		self.db.update_chat(self.user_id, self.chat_id, self.messages)

	def get_history(self, role=["Act as a professional GIS assistant", "Act as a Geographical information science student" 
		"Act as a geographical information science professor"][1]):
		history = self.db.get_chat(self.user_id, self.chat_id)
		if history:
			return history
		else:
			# self.db.add_chat(self.user_id, self.chat_id, [{"role": "system", "content": "You are a helper bot to help user."},])
			return [{"role": "system", "content": role},]

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
				model="gpt-3.5-turbo",
				messages=self.messages[-1 * self.maximum_number_of_diogues:]
			)
		else:
			response = openai.ChatCompletion.create(
				model="gpt-3.5-turbo",
				messages=self.messages
			)
		self.messages.append({"role": "assistant", "content": response["choices"][0]["message"].content})
		self.update_history()
		return response["choices"][0]["message"]
