from vaderSentiment.vaderSentiment import SentimentIntensityanalyser
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
import string
import csv

# CSV_FILE = "KeepBritainInEurope_facebook_statuses"
# TEXT_COLUMN = "status_message"
# DATE_COLUMN = "status_published"
CSV_FILE = "KeepBritainInEurope_facebook_comments"
TEXT_COLUMN = "comment_message"
DATE_COLUMN = "comment_published"

ROOT = "/Users/Tara/Desktop/C/Writing/sentiment analysis"
INPUT_FILE = ROOT + "/resources/" + CSV_FILE + ".csv"
OUTPUT_FILE = ROOT + "/sentiment/" + "sentiment_" + CSV_FILE + ".csv"

def sentiment_sentence(analyser, sentence):
    return analyser.polarity_scores(sentence)
    
def compound_sentiment_sentence(analyser, sentence):
    return float(sentiment_sentence(analyser, sentence).get("compound"))

def positive_sentiment_sentence(analyser, sentence):
    return float(sentiment_sentence(analyser, sentence).get("positive"))

def negative_sentiment_sentence(analyser, sentence):
    return float(sentiment_sentence(analyser, sentence).get("negative"))

def mean(lovalues, roundby = 2):
    return round(sum(lovalues)/len(lovalues), roundby)

analyser = SentimentIntensityanalyser()
date_sentiment_dict = {}

# read csv and assigns sentiment to date
counter = 0
with open(INPUT_FILE, 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        sentence = row[TEXT_COLUMN]
        dateTime = row[DATE_COLUMN]
        date = dateTime[0:10]
        sentiment = compound_sentiment_sentence(analyser, sentence)

        # puts empty array at date if not present
        if not date_sentiment_dict.has_key(date):
            date_sentiment_dict[date] = []

        date_sentiment_dict[date].append(sentiment)


        # counter += 1
        # if counter == 10:
        #     print date_sentiment_dict
        #     break


writer = csv.writer(open(OUTPUT_FILE, "wb"), delimiter=',', quotechar='', quoting=csv.QUOTE_NONE)

# write header
writer.writerow(["date", "sentiments"])

# write rows
for key in sorted(date_sentiment_dict.keys()):
    value = mean(date_sentiment_dict[key], 3)
    writer.writerow([key, value])

print len(date_sentiment_dict)
print date_sentiment_dict.keys()
