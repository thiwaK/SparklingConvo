import sqlite3
import json
import time
from datetime import datetime

class Database:

    def __init__(self):

        self.conn = sqlite3.connect('chat_history.db', check_same_thread=False)
        self.c = self.conn.cursor()

        self.c.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            created_at DATETIME NOT NULL
        )''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            chat_name TEXT NOT NULL,
            chat_json TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )''')

    def __del__(self):
        self.conn.close()

    def _millis_to_datetime(self, millis):
        now = datetime.fromtimestamp(millis).strftime("%Y-%m-%d %H:%M:%S")
        return now

    def _current_millis(self):
        return round(time.time() * 1000)

    def add_user(self, user_id, name):
        self.c.execute("INSERT OR IGNORE INTO users (user_id, name, created_at) VALUES (?, ?, ?)", (user_id, name, self._current_millis()))
        self.conn.commit()

    def add_chat(self, user_id, chat_name, chat_array):
        chat_json = json.dumps(chat_array)
        self.c.execute("INSERT INTO chats (user_id, chat_name, chat_json, created_at) VALUES (?, ?, ?, ?)", (user_id, chat_name, chat_json, self._current_millis()))
        self.conn.commit()

    def update_chat(self, user_id, chat_id, chat_array):
        chat_json = json.dumps(chat_array)
        if self.get_chat(user_id, chat_id):
            self.c.execute("UPDATE chats SET chat_json = ? WHERE id = ? and user_id = ?", (chat_json, chat_id, user_id))
            self.conn.commit()
        else:
            self.add_chat(user_id, "chat-" + str(chat_id), chat_array)
        

    def delete_chat(self, user_id, chat_id):
        self.c.execute("DELETE FROM chats WHERE id = ? and user_id = ?", (chat_id, user_id))
        self.conn.commit()

    def get_chats(self, user_id):
        self.c.execute("SELECT id, user_id, chat_name FROM chats WHERE user_id = ? ORDER BY created_at", (user_id,))
        rows = self.c.fetchall()
        # print(rows)
        if len(rows) == 0:
            return None
        return rows

    def get_chat(self, user_id, chat_id):
        self.c.execute("SELECT chat_json FROM chats WHERE id = ? and user_id = ?", (chat_id, user_id))
        rows = self.c.fetchall()
        if len(rows) == 0:
            return None
        # print(rows)
        return json.loads(rows[0][0])