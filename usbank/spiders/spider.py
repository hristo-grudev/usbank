import scrapy

from scrapy.loader import ItemLoader

from ..items import UsbankItem
from itemloaders.processors import TakeFirst


class UsbankSpider(scrapy.Spider):
	name = 'usbank'
	start_urls = ['https://www.usbank.com/newsroom/news.html']

	def parse(self, response):
		post_links = response.xpath('//h4/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@id="next-page"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "blogEntry", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "parbase", " " ))]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		try:
			date = response.xpath('//span[@class="getMoreArticlesLink"]/text()').get().split('|')[0]
		except:
			date = ''

		item = ItemLoader(item=UsbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
