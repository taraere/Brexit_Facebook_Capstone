
# coding: utf-8

# ## This cell scrapes the articles

# In[11]:

import json
import os
import requests
from datetime import date, timedelta
import os
# don't forget the slash
root = 'E:/Tom/Junk/tara_py/files/'


# In[8]:

# Sample URL
#
# http://content.guardianapis.com/search?from-date=2016-01-02&
# to-date=2016-01-02&order-by=newest&show-fields=all&page-size=200
# &api-key=your-api-key-goes-here

API_ENDPOINT = 'http://content.guardianapis.com/search'
my_params = {
    'q': "Clinton OR Trump",
    'from-date': "",
    'to-date': "",
    'order-by': "newest",
    'show-fields': 'all',
    'page-size': 200,
    'api-key': 'ac929774-d2b1-4586-8fad-45998b5e624b'
}

# day iteration from here:
# http://stackoverflow.com/questions/7274267/print-all-day-dates-between-two-dates

# SET YOUR DATES HERE
start_date = date(2016, 10, 1)
end_date = date(2016,11,1)

dayrange = range((end_date - start_date).days + 1)
for daycount in dayrange:
    dt = start_date + timedelta(days=daycount)
    datestr = dt.strftime('%Y-%m-%d')
    fname = os.path.join(root, datestr + '.json')
    if not os.path.exists(fname):
        # then let's download it
        print("Downloading", datestr)
        all_results = []
        my_params['from-date'] = datestr
        my_params['to-date'] = datestr
        current_page = 1
        total_pages = 1
        while current_page <= total_pages:
            print("...page", current_page)
            my_params['page'] = current_page
            resp = requests.get(API_ENDPOINT, my_params)
            data = resp.json()
            all_results.extend(data['response']['results'])
            # if there is more than one page
            current_page += 1
            total_pages = data['response']['pages']

        with open(fname, 'w') as f:
            print("Writing to", fname)

            # re-serialize it for appealing indentation
            f.write(json.dumps(all_results, indent=2))


# ## This cell reads the json files

# In[9]:

import json
from bs4 import BeautifulSoup

import re

# regex example
string = "<a href=\"dsafsadf\"> bkasdlfjaksldf </a> dsafsdafasf as dsafsa"
html_regex = '<(?:[^>=]|=\'[^\']*\'|="[^"]*"|=[^\'"][^\s>]*)*>'
# print str(re.sub(html_regex, "", string))

article_dict = {}

# REMOVE THE I CONDITION TO GO THROUGH EVERY ARTICLE
i = 0
for f in os.listdir(root):
    print f
    if f[-4:] == 'json' and i < 2:
        with open(root+f, "r") as f:
            data = json.loads(f.read())
            
            # print all the dicts in that list
            for news_article in data:
                date = news_article['fields']['firstPublicationDate']
                # keep unnecessary date format
                date = date.rpartition('T')[0]
                # extract the data
                news_article = news_article['fields']['body'].encode('ascii', 'ignore')
                
                # create soup object
                soup = BeautifulSoup(news_article)
                
                # compile the text of the current article
                currentarticle = ""
                for x in soup.findAll('p'):
                    # strip all html tags
                    currentarticle += str(re.sub(html_regex, " ", str(x)))
                    
                if date in article_dict:
                    article_dict[date] = article_dict[date] + [currentarticle]
                else:
                    article_dict[date] = [currentarticle]

            
# ARTICLE_DICT = {date, [list of articles]}
# on this  article on this date about trump / clinton
print "On 2016-03-01 we have this many articles about trump or clinton:"
print len(article_dict['2016-10-01'])
# the first of them (the first element is [] for some reason)
print "the first article is:"
print article_dict['2016-10-01'][1]
            



# ## Tokenize articles into sentences

# In[10]:

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



