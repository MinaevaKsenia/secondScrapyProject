import scrapy
from scrapy_project.items import ScrapyProjectItem
from scrapy.selector import Selector


class ForumSpider(scrapy.Spider):
    name = "forum"
    links = []

    def start_requests(self):
        urls = [
            'http://dccomics.ru/forum/forum_4'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        new_links = response.xpath('//tr/td[@class="row2"]/a/@href').getall()
        for link in new_links:
            if link not in self.links:
                self.links.append(link)
                yield response.follow(link, callback=self.parse)

        item = ScrapyProjectItem()
        item['forum_url'] = response.url

        title = response.xpath('//head/title/text()').get()
        usernames = response.xpath('//tr/td[@class="row2"]//b/a/text()').getall()
        dates = response.xpath('//div//tr//td/span[@class="postdetails"]//div/text()').getall()
        user_posts = response.xpath('//table/tr//td[@class="post2"]/span[@class="postcolor"]').getall()
        next_page = response.xpath('//table/tr//td/div/div[@class="forum_navigation"]/a/@href').getall()

        user_messages = []
        for post in user_posts:
            one_post = Selector(text=post).xpath('//div[contains(@id,"post-id")]/text()').getall()
            row = ""
            for message in one_post:
                row += str(message)
            user_messages.append(row)

        if len(next_page) and next_page is not None:
            yield response.follow(next_page[len(next_page) - 1], callback=self.parse)
        else:
            yield response.follow('http://dccomics.ru/forum/forum_4', callback=self.parse)

        for row in range(1, len(usernames) + 1):
            item['title'] = title
            item['usernames'] = usernames[row - 1]
            item['dates'] = dates[(row - 1) * 4]
            item['user_messages'] = user_messages[row - 1]

            yield item