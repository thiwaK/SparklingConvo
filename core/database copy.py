import sqlite3
import json
import time
from datetime import datetime

class Database:

    def __init__(self):

        self.conn = sqlite3.connect('chat_history_new.db', check_same_thread=False)
        self.c = self.conn.cursor()

        self.c.execute('''CREATE TABLE IF NOT EXISTS User (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            openai_key VARCHAR(100) NOT NULL,
            created_at DATETIME NOT NULL
        );''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS Conversation (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            created_at DATETIME NOT NULL
        );''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS Message (
            id INT AUTO_INCREMENT PRIMARY KEY,
            text TEXT NOT NULL,
            sent_at DATETIME NOT NULL,
            sender_id INT NOT NULL,
            receiver_id INT NOT NULL,
            conversation_id INT NOT NULL,
            FOREIGN KEY (sender_id) REFERENCES User(id),
            FOREIGN KEY (receiver_id) REFERENCES User(id),
            FOREIGN KEY (conversation_id) REFERENCES Conversation(id)
        );''')

        self.c.execute("SELECT id FROM User ORDER BY created_at DESC LIMIT 1;")
        if len(self.c.fetchall()) == 0:
            self.c.execute("INSERT OR IGNORE INTO User (username, openai_key, created_at) VALUES (Bot, Bot, NOW())")

    def __del__(self):
        self.conn.close()

    def _millis_to_datetime(self, millis):
        now = datetime.fromtimestamp(millis).strftime("%Y-%m-%d %H:%M:%S")
        return now

    def _current_millis(self):
        return round(time.time() * 1000)

    def add_user(self, name, api_key):
        '''Creating new user
        name - user name
        api_key - openai token'''
        self.c.execute("INSERT OR IGNORE INTO User (username, openai_key, created_at) VALUES (?, ?, NOW())", (name, api_key))
        self.conn.commit()

    def add_conversation(self, conv_name):
        '''Create new conversation
        conv_name - name of the new conversation'''
        self.c.execute("INSERT OR IGNORE INTO Conversation (name, created_at) VALUES (?, NOW())", (conv_name,))
        self.conn.commit()
        
    def add_message(self, message, sender_id, receiver_id, conversation_id):
        '''Add new message
        message - the actual message
        sender_id - user_id of the sender
        receiver_id - user_id of ther receiver
        conversation_id - id of the conversation'''
        self.c.execute("INSERT INTO Message (text, sent_at, sender_id, receiver_id, conversation_id) VALUES (?, NOW(), ?, ?, ?)", 
                        (message, sender_id, receiver_id, conversation_id))
        self.conn.commit()
    
    def delete_conversation(self, conv_id):
        '''Delete selected conversation with all the messages associate
        conv_id - id of the conversation needs to be delete'''
        self.c.execute("DELETE FROM Message WHERE conversation_id = ?", (conv_id,))
        self.c.execute("DELETE FROM Conversation WHERE id = ?", (conv_id,))
        self.conn.commit()

    def update_message(self, message_id, new_message):
        self.c.execute("UPDATE Message SET text = ? WHERE id = ?", (new_message, message_id))
        self.conn.commit()

    def delete_message(self, message_id):
        self.c.execute("DELETE FROM Message WHERE id = ?", (message_id,))
        self.conn.commit()

        
    def get_last_conversation(self):
        '''Get last conversation id'''
        self.c.execute("SELECT id FROM Conversation ORDER BY created_at DESC LIMIT 1;")
        id = self.c.fetch()

    def get_conversations(self):
        '''Get conversations with id and name'''
        self.c.execute("SELECT id, name FROM Conversation ORDER BY created_at;")
        rows = self.c.fetchall()

    def get_messages(self, conv_id):
        self.c.execute("SELECT * FROM Message WHERE conversation_id = ? ORDER BY created_at", (conv_id,))
        rows = self.c.fetchall()
        if len(rows) == 0:
            return None
        return rows