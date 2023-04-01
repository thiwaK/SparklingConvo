# 🤖 SparklingConvo

SparklingConvo is a Python-based Flask web app that connects to OpenAI's GPT-3 API and enables you to communicate with an AI chatbot in a variety of media formats including text, images, and audio.

## 📦 Dependencies
Before running this application, please make sure that you have the following dependencies installed:
- Python 3 🐍
- Flask 🌶️
- OpenAI API key 🔑

## 🚀 Getting Started
1. Clone or download the SparklingConvo repository to your local machine.
2. Add your OpenAI API key to the `settings.config` file located in the root directory.
~~3. Install the necessary dependencies by running `pip install -r requirements.txt` in your terminal.~~
4. Start the application by running `python app.py` in your terminal.

### ⚙️ Configuration file
Create `settings.config` on the root directory and add your OpenAi API key as follows.

```json
{
	"openai_key":"Your-API-Key"
}
```

If you don't have a key, use [this link](https://platform.openai.com/account/api-keys) to get one.


## 💻 Usage
Once the application is running, open your web browser and go to `http://localhost:5000`. From there, you can start communicating with the chatbot by typing in your messages and sending them.


## 🤝 Contributor
- Thiwanka Kaushal