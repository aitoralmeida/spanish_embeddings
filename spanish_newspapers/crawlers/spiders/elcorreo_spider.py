import scrapy
from scrapy import Selector, Request
import datetime
from crawlers.items import ScrapyEditorialItem
#USAGE: scrapy crawl elcorreo_spider -o elcorreo.json
class ElcorreoScraper(scrapy.Spider):
    name = 'elcorreo_spider'
    start_date = datetime.datetime.now()
    finish_date = datetime.datetime(2012, 6, 24)
    day = datetime.timedelta(days=1)
    total_news = 0
    not_allowed = 0
    start_urls = ['http://www.elcorreo.com/hemeroteca/noticia/20160627.html']
    pre_url = 'http://www.elcorreo.com/hemeroteca/noticia/'
    post_url = '.html'
    def parse(self, response):
        sel = scrapy.Selector(response)
        yield Request(response.url,callback=self.parse_day,dont_filter=True)
        while self.start_date > self.finish_date:
            self.start_date = self.start_date - self.day
            date_string = self.date_to_string(self.start_date)
            yield Request(self.pre_url + date_string + self.post_url,callback=self.parse_list_days,dont_filter=True)

    def parse_list_days(self, response):
        sel = scrapy.Selector(response)
        last_page_number = sel.xpath('/html/body/div[1]/div[2]/div/div/div[2]/nav/ul/li[9]/a/@href').extract()
        if len(last_page_number) > 0:
            last_page_number = int(last_page_number.pop().split('=')[-1])
            i = 1
            while i <= last_page_number:
                yield Request(response.url + "?pag=" + str(i),callback=self.parse_day,dont_filter=True)
                i += 1
    def parse_day(self, response):
        sel = scrapy.Selector(response)
        news = sel.xpath("/html/body/div[1]/div[2]/div/div/div[2]/section[contains(@class,'noticiaH')]/article/div/h3/a/@href").extract()
        print response.url
        for new in news:
            yield Request(new, callback=self.parse_news,dont_filter=True)

    def parse_news(self, response):
        print response.url
        sel = scrapy.Selector(response)
        item = ScrapyEditorialItem()
        title = sel.xpath("/html/body/div[2]/div[7]/article/div/div/h1//text()")
        if len(title) != 0:
            title = title.extract()
            item['title'] = title.pop()
        #Not in all the news
        """subtitle = sel.xpath("/html/body/div[2]/div[7]/article/div/div/ul/li//text()").extract()
        subtitle = '. '.join(subtitle)
        print subtitle"""
        content = sel.xpath('//*[@id="ccronica"]/p//text()').extract()
        if len(content) == 0:
            content = sel.xpath('//*[@id="story-texto"]/p//text()').extract()
            if len(content) == 0:
                self.not_allowed += 1
            else:
                content = ' '.join(content)
                item['text'] = content
                self.total_news += 1
                return item
        else:
            content = ' '.join(content)
            item['text'] = content
            self.total_news += 1
            print item
            return item
            #print content
        print "Total allowed " + str(self.total_news)
        print "Not allowed " + str(self.not_allowed)
    def date_to_string(self, date):
        year = str(date.year)
        month = str(date.month)
        day = str(date.day)
        if len(day) < 2:
            day = '0' + day
        if len(month) < 2:
            month = '0' + month
        return str(year) + str(month) + str(day)
