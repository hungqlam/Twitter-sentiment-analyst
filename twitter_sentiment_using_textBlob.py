import re
import emoji
from textblob import TextBlob
import snscrape.modules.twitter as sntwitter
import pandas as pd


# Define your Twitter query
query = "$ARB"

# Set a limit on the number of tweets to retrieve
limit = 100

# Retrieve the tweets that match your query and meet your criteria for number of likes
tweets = []
for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    if len(tweets) == limit:
        break
    elif tweet.likeCount >= 50:
        # Clean the tweet text using regular expressions
        cleaned_text = re.sub(r'http\S+', '', tweet.rawContent)  # Remove URLs
        cleaned_text = re.sub(r'\n', ' ', cleaned_text)  # Remove newlines
        cleaned_text = re.sub(r'@[A-Za-z0-9_]+', '', cleaned_text)  # Remove mentions
        #cleaned_text = re.sub(r'#', '', cleaned_text)  # Remove hashtags
        cleaned_text = re.sub(r'RT : ', '', cleaned_text)  # Remove retweet prefix
        cleaned_text = ''.join(c for c in cleaned_text if c <= '\uFFFF')  # Remove non-English characters
        cleaned_text = emoji.emojize(cleaned_text, language='alias')  # Replace emojis with their corresponding text descriptions
        cleaned_text = cleaned_text.encode('ascii', 'ignore').decode('utf-8')  # Remove any remaining non-ASCII characters
        tweets.append([tweet.date, tweet.user.username, cleaned_text, tweet.likeCount])

# Create a pandas dataframe from the tweets
df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet', 'Favorite'])

# Define a function to perform sentiment analysis on a text input using TextBlob
def get_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score < 0:
        return 'negative'
    elif sentiment_score == 0:
        return 'neutral'
    else:
        return 'positive'

# Apply the sentiment analysis function to the 'Tweet' column of the dataframe
df['Sentiment'] = df['Tweet'].apply(get_sentiment)

# Export the dataframe to a CSV file
df.to_csv('twitter_data_textBlob.csv', index=False)
