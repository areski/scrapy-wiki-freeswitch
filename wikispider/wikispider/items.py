# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class WikiItem(Item):
    """
    Definition of all the fields we want to extract from wiki.freeswitch.org webpage.
    """
    title = Field()
    pageurl = Field()
    links = Field()
    desc = Field()
    content = Field()


class IsBullshitItem(Item):
    """
    Definition of all the fields we want to extract from a scraped webpage.
    """
    title = Field()
    author = Field()
    tag = Field()
    date = Field()
    url = Field()
    location = Field()
    article_html = Field()
