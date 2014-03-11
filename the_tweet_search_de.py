import sys
import twitter
import couchdb
from couchdb.design import ViewDefinition
from twitter_login import login

Q = ""
MAX_PAGES = 10
#result_type = 'recent'

server = couchdb.Server('http://localhost:5984')
DB = 'de-%s' % (Q.lower().replace('#', '').replace('@', ''), )

t = login()
search_results = t.search.tweets(q=Q, lang='de', until='2013-07-19', count=10)
tweets = search_results['statuses']

for _ in range(MAX_PAGES-1): # Get more pages
    next_results = search_results['search_metadata']['next_results']

    # Create a dictionary from the query string params
    kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ]) 

    search_results = t.search.tweets(**kwargs)
    tweets += search_results['statuses']

    if len(search_results['statuses']) == 0:
        break

    print 'Fetched %i tweets so far' % (len(tweets),)

# Store the data
try:
    db = server.create(DB)
except couchdb.http.PreconditionFailed, e:
    # Already exists, so append to it (but be mindful of appending duplicates with repeat searches.)
    # The refresh_url in the search_metadata or streaming API might also be
    # appropriate to use here.
    db = server[DB]

db.update(tweets, all_or_nothing=True)
print 'Done. Stored data to CouchDB - http://localhost:5984/_utils/database.html?%s' % (DB,)
