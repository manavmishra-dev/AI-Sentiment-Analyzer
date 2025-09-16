import streamlit as st
from transformers import pipeline
import requests
import pandas as pd
from datetime import datetime, timedelta

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI Financial News Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODEL LOADING (Cached for performance) ---
# Using a specific model trained on financial news
@st.cache_resource
def load_model():
    model = pipeline("sentiment-analysis", model="ProsusAI/finbert")
    return model

sentiment_model = load_model()

# --- API KEY & NEWS FETCHING ---
NEWS_API_KEY = st.secrets["NEWS_API_KEY"]

@st.cache_data(ttl=600) # Cache data for 10 minutes
def fetch_news(stock_ticker):
    """Fetches financial news for a given stock ticker."""
    try:
        # Search for news from the last 7 days
        to_date = datetime.now().strftime('%Y-%m-%d')
        from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        url = (f"https://newsapi.org/v2/everything?"
               f"q={stock_ticker}&"
               f"from={from_date}&"
               f"to={to_date}&"
               f"language=en&"
               f"sortBy=publishedAt&"
               f"apiKey={NEWS_API_KEY}")
        
        response = requests.get(url)
        response.raise_for_status() # Raises an exception for bad responses
        articles = response.json().get("articles", [])
        return articles
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching news: {e}. Check your API key and internet connection.")
        return []

# --- MAIN APP LAYOUT ---
st.title("🤖 AI-Powered Financial News Sentiment Analyzer")
st.markdown("Analyze the market sentiment for any stock based on the latest news headlines. A project by **Manav Mishra**.")

# --- SIDEBAR ---
st.sidebar.header("Controls")
ticker_input = st.sidebar.text_input("Enter a Stock Ticker (e.g., GOOGL, AAPL, MSFT)", "GOOGL").upper()
analyze_button = st.sidebar.button("Analyze Sentiment", type="primary")

st.sidebar.markdown("---")
st.sidebar.info(
    "This app uses the **ProsusAI/finbert** model, a powerful AI specifically "
    "trained on financial text to understand the nuances of market sentiment."
)

# --- ANALYSIS AND DISPLAY ---
if analyze_button:
    if NEWS_API_KEY == "YOUR_NEWS_API_KEY" or not NEWS_API_KEY:
        st.error("Please replace 'YOUR_NEWS_API_KEY' in the code with your actual key from newsapi.org.")
    else:
        with st.spinner(f"Fetching news and analyzing sentiment for {ticker_input}..."):
            news_articles = fetch_news(ticker_input)

            if not news_articles:
                st.warning("No recent news articles found for this ticker. Please try another one.")
            else:
                headlines = [article['title'] for article in news_articles if article['title']]
                sentiments = sentiment_model(headlines)

                # Combine results for display
                results = []
                for article, sentiment in zip(news_articles, sentiments):
                    results.append({
                        "Date": pd.to_datetime(article['publishedAt']).strftime('%Y-%m-%d'),
                        "Headline": article['title'],
                        "Sentiment": sentiment['label'].capitalize(),
                        "Confidence": sentiment['score'],
                        "Link": article['url']
                    })

                df = pd.DataFrame(results)

                # --- DISPLAY METRICS AND CHARTS ---
                st.header(f"Sentiment Analysis for {ticker_input}")

                # Metrics
                col1, col2, col3 = st.columns(3)
                positive_count = df[df['Sentiment'] == 'Positive'].shape[0]
                neutral_count = df[df['Sentiment'] == 'Neutral'].shape[0]
                negative_count = df[df['Sentiment'] == 'Negative'].shape[0]
                
                col1.metric("Positive Headlines", f"{positive_count}")
                col2.metric("Neutral Headlines", f"{neutral_count}")
                col3.metric("Negative Headlines", f"{negative_count}")

                # Donut Chart
                sentiment_counts = df['Sentiment'].value_counts()
                st.write("#### Sentiment Distribution")
                st.bar_chart(sentiment_counts)
                
                # --- DISPLAY DATA TABLE ---
                st.write("#### Detailed News Analysis")
                st.dataframe(
                    df,
                    column_config={
                        "Link": st.column_config.LinkColumn("Article Link", display_text="Read Article"),
                        "Confidence": st.column_config.ProgressColumn(
                            "Confidence Score",
                            format="%.2f",
                            min_value=0,
                            max_value=1,
                        ),
                    },
                    hide_index=True,
                    use_container_width=True
                )
