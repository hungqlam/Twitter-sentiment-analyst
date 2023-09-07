# Twitter-sentiment-analyst
## README for Twitter Sentiment Analysis Tools

---

### Description

This repository offers a collection of scripts tailored for sentiment analysis on Twitter data. The tools range from collecting tweets based on specific queries to performing sentiment analysis on the collected data.

### Requirements

- Python 3.x
- pandas
- snscrape
- textblob
- nltk
- emoji
- re

### Scripts Overview

1. **test_ARIMAmodel.py**: 
    - A simple script to download the 'punkt' tokenizer models from the NLTK library.
    
    
2. **tweet.py**: 
    - This script uses the `snscrape` library to scrape tweets from Twitter.
    - Targets tweets related to the query "$LSD".
    - Collects a maximum of 5000 tweets and saves them to 'LSD.csv'.
   

3. **twitter_sentiment_using_textBlob.py**: 
    - Retrieves tweets based on the query "$ARB".
    - Includes a tweet preprocessing phase, removing URLs, mentions, newlines, retweet prefixes, and more.
    - Uses `textblob` for sentiment analysis on cleaned tweets.


### How to Run

1. Ensure you have all the required libraries installed.
2. Clone the repository and navigate to the project directory.
3. Run the desired script using:

```bash
python <script_name>.py
```

For example:

```bash
python tweet.py
```

### Contributions

Feel free to fork this repository and contribute. If you find any bugs or have feature suggestions, please open an issue. Pull requests are also welcome.

---

