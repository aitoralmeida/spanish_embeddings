import scrapy
from scrapy import Selector, Request
from crawlers.items import ScrapyEditorialItem
from scrapy_splash import SplashRequest

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


    """def parse(self, response):
        sel = scrapy.Selector(response)
        yield SplashRequest(response.url,callback=self.parse_middleware,dont_filter=True,args={'wait': 2})
        #nextornot = sel.xpath('//*[@id="content-section"]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]//text()').extract()
        #nextornot = sel.xpath('//*[@id="content-section"]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]').extract()
        #print nextornot
        #if 'Siguiente' in nextornot:
            #new_url = sel.xpath('//*[@id="principal"]/nav/ul/li/a/@href').extract().pop()
            #yield Request(new_url)

    def parse_middleware(self,response):
        sel = scrapy.Selector(response)
        #yield Request(response.url,callback=self.parse_article_links,dont_filter=True)
        nextornot = sel.xpath('//*[@id="content-section"]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[3]/a[1]/@href').extract()
        print nextornot
        if len(nextornot) > 0:
            url = self.BASE + nextornot.pop()
            print url
            yield SplashRequest(url,callback=self.parse_middleware,dont_filter=True,args={'wait': 2})"""
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
        date = sel.xpath('//*[@id="content-section"]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[3]/span//text()').extract().pop()
        item['published'] = date
        text = sel.xpath('//*[@id="content-section"]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/p/text()').extract()
        if len(text) > 0:
            item['text'] = text.pop()
        else:
            text = sel.xpath('//*[@id="content-section"]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div/p/text()').extract()
            if len(text) > 0:
                item['text'] = text.pop()
            else:
                text = sel.xpath('//*[@id="content-section"]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/p/text()').extract()
                if len(text) > 0:
                    item['text'] = text.pop()
                else:
                    if len(text)>0:
                        text = sel.xpath('//*[@id="content-section"]/div/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div/p/text()').extract()
                        item['text'] = text.pop()
                    else:
                        print "Not able to gather the editorial entitled: " +title + "with url " + response.url
        return item
