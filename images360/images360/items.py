# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from scrapy import  Item,Field


class ImageItem(Item):
    collectione = table = "images"
    id = Field()
    url = Field()
    title = Field()
    thumb = Field()