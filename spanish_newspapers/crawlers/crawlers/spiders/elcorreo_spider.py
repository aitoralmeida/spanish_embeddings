import scrapy
from scrapy import Selector, Request
import datetime
class ElcorreoScraper(scrapy.Spider):
    name = 'elcorreo_spider'
    start_date = datetime.datetime.now()
    finish_date = datetime.datetime(2016, 1, 24)
    day = datetime.timedelta(days=1)
    total_news = 0
    not_allowed = 0
    start_urls = ['http://www.elcorreo.com/hemeroteca/20160627.html']
    pre_url = 'http://www.elcorreo.com/hemeroteca/'
    post_url = '.html'
    def parse(self, response):
        sel = scrapy.Selector(response)
        yield Request(response.url,callback=self.parse_day,dont_filter=True)
        while self.start_date > self.finish_date:
            self.start_date = self.start_date - self.day
            print self.start_date
            date_string = self.date_to_string(self.start_date)
            yield Request(self.pre_url + date_string + self.post_url,callback=self.parse_day,dont_filter=True)


    def parse_day(self, response):
        sel = scrapy.Selector(response)
        news = sel.xpath("/html/body/div[1]/div[2]/div/div/div[2]/section[contains(@class,'noticiaH')]/article/div/h3/a/@href").extract()
        print response.url
        print len(news)
        for new in news:
            yield Request(new, callback=self.parse_news,dont_filter=True)

    def parse_news(self, response):
        print response.url
        sel = scrapy.Selector(response)
        title = sel.xpath("/html/body/div[2]/div[7]/article/div/div/h1//text()")
        if len(title) != 0:
            title = title.extract()
            print title
        #Not in all the news
        """subtitle = sel.xpath("/html/body/div[2]/div[7]/article/div/div/ul/li//text()").extract()
        subtitle = '. '.join(subtitle)
        print subtitle"""
        content = sel.xpath('//*[@id="ccronica"]/p//text()').extract()
        #content = sel.xpath('//*[@id="ccronica"]').extract()
        if len(content) == 0:
            """print "INICIOasdadsdas"
            print sel.xpath("/html/body").extract()
            print "FIN"""
            self.not_allowed += 1
        else:
            content = ' '.join(content)
            self.total_news += 1
            #print content
        print "Total allowed " + str(self.total_news)
        print "Not allowed" + str(self.not_allowed)
    def date_to_string(self, date):
        year = str(date.year)
        month = str(date.month)
        day = str(date.day)
        if len(day) < 2:
            day = '0' + day
        if len(month) < 2:
            month = '0' + month
        return str(year) + str(month) + str(day)
