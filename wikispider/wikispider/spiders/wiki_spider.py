from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
# from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from wikispider.items import WikiItem


class WikiSpider(CrawlSpider):
    pcounter = 0
    name = "wiki"
    allowed_domains = ["freeswitch.org"]
    # start_urls = [
    #     "http://wiki.freeswitch.org/"
    # ]
    start_urls = [
        "http://wiki.freeswitch.org/index.php?title=Special:AllPages&from=.1.3.6.1.4.1.27880&to=FS_weekly_2010_11_10",
        "http://wiki.freeswitch.org/index.php?title=Special:AllPages&from=FS_weekly_2010_11_17&to=Java_ESL_Client",
        "http://wiki.freeswitch.org/index.php?title=Special:AllPages&from=Javascript&to=Mod_managed",
        "http://wiki.freeswitch.org/index.php?title=Special:AllPages&from=Mod_memcache&to=Report_Issue_Checklist",
        "http://wiki.freeswitch.org/index.php?title=Special:AllPages&from=Reporting_Bugs&to=Variable_execute_on_tone_detect",
        "http://wiki.freeswitch.org/index.php?title=Special:AllPages&from=Variable_export_vars&to=Variable_stream_prebuffer",
        "http://wiki.freeswitch.org/index.php?title=Special:AllPages&from=Variable_suppress-cng&to=Zeroconf.conf.xml"
    ]

    # rules = (
    #     Rule(SgmlLinkExtractor(), callback='parse_item', follow=True),
    # )

    # <a href="/wiki/Release_Notes" title="Release Notes">
    # wiki/Special:
    # wiki/User_talk:
    # wiki/User:
    # wiki/Talk:

    rules = [
        # Rule(SgmlLinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),
        Rule(SgmlLinkExtractor(allow=[r'wiki/\w+']), callback='parse_item', follow=True),
        # Rule(SgmlLinkExtractor(allow=[r'wiki/\w+'], deny=[r'wiki/[Special\:|User_talk\:|User\:|Talk\:]\w+']), callback='parse_item', follow=True),
    ]
        # r'page/\d+' : regular expression for http://isbullsh.it/page/X URLs


    # rules = (
    #     # Extract links matching 'category.php' (but not matching 'subsection.php')
    #     # and follow links from them (since no callback means follow=True by default).
    #     Rule(SgmlLinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

    #     # Extract links matching 'item.php' and parse them with the spider's method parse_item
    #     Rule(SgmlLinkExtractor(allow=('item\.php', )), callback='parse_item'),
    # )


    # def parse(self, response):
    #     sel = Selector(response)
    #     sites = sel.xpath('//ul/li')
    #     items = []
    #     for site in sites:
    #         item = DmozItem()
    #         item['title'] = site.xpath('a/text()').extract()
    #         item['link'] = site.xpath('a/@href').extract()
    #         item['desc'] = site.xpath('text()').extract()
    #         items.append(item)
    #     return items


    # Try this in a shell
    def parse_item(self, response):
        self.pcounter +=  1
        self.log('Hi, this is an item page (%d)! %s' % (self.pcounter, response.url))
        sel = Selector(response)
        item = WikiItem()
        item['title'] = sel.xpath('//title/text()').extract()
        item['pageurl'] = response.url
        # item['content'] = sel.xpath('//div[re:test(@id, "content")]').extract()
        list_links = []
        # for links in sel.xpath('//a/@href').extract():
        for links in sel.xpath('//div[re:test(@id, "content")]//a/@href').extract():
            if links[:6] != '/wiki/':
                continue
            if links.find('wiki/Special:') != -1 or links.find('wiki/User_talk:') != -1 or links.find('wiki/User:') != -1 or links.find('wiki/Talk:') != -1 or links.find('wiki/Category:') != -1:
                continue
            list_links.append(links)
        # item['links'] = list_links
        return item

    def parse_item_long(self, response):
        self.log('Hi, this is an item page! %s' % response.url)

        hxs = HtmlXPathSelector(response)
        item = IsBullshitItem()
        # Extract title
        item['title'] = hxs.select('//header/h1/text()').extract()[0]
        # Extract author
        item['author'] = hxs.select('//header/p/a/text()').extract()[0]
        # Extract tag(s)
        item['tag'] = hxs.select("//header/div[@class='post-data']/p/a/text()").extract()
        # Extract date
        item['date'] = hxs.select("//header/div[@class='post-data']/p[contains(text(), '20')]/text()").extract()[0]
        # Extract location
        item['location'] = hxs.select("//header/div[@class='post-data']/p[contains(text(), 'From')]/text()").extract()[0].replace('From', '')
        # Extract article url
        urls = hxs.select("//div[@class='breadcrumb-container']/ul[@class='breadcrumb']/li/a/@href").extract()
        item['url'] = urlparse.urljoin(urls[1], urls[2])
        # Extract article text, with html tags
        item['article_html'] = hxs.select("//div[@role='main']/article").extract()[0]

        return item

    # def parse(self, response):
    #     self.log('Hi, this is an item page! %s' % response.url)

        # filename = response.url.split("/")[-2]
        # filename = './download/' + filename
        # open(filename, 'wb').write(response.body)

        # sel = Selector(response)
        # for h1 in sel.xpath('//h1').extract():
        #     yield DmozItem(title=h1)

        # for url in sel.xpath('//a/@href').extract():
        #     if url[:-3] != 'png':
        #         yield Request(url, callback=self.parse)
