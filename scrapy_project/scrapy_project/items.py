# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    forum_url = scrapy.Field()
    title = scrapy.Field()
    usernames = scrapy.Field()
    dates = scrapy.Field()
    user_messages = scrapy.Field()
    # pass
