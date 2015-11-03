# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from mtgspider.items import EventItem
from mtgspider import settings

BASE_URL = 'http://magic.wizards.com'


class EventsSpider(scrapy.Spider):
    """
    Scraping the event results page for Magic: The Gathering Online in order
    to generate player specific statistics.
    """

    name = "events"
# Commented this line because Splash requests go to a different domain.
#    allowed_domains = ["magic.wizards.com"]
    start_urls = (
        BASE_URL + '/en/content/deck-lists-magic-online-products-game-info',
    )

    def build_event_url(self, event):
        return BASE_URL + event.xpath('div/a/@href').extract()[0]

    def start_requests(self):
        """
        The script looks like this because the Webkit driver that
        Splash uses doesn't handle .click() events well on non-button DOM
        elements. It is intended to click on the "LOAD MORE" button to
        parse more than six events at a time.
        """

        script = """
        function main(splash)
            splash.resource_timeout = 20
            assert(splash:go(splash.args.url))

            local fireClick = splash:jsfunc([[
                function() {{
                    var c = document.createEvent("MouseEvents"),
                    el = document.getElementsByClassName(
                        'see-more-article-listing-section'
                    )[0];

                    c.initMouseEvent(
                        "click",
                        true,true,window,
                        0,0,0,0,0,
                        false,false,false,false,
                        0,null
                    );

                    el.dispatchEvent(c);
                }}
            ]])

            for i = 1,{0} do
                fireClick()
                splash:wait(3.0)
            end

            return splash:html()
        end
        """.format(settings.CLICK_LOAD_MORE_ITERATIONS,)

        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    'endpoint': 'execute',
                    'args': {'lua_source': script}
                }
            })

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
