from selenium import webdriver


class HeadersMiddleware:
    """

    """

    def __init__(self):
        """
        初始化cookies
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(options=options)
        browser.get('https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA')
        browser.get('https://item.jd.com/100007864391.html')
        cookies = browser.get_cookies()
        self.cookies_dict = {}
        for cookie in cookies:
            self.cookies_dict[cookie['name']] = cookie['value']

    def process_request(self, request, spider):
        """
        设置headers和cookies

        :param spider:
        :param request:
        :return:
        """
        if 'item.jd.com' in request.url:
            request.headers[
                'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
            request.cookies = self.cookies_dict
