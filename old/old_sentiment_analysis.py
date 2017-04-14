'''
from nltk import word_tokenize
from nltk.tokenize import sent_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import string

trump = "trump"
clinton = "clinton"
clinton_identifiers = ['clinton', 'clintons', 'hillary', 'democrat', 'democrats']
trump_identifiers = ['trump', 'trumps', 'donald', 'republican', 'republicans']

def avg(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def sentences_contain(identifiers, sentences):
    return [sentence for sentence in sentences if any(identifier.lower() in sentence.split(' ') for identifier in identifiers)]

def compound_sentiment_sentence(analyzer, sentence):
    return float(analyzer.polarity_scores(sentence).get("compound"))

def compound_sentiment_sentences(analyzer, text):
    compound_scores = []
    for sentence in text:
        compound_scores.append(compound_sentiment_sentence(analyzer, sentence))
    return avg(compound_scores) # normalize score


analyzer = SentimentIntensityAnalyzer()
printable = set(string.printable)
# result map in format:
#   {
#       date1: {
#           'trump': [score_1, score_2, .. score_n-1]
#           'clinton': [score_1, score_2, .. score_n-1]
#       }
#       date2: etc..
#   }
result_map = {}

i = 1
for date, articles in article_dict.items():
    if i > 1 : break
    # articles is still a list of articles on that date
    print date
    # initialize result map for date
    result_map[date] = {}
    result_map[date][trump] = []
    result_map[date][clinton] = []

    for article in articles:
        # + remove all punctuation: Trump. is not Trump
        # to ignore characters that cannot be printed in printable.
        sent_tokenize_list = [x.translate(None, string.punctuation).lower() for x in sent_tokenize(filter(lambda x: x in printable, article))]

        # retrieve sentences that talk about trump or clinton
        # both will contain sentences that mention both Clinton and Trump, but because they are present in both they cancel eachother out
        # one could opt to remove them to increase processing speed or handle them in a more sophisticated manner so they actually contribute to the score
        sentences_with_trump = sentences_contain(trump_identifiers, sent_tokenize_list)
        sentences_with_clinton = sentences_contain(clinton_identifiers, sent_tokenize_list)

        # calculate polarity scores for both candidates
        polarity_score_trump = compound_sentiment_sentences(analyzer, sentences_with_trump)
        polarity_score_clinton = compound_sentiment_sentences(analyzer, sentences_with_clinton)

        # append score to result map
        result_map[date][trump].append(polarity_score_trump)
        result_map[date][clinton].append(polarity_score_clinton)

    i+1

def total_score_candidate(candidate, result_map):
    total_scores = []
    for date, scoreMap in result_map.items():
        total_scores.extend(scoreMap[candidate])
    return round(avg(total_scores), 3) # normalize score

print result_map
print "Total score ", trump, ": ", total_score_candidate(trump, result_map)
print "Total score ", clinton, ": ", total_score_candidate(clinton, result_map)

print "Normalized score per date (neutral scores ignored):"
print "date trump hillary"
for date, scoreMap in result_map.items():
    print date, avg([x for x in scoreMap[trump] if x != 0]), avg([x for x in scoreMap[clinton] if x != 0])
print ""

print "Normalized score per date (neutral scores included):"
print "date trump hillary"
for date, scoreMap in result_map.items():
    print date, avg(scoreMap[trump]), avg(scoreMap[clinton])
print ""

print "Absolute number of positive, neutral, and negative articles per candidate per date"
print "date trump_neg trump_neu trump_pos clinton_neg clinton_neu clinton_pos"
for date, scoreMap in result_map.items():
    print date, len([x for x in scoreMap[trump] if x < 0]), len([x for x in scoreMap[trump] if x == 0]), len([x for x in scoreMap[trump] if x > 0]), len([x for x in scoreMap[clinton] if x < 0]), len([x for x in scoreMap[clinton] if x == 0]), len([x for x in scoreMap[clinton] if x > 0])

# In[ ]:
'''