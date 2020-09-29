from jd_phone.items import Jd_phoneItem
from scrapy import Request, Spider
from urllib.parse import quote
import json
import re


class PhoneSpider(Spider):
    """
    手机爬虫
    """
    name = 'phone'
    allowed_domains = ['jd.com']

    # 需要爬取的 类目
    keyword = quote('手机')
    # 需要爬取的最大页数
    max_page = 5
    # 商品列表url
    start_url = 'https://search.jd.com/s_new.php?keyword={keyword}&page={page}&s={s}'
    # 商品评论页面(JSON)url
    comment_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds={id}'
    # 商品详情页面url
    items_url = 'https://item.jd.com/{id}.html'

    def start_requests(self):
        """
        生成初始请求

        :return: 初始请求
        """
        # 请求 商品列表页的第1页，获取的商品列表页只包含 前30个商品
        page = s = 1
        yield Request(url=self.start_url.format(keyword=self.keyword, page=page, s=s),
                      meta={'page': page, 's': s})

    def parse(self, response):
        """
        解析商品列表

        :param response:
        :return: 评论页面请求，下一页请求
        """
        ids = re.search(r"wids:'(.*?)'", response.text, re.S).group(1)
        for id in ids.split(','):
            title = response.css(f'li[data-sku="{id}"] .p-name.p-name-type-2 em::text').extract_first('').strip()
            price = response.css(f'strong.J_{id} i::text').extract_first('')
            # 回调处理评论页面
            yield Request(url=self.comment_url.format(id=id), callback=self.parseComment,
                          meta={'title': title, 'price': price}, dont_filter=True)
        # page 代表半页，即30个商品
        page = response.meta['page'] + 1
        s = response.meta['s'] + 25
        if page < self.max_page * 2 + 1:
            # 回调解析后30个商品
            yield Request(url=self.start_url.format(keyword=self.keyword, page=page, s=s), callback=self.parse,
                          meta={'page': page, 's': s})

    def parseComment(self, response):
        """
        解析评论内容(JSON)

        :param response:
        :return: 详情页面请求
        """

        comment_dict = json.loads(response.text)['CommentsCount'][0]
        # 获取 商品总评论数
        comment_count = comment_dict.get('CommentCount', 0)
        # 获取 商品好评数
        good_count = comment_dict.get('GoodCount', 0)
        # 获取 商品中评数
        general_count = comment_dict.get('GeneralCount', 0)
        # 获取 商品差评数
        poor_count = comment_dict.get('PoorCount', 0)
        # 获取 商品被展示次数
        show_count = comment_dict.get('ShowCount', 0)
        # 获取 商品id
        id = comment_dict.get('SkuId', 0)
        # 拼接 详情url
        item_url = self.items_url.format(id=id)
        # 回调解析商品详情页面
        yield Request(url=item_url, callback=self.parseDetail,
                      meta={'comment_count': comment_count, 'good_count': good_count, 'general_count': general_count,
                            'poor_count': poor_count, 'show_count': show_count, 'id': id, 'fail_time': 0,
                            'title': response.meta['title'], 'price': response.meta['price']},
                      dont_filter=True)

    def parseDetail(self, response):
        """
        解析详情页面

        :param response:
        :return: 项目
        """
        # 获取 商品品牌
        brand = response.css('#parameter-brand li::attr(title)').extract_first('')
        if brand == '':
            if response.meta['fail_time'] <= 5:
                response.meta['fail_time'] += 1
                yield Request(url=response.url, callback=self.parseDetail, meta=response.meta, dont_filter=True)
            else:
                pass
        # 获取 商品型号
        else:
            model = response.css('.item.ellipsis::text').extract_first('')
            if not model:
                model = response.css('.parameter2.p-parameter-list li::attr(title)').extract_first('')
            # 获取 商品的店名
            shop_name = response.css('.J-hove-wrap.EDropdown.fr .item .name a::text').extract_first('')
            if not shop_name:
                shop_name = response.css(
                    '.item.hide.J-im-item .J-im-btn .im.customer-service::attr(data-seller)').extract_first('')
            # 获取 商品url
            url = response.url

            # 获取 meta中的值
            comment_count = response.meta['comment_count']
            good_count = response.meta['good_count']
            general_count = response.meta['general_count']
            poor_count = response.meta['poor_count']
            show_count = response.meta['show_count']
            id = response.meta['id']
            title = response.meta['title']
            price = response.meta['price']

            # 传入 item
            item = Jd_phoneItem()
            item['id'] = id
            item['title'] = title
            item['url'] = url
            item['shop_name'] = shop_name
            item['price'] = price
            item['brand'] = brand
            item['model'] = model
            item['comment_count'] = comment_count
            item['good_count'] = good_count
            item['general_count'] = general_count
            item['poor_count'] = poor_count
            item['show_count'] = show_count
            yield item
