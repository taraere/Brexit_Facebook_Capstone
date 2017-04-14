from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def compound_sentiment_sentence(analyzer, sent):
    return float(analyzer.polarity_scores(sent).get("compound"))

analyzer = SentimentIntensityAnalyzer()
sentence = "The great company Apple is doing well considering the very bad economy."

print compound_sentiment_sentence(analyzer, sentence)


