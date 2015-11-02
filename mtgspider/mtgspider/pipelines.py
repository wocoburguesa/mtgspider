# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.exceptions import DropItem
from scrapy.conf import settings


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        new_id = item['id'][0]
        if new_id in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(new_id)
            return item


class PlayerStatsPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        event_id = int(item['id'][0][1:])
        for player in item['players']:
            db_player = self.collection.find_one({'name': player})

            if not db_player:
                self.collection.insert({
                    'name': player,
                    'last_event': item['id'][0],
                    'games_played': 1
                })
            elif event_id > int(db_player['last_event'][1:]):
                self.collection.update(
                    {'name': player},
                    {
                        '$set': {
                            'games_played': db_player['games_played'] + 1,
                            'last_event': item['id'][0]
                        }
                    },
                    upsert=False
                )
        return item
