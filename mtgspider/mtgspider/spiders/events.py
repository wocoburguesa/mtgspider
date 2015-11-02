# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from mtgspider.items import EventItem


class EventsSpider(scrapy.Spider):
    name = "events"
    allowed_domains = ["magic.wizards.com"]
    start_urls = (
        'http://magic.wizards.com/en/content/' +
        'deck-lists-magic-online-products-game-info',
    )

    def build_event_url(self, event, response):
        return response.urljoin(event.xpath('div/a/@href').extract()[0])

    def parse(self, response):
        events = []
        count = 0

        for event in response.css('div.article-item'):
            count += 1
            event_loader = ItemLoader(item=EventItem())
            event_url = self.build_event_url(event, response)
            event_loader.add_value(
                'id', event.css('.metaText .section a::text').extract())
            event_loader.add_value(
                'date', event.css('.metaText .section a::text').extract())
            event_loader.add_value('url', event_url)

            event = event_loader.load_item()
            request = scrapy.Request(
                event_url,
                callback=self.parse_event_detail
            )
            request.meta['event'] = event
            request.meta['events'] = events
            yield request

#        return events

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
