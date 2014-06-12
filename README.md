scrapy-wiki-freeswitch
======================

Use Scrapy to retrieve all wiki pages and their relation and use D3 for visualization of those pages


There is 3 directories that contains different parts of the project.


1) WikiSpider
-------------

This is our Scrapy project using http://doc.scrapy.org/en/latest/index.html
WikiSpider will scrape all The wiki pages from http://wiki.freeswitch.org.

The standard usage::

    crapy crawl wiki -o items.json -t json

This will produce a json output will all the pages and their links to other pages of the wiki.

You will find also `prepare_json_items.py` in WikiSpider. `prepare_json_items.py` is a script that will
take the json output and create different results that can be reused for visualization.
Check out the code of `prepare_json_items.py` is documented and should shed some light on the process.


2) D3-wiki
----------

D3-Wiki aims to visualize the data previously collected, it's inspired from http://bl.ocks.org/d3noob/5141528


3) D3-process-map
-----------------

This is an attempt of data visualization using https://github.com/nylen/d3-process-map,
unfortunately this doesn't work well when trying to display a thousands of node and its relations.


Requirements
------------

The only requirements is Scrapy (Scrapy==0.22.2)

