import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import BbankofbarodaItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class BbankofbarodaSpider(scrapy.Spider):
	name = 'bankofbaroda'
	start_urls = ['https://bankofbaroda.gy/news-notices/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="more-link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//time/text()').get()
		title = response.xpath('(//h2)[last()]/text()').get()
		content = response.xpath('//div[@class="entry-content"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))
		if not content:
			content = "You can find image in the link"

		item = ItemLoader(item=BbankofbarodaItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
