# Simple Chatbot
This project implements a chatbot that provides weather information and performs web searches based on user queries. It uses web scraping to gather content, summarizes it, and presents relevant details. The chatbot also includes source citations.

## Features
1. Weather Query:
The chatbot fetches real-time weather data based on user-provided locations using the python-weather library. This library depends on wttr.in, which in turn uses data from the World Weather Online API. It returns information like temperature, chances of raining, and sunlight hours.
2. General Query (Web Search and Summarization):
The chatbot allows users to enter general queries (e.g., "What is quantum computing?").
The chatbot performs a web search, scrapes the top articles, and summarizes the content into concise key points.
For each query, the chatbot provides:
* A summary of the information pulled from the web.
* Citations of the sources where the data was gathered.

# Installation
* Clone the repository:
--> git clone https://github.com/yourusername/simple-chatbot.git
--> cd chatbot
* Install dependencies: Make sure you have Python 3.7+ installed, then run:
--> pip install -r requirements.txt
* Run the app: Start the chatbot application:
--> py main.py
* Access the chatbot: After running the app, you should see something like:
  "* Running on local URL:  http://127.0.0.1:7860"
--> Copy and paste the URL into your browser to interact with the chatbot.

# Note
* Responses in general query may take a few minutes to generate, this is due to the extensive web scraping being executed one by one to not overwhelm the server and not get banned. Please be patient.

# Future Improvements
* User Personalization: Add the ability for users to save preferences or past queries for a personalized experience.
* Advanced Summarization: Improve the summarization algorithm to handle more complex topics and provide more concise answers.
* Expanded Knowledge Base: Integrate additional data sources for broader and more accurate information across different domains.
* Multi-language Support: Implement multi-language capabilities to make the chatbot accessible to non-English speakers.
* Voice Integration: Allow users to interact with the chatbot using voice commands.
* Sentiment Analysis: Add sentiment analysis to provide feedback on the tone of user queries or responses.
* NLP Intent Classification: Implement intent classification to identify specific user intentions (e.g., weather query, general knowledge, etc.) and improve response accuracy by tailoring the behavior of the chatbot to different types of requests.
* Contextual Conversation Flow: Enhance the chatbot’s ability to maintain context over multiple interactions, providing more natural conversations.
* Additional Features: Add more features that improve the chatbot's capabilities, such as real-time data updates, deeper integration with external APIs, and other intelligent functionalities.
