import snscrape.modules.twitter as sntwitter
import pandas as pd
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
import datetime

query = "Real World Assert "

df = []

for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
    if i > 2000:
        break
    df.append([tweet.id, tweet.date, tweet.source, tweet.place, tweet.user.username, tweet.rawContent, tweet.hashtags, tweet.likeCount])

data = pd.DataFrame(df, columns=['id', 'date', 'source', 'place', 'username', 'content', 'hashtags', 'likes'])

# Download stopwords if not already downloaded
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Define a function to preprocess text
def preprocess_text(text):
    tokens = [token for token in word_tokenize(text.lower()) if token.isalpha() and not token.startswith(('http', 'www'))]
    tokens = [token for token in tokens if token not in stop_words]
    return ' '.join(tokens)

# Preprocess content
data['clean_content'] = data['content'].apply(preprocess_text)

# Calculate TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['clean_content'])

# Get important words
important_words = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())
top_words = important_words.sum().sort_values(ascending=False).head(10)
print("Top words:", top_words)

# Sentiment analysis
data['sentiment'] = data['clean_content'].apply(lambda x: TextBlob(x).sentiment.polarity)

# Group tweets by date
data['date'] = pd.to_datetime(data['date']).dt.date
grouped_data = data.groupby(['date']).agg({'id': 'count', 'sentiment': 'mean', 'likes': 'sum'}).reset_index()
grouped_data.columns = ['date', 'tweet_count', 'avg_sentiment', 'total_likes']

# Save insights to CSV
data.to_csv('RWA_narrative_insights.csv', index=False)
grouped_data.to_csv('RWA_narrative_grouped_insights.csv', index=False)
