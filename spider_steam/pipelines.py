# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SpiderSteamPipeline:
    def process_item(self, item, spider):
        return item

    # Нам по сути не нужны все эти штуки, потому что флаги -o -O - делают все за нас

    # def open_spider(self, spider):
    #     self.file = open("items.json", "w")
    #     self.file.write('[')
    #
    # def close_spider(self, spider):
    #     self.file.write(']')
    #     self.file.close()
    #
    # def process_item(self, item, spider):
    #     line = json.dumps(ItemAdapter(item).asdict()) + ',\n'
    #     self.file.write(line)
    #     return item
