import scrapy
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy_project.items import ScrapyProjectItem


class LoginSpider(scrapy.Spider):
    name = 'login'
    start_urls = ["http://dccomics.ru/"]
    links = []

    def parse(self, response):
        return [
            FormRequest.from_response(
                response,
                formdata={"login_name": "fodef37345", "login_password": "fodef37345"},
                callback=self.parse_after_login
            )]

    def parse_after_login(self, response):
        if response.xpath('//div[@class="wrap not-logged"]/ul//li[@class="login-btn"]').get() is not None:
            print("Ошибка авторизации.")
        else:
            print("Успешная авторизация.")
            return scrapy.Request("http://dccomics.ru/forum/forum_4", callback=self.parse_forum)

    def parse_forum(self, response):
        new_links = response.xpath('//tr/td[@class="row2"]/a/@href').getall()
        for link in new_links:
            if link not in self.links:
                self.links.append(link)
                yield response.follow(link, callback=self.parse_forum)

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
            yield response.follow(next_page[len(next_page) - 1], callback=self.parse_forum)
        else:
            yield response.follow('http://dccomics.ru/forum/forum_4', callback=self.parse_forum)

        for row in range(1, len(usernames) + 1):
            item['title'] = title
            item['usernames'] = usernames[row - 1]
            item['dates'] = dates[(row - 1) * 4]
            item['user_messages'] = user_messages[row - 1]

            yield item

