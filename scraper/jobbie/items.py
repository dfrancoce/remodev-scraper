# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Job(scrapy.Item):
    """ A job contains the following properties:
        url: Url of the job offer
        position = A text explaining the offer
        company = The company offering the position
        date = Date of the offer
        tags = Some extra information in the form of tags
    """
    url = scrapy.Field()
    position = scrapy.Field()
    company = scrapy.Field()
    date = scrapy.Field()
    tags = scrapy.Field()
