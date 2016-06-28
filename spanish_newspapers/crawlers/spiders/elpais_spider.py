import scrapy
from scrapy import Selector, Request
from crawlers.items import ScrapyEditorialItem

class EditorialScraper(scrapy.Spider):
    name = 'editorials_spider'
    start_urls = ['http://elpais.com/tag/c/aac32d0cdce5eeb99b187a446e57a9f7']


    def parse(self, response):
        sel = scrapy.Selector(response)
        yield Request(response.url,callback=self.parse_article_links,dont_filter=True)
        nextornot = sel.xpath('//*[@id="principal"]/nav/ul/li/a//text()').extract().pop()
        if 'Siguiente' in nextornot:
            new_url = sel.xpath('//*[@id="principal"]/nav/ul/li/a/@href').extract().pop()
            yield Request(new_url)


    def parse_article_links(self, response):
        sel=Selector(response)
        urls = sel.xpath('//*[@id="principal"]/section/div/div/div/article/div/h2/a/@href').extract()
        for url in urls:
            yield Request(url,callback=self.parse_article)


    def parse_article(self, response):
        item = ScrapyEditorialItem()
        sel=Selector(response)
        title = sel.xpath('//*[@id="articulo-titulo"]//text()').extract().pop()
        item['title'] = title
        subtitle = sel.xpath('//*[@id="articulo-titulares"]/div/h2').extract()
        if len(subtitle) > 0:
            subtitle = subtitle.pop()
            item['subtitle'] = subtitle
        paragraphs_text = sel.xpath('//*[@id="cuerpo_noticia"]/p//text()').extract()
        text = ''.join(paragraphs_text)
        item['text'] = text
        item['url'] = response.url
        last_updated = sel.xpath('//*/meta[@itemprop="datePublished"]/@content').extract()
        if len(last_updated) > 0:
            item['last_updated'] = last_updated.pop()
        published = sel.xpath('//*/meta[@itemprop="dateModified"]/@content').extract()
        if len(published) > 0:
            item['published'] = published.pop()
        tags = sel.xpath('//*[@id="listado"]/li//text()').extract()
        item['tags'] = tags
        return item
