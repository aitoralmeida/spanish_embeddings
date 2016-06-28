import scrapy
from scrapy import Selector, Request
from crawlers.items import ScrapyEditorialItem
from scrapy_splash import SplashRequest
#USAGE: scrapy crawl naiz_spider -o naiz.json
class NaizScraper(scrapy.Spider):
    name = 'naiz_spider'
    start_urls = ['http://www.naiz.eus/eu/editorials/1570/page/1']
    BASE = 'http://www.naiz.eus'
    page = 1
    def parse(self, response):
        sel = scrapy.Selector(response)
        urls = sel.xpath('/html/body/div[2]/div/div/a/@href').extract()
        if len(urls) > 0:
            for url in urls:
                yield Request(url,callback=self.parse_article)
            self.page += 1
            new_url = response.url.rsplit('/',1)
            new_url = new_url[0] + '/' + str(self.page)
            print new_url
            yield Request(new_url,callback=self.parse)

    def parse_article_links(self, response):
        sel=Selector(response)
        urls = sel.xpath('//*[@id="principal"]/section/div/div/div/article/div/h2/a/@href').extract()
        for url in urls:
            yield Request(url,callback=self.parse_article)


    def parse_article(self, response):
        item = ScrapyEditorialItem()
        sel=Selector(response)
        title = sel.xpath('//*[@id="content-section"]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/span//text()').extract().pop()
        item['title'] = title
        item['url'] = response.url
        date = sel.xpath('//*[@id="content-section"]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[3]/span//text()').extract().pop()
        item['published'] = date
        text = sel.xpath('//*[@id="content-section"]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/p/text()').extract()
        if len(text) > 0:
            text = ' '.join(text)
            item['text'] = text
        else:
            text = sel.xpath('//*[@id="content-section"]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div/p/text()').extract()
            if len(text) > 0:
                text = ' '.join(text)
                item['text'] = text
            else:
                text = sel.xpath('//*[@id="content-section"]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/p/text()').extract()
                if len(text) > 0:
                    text = ' '.join(text)
                    item['text'] = text
                else:
                    if len(text)>0:
                        text = sel.xpath('//*[@id="content-section"]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div/p/text()').extract()
                        text = ' '.join(text)
                        item['text'] = text
                    else:
                        print "Not able to gather the editorial entitled: " +title + "with url " + response.url
        print item
        return item
