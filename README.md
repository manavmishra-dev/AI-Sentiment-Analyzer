🤖 AI-Powered Financial News Sentiment Analyzer
Live Demo: [Link to your deployed Streamlit App will go here]

🚀 Overview
This web application provides real-time sentiment analysis for financial news related to any stock ticker. It was built to demonstrate skills in Python, AI/ML model integration, API usage, and modern web app development. The app fetches the latest news headlines and uses a sophisticated AI model (FinBERT), specifically trained on financial text, to score each headline as positive, negative, or neutral.

This project fulfills a key promise made on my professional CV and showcases my ability to rapidly build and deploy data-driven tools.

✨ Features
Real-Time News: Fetches the latest financial news from the past 7 days using the NewsAPI.

Advanced AI Analysis: Utilizes the ProsusAI/finbert model for highly accurate sentiment scoring on financial language.

Interactive Dashboard: Clean, user-friendly interface built with Streamlit.

Data Visualization: Displays sentiment distribution with clear metrics and charts.

Detailed Breakdown: Provides a table of all headlines, their sentiment scores, confidence levels, and direct links to the articles.

🛠️ Tech Stack
Language: Python

Web Framework: Streamlit

AI/ML: Hugging Face Transformers, PyTorch

Data Handling: Pandas

APIs: NewsAPI

⚙️ How to Run Locally
1. Clone the repository:

   git clone [https://github.com/manavmishra-dev/AI-Sentiment-Analyzer.git](https://github.com/manavmishra-dev/AI-Sentiment-Analyzer.git)

2. Navigate to the directory:

   cd AI-Sentiment-Analyzer

3. Install dependencies:

   pip install -r requirements.txt

4. Create your secrets file:

   Create a folder: .streamlit

   Inside it, create a file: secrets.toml

   Add your API key: NEWS_API_KEY = "YOUR_KEY_HERE"

5. Run the Streamlit app:

   streamlit run app.py
