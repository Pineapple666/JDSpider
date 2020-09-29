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

    product_name = Field()  # 商品名称
    product_weight = Field()  # 商品重量
    cpu_model = Field()  # cpu型号
    ram = Field()  # 运行内存
    memory = Field()  # 机身存储
    resolution = Field()  # 分辨率
    rear_pixels = Field()  # 后摄像素
    front_pixels=Field()#前摄像素
    screen_size=Field()#屏幕尺寸
    cameras_number=Field()#摄像头数量
