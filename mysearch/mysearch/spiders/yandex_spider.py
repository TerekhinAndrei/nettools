import scrapy
from scrapy.http import FormRequest


class YandexSpider(scrapy.Spider):
    name = "tesnsk"
    start_urls = ['http://tesnsk.ru']

    def parse(self, response):
        # Check if we are redirected to the login page
        if "passport.yandex.ru" in response.url:
            self.logger.debug("Redirected to login page. Handling login.")
            return FormRequest.from_response(
                response,
                formdata={
                    'login': 'your_username',  # replace with your username
                    'passwd': 'your_password'  # replace with your password
                },
                callback=self.after_login
            )
        else:
            # Continue parsing the initial page if no login is needed
            self.logger.debug("No login required. Parsing main page.")
            return self.parse_main_page(response)

    def after_login(self, response):
        if "passport.yandex.ru" in response.url:
            self.logger.error("Login failed")
            return

        # Login was successful, proceed to the main page
        self.logger.debug("Login successful. Proceeding to main page.")
        return self.parse_main_page(response)

    def parse_main_page(self, response):
        # Your parsing code here
        self.logger.info("Parsing main page content")
        pass
