from scrapy import Item, Field


class Jd_phoneItem(Item):
    collection = table = 'phone'
    id = Field()
    title = Field()
    url = Field()
    shop_name = Field()
    price = Field()
    brand = Field()
    model = Field()
    comment_count = Field()
    good_count = Field()
    general_count = Field()
    poor_count = Field()
    show_count = Field()
    crawl_date = Field()
