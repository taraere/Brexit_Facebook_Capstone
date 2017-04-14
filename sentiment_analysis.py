from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
import string
import csv

CSV_FILE = "./../resources/KeepBritainInEurope_facebook_comments.csv"
TEXT_COLUMN = "comment_message"
DATE_COLUMN = "comment_published"

def compound_sentiment_sentence(analyzer, sentence):
    return float(analyzer.polarity_scores(sentence).get("compound"))


analyzer = SentimentIntensityAnalyzer()


date_sentiment_dict = {}

with open(CSV_FILE, 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        sentence = row[TEXT_COLUMN]
        date = row[DATE_COLUMN]
        sentiment = compound_sentiment_sentence(analyzer, sentence)

        if not date_sentiment_dict.has_key(date):
            date_sentiment_dict[date] = []

        date_sentiment_dict[date].append(sentiment)

        print date_sentiment_dict
        break

