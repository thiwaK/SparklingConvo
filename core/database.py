import sqlite3
import json
import time
from datetime import datetime

class Database:

    def __init__(self):

        self.conn = sqlite3.connect('chat_history.db', check_same_thread=False)
        self.c = self.conn.cursor()

        # Create the users table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create the chats table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                chat_id INTEGER PRIMARY KEY,
                about TEXT NOT NULL,
                sender_id INTEGER NOT NULL,
                receiver_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sender_id) REFERENCES users(user_id),
                FOREIGN KEY (receiver_id) REFERENCES users(user_id)
            )
        ''')

        # Create the messages table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                message_id INTEGER PRIMARY KEY,
                chat_id INTEGER NOT NULL,
                sender_id INTEGER NOT NULL,
                receiver_id INTEGER NOT NULL,
                message_text TEXT NOT NULL,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES chats(chat_id),
                FOREIGN KEY (sender_id) REFERENCES users(user_id),
                FOREIGN KEY (receiver_id) REFERENCES users(user_id)
            )
        ''')

        # Commit the changes and close the connection
        self.c.commit()
        self.insert_user("Bot")
        self.insert_user("Human")

        print("Database successfully initalized.")

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
    

    def get_user_id(self, username):
        self.c.execute('''
            SELECT user_id FROM users WHERE username=?
        ''', (username,))
        user_id = self.c.fetchone()
        if user_id:
            return user_id[0]
        else:
            return None
        
    # Insert a new message
    def insert_message(self, chat_id, sender_id, receiver_id, message_text):
        sent_at = datetime.now()
        self.c.execute('''
            INSERT INTO messages (chat_id, sender_id, receiver_id, message_text, sent_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (chat_id, sender_id, receiver_id, message_text, sent_at))
        self.c.commit()

    # Retrieve messages for a given chat
    def get_conversation(self, chat_id):
        self.c.execute('''
            SELECT * FROM messages WHERE chat_id=?
        ''', (chat_id,))
        messages = self.c.fetchall()
        for message in messages:
            print(message)

    # Delete a conversation
    def delete_conversation(self, chat_id):
        self.c.execute('''
            DELETE FROM messages WHERE chat_id=?
        ''', (chat_id,))
        self.c.commit()

    # Update a message
    def update_message(self, message_id, new_text):
        self.c.execute('''
            UPDATE messages SET message_text=? WHERE message_id=?
        ''', (new_text, message_id))
        self.c.commit()

    # Start a new chat
    def start_new_conversation(self, sender_id, receiver_id, about, message_text):
        # Check if both sender and receiver exist
        self.c.execute('''
            SELECT * FROM users WHERE user_id=? OR user_id=?
        ''', (sender_id, receiver_id))
        users = self.c.fetchall()
        if len(users) != 2:
            print("Both sender and receiver must exist.")
        else:
            # Create a new chat entry
            sent_at = datetime.now()
            self.c.execute('''
                INSERT INTO chats (sender_id, receiver_id, about, created_at)
                VALUES (?, ?, ?, ?)
            ''', (sender_id, receiver_id, about, sent_at))
            self.c.commit()

            # Retrieve the newly created chat ID
            chat_id = self.c.lastrowid

            # Insert the initial message into the messages table
            sent_at = datetime.now()
            self.c.execute('''
                INSERT INTO messages (chat_id, sender_id, receiver_id, message_text, sent_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (chat_id, sender_id, receiver_id, message_text, sent_at))
            self.c.commit()
            print("New chat started successfully.")

    # Function to get all conversations ordered by date
    def get_all_conversations(self):
        self.c.execute('''
            SELECT chat_id, about
            FROM chats
            ORDER BY created_at
        ''')
        conversations = self.c.fetchall()
        for conversation in conversations:
            print(conversation)

    # Insert a new user if not exists
    def insert_user(self, username):
        self.c.execute('''
            SELECT user_id FROM users WHERE username=?
        ''', (username,))
        existing_user = self.c.fetchone()
        if existing_user:
            print(f"{username} already exists.")
        else:
            created_at = datetime.now()
            self.c.execute('''
                INSERT INTO users (username, created_at)
                VALUES (?, ?, ?)
            ''', (username, created_at))
            self.c.commit()
            print(f"{username} created successfully.")

    # Delete an existing user
    def delete_user(self, user_id):
        self.c.execute('''
            DELETE FROM users WHERE user_id=?
        ''', (user_id,))
        self.c.commit()