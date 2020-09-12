import codecs
import pymongo
import pymysql
import json


class JsonWithEncodingPipeline:
    """

    """

    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('jd_phone.json', 'w', encoding="utf-8")

    def open_spider(self, spdier):
        # self.file.write('[')
        pass

    def process_item(self, item):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item

    def close_spider(self):
        # self.file.write(']')
        self.file.close()


class MongoPipeline:
    """
    MongoDB存储
    """

    def __init__(self, mongo_uri, mongo_db):
        """

        :param mongo_uri:
        :param mongo_db:
        """
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        """
        配置数据库

        :param crawler:
        :return:
        """
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        """
        连接数据库

        :param spider:
        :return:
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        """
        插入数据

        :param spider:
        :param item:
        :return:
        """
        self.db[item.collection].insert(dict(item))
        return item

    def close_spider(self, spider):
        """
        关闭数据库

        :param spider:
        :return:
        """
        self.client.close()


class MysqlPipeline:
    """
    MySQL存储
    """

    def __init__(self, host, database, user, password, port):
        """

        :param host:
        :param database:
        :param user:
        :param password:
        :param port:
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.db = None
        self.cursor = None

    @classmethod
    def from_crawler(cls, crawler):
        """
        配置数据库

        :param crawler:
        :return:
        """
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT')
        )

    def open_spider(self, spider):
        """
        连接数据库

        :param spider:
        :return:
        """
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        """
        插入数据

        :param spider:
        :param item:
        :return:
        """
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item

    def close_spider(self, spider):
        """
        关闭数据库

        :param spider:
        :return:
        """
        self.db.close()
