# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from mtgspider.items import EventItem

BASE_URL = 'http://magic.wizards.com'


class EventsSpider(scrapy.Spider):
    """
    Scraping the event results page for Magic: The Gathering Online in order
    to generate player specific statistics.
    """

    name = "events"
    allowed_domains = ["magic.wizards.com"]
    start_urls = (
        BASE_URL + '/en/content/deck-lists-magic-online-products-game-info',
    )

    def build_event_url(self, event):
        return BASE_URL + event.xpath('div/a/@href').extract()[0]

    def parse(self, response):
        events = []

        for event in response.css('div.article-item'):
            event_loader = ItemLoader(item=EventItem())
            event_url = self.build_event_url(event)
            event_loader.add_value(
                'id', event.css('.metaText .section a::text').extract())
            event_loader.add_value(
                'date', event.css('.metaText .section a::text').extract())
            event_loader.add_value('url', event_url)

            event_item = event_loader.load_item()
            request = scrapy.Request(
                event_url,
                callback=self.parse_event_detail
            )
            request.meta['event'] = event_item
            request.meta['events'] = events
            yield request

    def parse_event_detail(self, response):
        event = response.meta['event']
        events = response.meta['events']
        players = response.xpath('//table[@class="sticky-enabled"]/tbody/tr')
        event_loader = ItemLoader(event)

        for player in players:
            event_loader.add_value(
                'players', player.xpath('td/text()').extract())

        events.append(event_loader.load_item())
        return events
