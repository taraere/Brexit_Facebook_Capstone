from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
import string
import csv

CSV_FILE = "KeepBritainInEurope_facebook_statuses"
TEXT_COLUMN = "status_message"
DATE_COLUMN = "status_published"
# CSV_FILE = "KeepBritainInEurope_facebook_comments"
# TEXT_COLUMN = "comment_message"
# DATE_COLUMN = "comment_published"

ROOT = "/Users/Tara/Desktop/C/Writing/sentiment analysis"
INPUT_FILE = ROOT + "/resources/" + CSV_FILE + ".csv"
OUTPUT_FILE = ROOT + "/sentiment/" + "sentiment_" + CSV_FILE + ".csv"

def sentiment_sentence(analyser, sentence):
    return analyser.polarity_scores(sentence)

def compound_sentiment_sentence(analyser, sentence):
    return float(sentiment_sentence(analyser, sentence).get("compound"))

def positive_sentiment_sentence(analyser, sentence):
    return float(sentiment_sentence(analyser, sentence).get("pos"))

def negative_sentiment_sentence(analyser, sentence):
    return float(sentiment_sentence(analyser, sentence).get("neg"))

def neutral_sentiment_sentence(analyser, sentence):
    return float(sentiment_sentence(analyser, sentence).get("neu"))

def mean(lovalues, roundby = 2):
    return round(sum(lovalues)/len(lovalues), roundby)

analyser = SentimentIntensityAnalyzer()
date_sentiment_dict = {}

# read csv and assigns sentiment to date
counter = 0
with open(INPUT_FILE, 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        sentence = row[TEXT_COLUMN]
        dateTime = row[DATE_COLUMN]
        date = dateTime[0:10]
        compound = compound_sentiment_sentence(analyser, sentence)
        positive = positive_sentiment_sentence(analyser, sentence)
        negative = negative_sentiment_sentence(analyser, sentence)
        neutral = neutral_sentiment_sentence(analyser, sentence)

        # puts empty dictionary for date if it is not present
        # and initialises empty arrays for the keys
        if not date_sentiment_dict.has_key(date):
            date_sentiment_dict[date] = {}
            date_sentiment_dict[date]["compound"] = []
            date_sentiment_dict[date]["positive"] = []
            date_sentiment_dict[date]["negative"] = []
            date_sentiment_dict[date]["neutral"] = []

        date_sentiment_dict[date]["compound"].append(compound)
        date_sentiment_dict[date]["positive"].append(positive)
        date_sentiment_dict[date]["negative"].append(negative)
        date_sentiment_dict[date]["neutral"].append(neutral)

        # counter += 1
        # if counter == 10:
        #     print date_sentiment_dict
        #     break

writer = csv.writer(open(OUTPUT_FILE, "wb"), delimiter=',', quotechar='', quoting=csv.QUOTE_NONE)

# # write header.
# writer.writerow(["date", "compound_sentiment", "num_negative", "num_positive", "num_neutral"])

# write header
writer.writerow(["date", "num_comments", "mean_compound", "num_positive", "mean_positive", "mean_positive", "num_negative", "mean_negative", "num_neutral", "mean_neutral"])

# write rows
for dateKey in sorted(date_sentiment_dict.keys()):
    meanCompound = mean(date_sentiment_dict[dateKey]["compound"], 3)
    meanPositive = mean(date_sentiment_dict[dateKey]["positive"], 3)
    meanNegative = mean(date_sentiment_dict[dateKey]["negative"], 3)
    meanNeutral = mean(date_sentiment_dict[dateKey]["neutral"], 3)

    numComments = len(date_sentiment_dict[dateKey]["compound"])
    numPositive = len({x for x in date_sentiment_dict[dateKey]["positive"] if x > 0})
    numNegative = len({x for x in date_sentiment_dict[dateKey]["negative"] if x > 0})
    numNeutral = len({x for x in date_sentiment_dict[dateKey]["neutral"] if x > 0})
    writer.writerow([dateKey, numComments, meanCompound, numPositive, meanPositive, numNegative, meanNegative, numNeutral, meanNeutral])

print len(date_sentiment_dict)
print date_sentiment_dict.keys()
print OUTPUT_FILE
