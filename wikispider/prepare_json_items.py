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

json_data = open('items_all.json')

deny_pages = (
    'wiki_meet_',
    'category:',
    'fs_weekly_',
    'variable_',
    'file:',
    )

data = json.load(json_data)
data_unique = []
# We will create a list of all the pages linking to a page
# that way we can easily know which are all the page pointing
# to the page MYPAGE with -> list_links[MYPAGE]
list_links = {}
list_pages = Set()
with open('unique_pages.csv', 'wb') as csvfile:
    for line in data:
        # pprint(line)
        pagename = line['pageurl'][32:]

        if pagename.lower().startswith(deny_pages):
            #handle deny pages
            continue
        pagename.replace("http://wiki.freeswitch.org/wiki/", "")
        pagename.replace("https://wiki.freeswitch.org/wiki/", "")
        pageurl = line['pageurl']
        pageurl = pageurl.replace("http://wiki.freeswitch.org/wiki/", "https://wiki.freeswitch.org/wiki/")
        pageurl_secret = pageurl.replace("https://wiki.freeswitch.org/wiki/", "https://70.169.193.216/wiki/")

        if pagename.lower() not in list_pages:
            #create data_unique
            title = line['title'][0].replace(" - FreeSWITCH Wiki", "")
            data_unique.append({
                               "pageurl": pagename,
                               "title": title,
                               "links": line['links'],
                               })

            list_pages.add(pagename.lower())
            for link in line['links']:
                # remove the /wiki/
                sanlink = link.replace("/wiki/", "")
                if sanlink.find("#") != -1:
                    sanlink = sanlink[0:sanlink.find("#")]
                # pagename ->> many links
                if sanlink not in list_links:
                    list_links[sanlink] = Set()
                list_links[sanlink].add(pagename)

            # Write unique to csv
            # Csv will be used for import into Spreadsheet
            pageswriter = csv.writer(csvfile, delimiter=',')
            pageswriter.writerow([pageurl, pagename, pageurl_secret])
        else:
            # print "Duplicate record : %s" % pagename
            continue

# Group list
group_list = {
    "Category": "Category",
    "variable": "Variable",
    "FS_weekly": "Weekly Conf",
    "Mod_": "Modules",
    "Misc": "Misc",
    "Javascript_": "Javascript",
    "File:": "File",
    "Examples_": "Examples",
    "Dialplan_": "Dialplan",
    "Channel_": "Channel",
    "default": "Others",
}

# pprint(list_pages)
print "list pages -> # %d" % len(list_pages)
print "list data unique -> # %d" % len(data_unique)

dataset = {}
list_relation = []
list_relation.append(["source", "target", "value"])
for line in data_unique:
    pagename = line['pageurl']
    #Set group for pages
    group = "Others"
    for key in group_list.keys():
        if pagename.find(key) != -1:
            group = group_list[key]
            break

    # dependedOnBy -> link to page
    depends = []
    if pagename in list_links:
        #For the visualization to work we need to ensure that the links we will display have existing pages:
        for currentlinks in list(list_links[pagename]):
            if currentlinks.lower() in list_pages and currentlinks != pagename:
                depends.append(currentlinks)
            # else:
            #     print currentlinks

    # dependedOnBy -> link to page
    dependedonby = []
    for link in set(line['links']):
        sanlink = link.replace("/wiki/", "")
        # Remove anchor
        if sanlink.find("#") != -1:
            sanlink = sanlink[0:sanlink.find("#")]
        #handle deny pages
        if sanlink.lower().startswith(deny_pages):
            continue
        list_relation.append([pagename, sanlink, 1])
        dependedonby.append(sanlink)

    dataset[pagename] = {
        "name": pagename,
        "type": group,
        "depends": depends,
        "dependedOnBy": dependedonby,
        "docs": ""
    }
json_data.close()

data = {'data' : dataset, 'errors' : []}
# pprint(list_relation)
with open('../d3-noob/force_wiki.csv', 'w') as csvfile:
    relfile = csv.writer(csvfile)
    # relfile.writerows({"source", "target", "value"})
    relfile.writerows(list_relation)

outputfilename = '../d3-process-map/wikidataset.json'
with open(outputfilename, 'wb') as outfile:
    json.dump(data, outfile)
