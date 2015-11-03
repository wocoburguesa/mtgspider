# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import re

import scrapy


def get_event_id(value):
    event_id = re.search('#[0-9]*', value[0])
    return event_id.group(0)


def get_event_date(value):
    event_date = re.search('[0-9]*\/[0-9]*\/[0-9]*', value[0])
    return event_date.group(0)


def get_player(value):
    player = value[1]
    return player


class EventItem(scrapy.Item):
    """
    id: event id, it looks like they are assigned auto-increasing integers.
    url: event url.
    date: extracted from event description.
    players: list of participants in the event. Will use this to generate
    user stats down the pipeline.
    """
    id = scrapy.Field(
        input_processor=get_event_id
    )
    url = scrapy.Field()
    date = scrapy.Field(
        input_processor=get_event_date
    )
    players = scrapy.Field(
        input_processor=get_player
    )


class DeckItem(scrapy.Item):
    """
    Coming soon
    """
    pilot = scrapy.Field()
    planeswalkers = scrapy.Field()
    creatures = scrapy.Field()
    sorceries = scrapy.Field()
    instants = scrapy.Field()
    enchantments = scrapy.Field()
    lands = scrapy.Field()
    # Either 'mainboard' or 'sideboard'
    type = scrapy.Field()