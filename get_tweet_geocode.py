import sys
import sys
import twitter
from twitter_login import login


q = ""
count = 1000
geocode = '50.986099,10.144501,1000km'
MAX_PAGES = 10

t = login()

search_results = t.search.tweets(q=q, geocode=geocode, count=count)

#print >> sys.stderr, search_results

statuses = search_results['statuses']

assert len(statuses) > 0, "No need to continue. There were no tweets for this query"

for _ in range(MAX_PAGES-1): 
    next_results = search_results['search_metadata']['next_results']
    kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ]) # Create a dictionary from the query string params
    search_results = t.search.tweets(**kwargs)
    statuses += search_results['statuses']
    if len(search_results['statuses']) == 0:
        break
    print 'Fetched %i tweets so far' % (len(tweets),)
    
import json
#print json.dumps(statuses[0:1], indent=1)


tweets = [ status['text'] for status in statuses ]

print tweets[0]

words = []
for t in tweets:
    words += [ w for w in t.split() ]

# total words
print len(words) 

# unique words
print len(set(words)) 

# lexical diversity
print 1.0*len(set(words))/len(words) 

# avg words per tweet
print 1.0*sum([ len(t.split()) for t in tweets ])/len(tweets) 

import nltk

freq_dist = nltk.FreqDist(words)
print freq_dist.keys()[:50] # 50 most frequent tokens
print freq_dist.keys()[-50:] # 50 least frequent tokens
