import logging

from selenium import webdriver

class Browser:
    def __init__(self, headless):
        options = webdriver.ChromeOptions()

        options.add_argument("--start-maximized")

        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=options)
        self.logger = logging.getLogger()

    def navigate_to(self, url):
        self.driver.get(url)
        self.logger.info(f"Відкриття сторінки: {url}.")

    def reload(self):
        self.driver.refresh()
        self.logger.info("Перезавантаження сторінки.")

    def terminate(self):
        self.driver.quit()
        self.logger.info("Закриття браузера.")
