#
# Usage: python prepare_json_items.py
#
# This script take the json data from the Web scraper (Scrapy) and transform it into
# an other json object that we could use for visualization.
# We need this new object to build up the relation between the page, by default we know where a
# page points to other pages but we dont know which pages point to them
#
# We need to :
# remove duplicate from items_all.json

import json
from sets import Set
from pprint import pprint
import csv

json_data = open('items_specialall2.json')

data = json.load(json_data)
data_unique = []
# We will create a list of all the pages linking to a page
# that way we can easily know which are all the page pointing
# to the page MYPAGE with -> list_links[MYPAGE]
list_pages = Set()
with open('wikisheet.csv', 'rb') as csvfile:
    wikireader = csv.reader(csvfile, delimiter=',')
    for row in wikireader:
        pagename = row[0]
        list_pages.add(pagename)

#loop in json now
for line in data:
    # pprint(line)
    # pagename = line['pageurl'][32:]
    pagename = line['pageurl']
    if pagename not in list_pages:
        print pagename

json_data.close()
