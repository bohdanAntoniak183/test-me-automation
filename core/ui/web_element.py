import logging

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

class WebElement:
    def __init__(
        self,
        browser,
        locator,
        description,
        parent = None
    ):
        self.driver = browser.driver

        if parent:
            self.locator = parent.locator + locator
            self.description = f"Дочірній елемент '{description}' від '{parent.description}'"
        else:
            self.locator = locator
            self.description = description

        self.waiter = WebDriverWait(self.driver, 30)
        self.logger = logging.getLogger()

    def __get(self):
        return self.driver.find_element(By.XPATH, self.locator)

    def get_text(self):
        self.logger.info(f"Отримання тексту елемента '{self.description}'")
        return self.waiter.until(
            lambda _: self.__get().text or None,
            message=f"Не вдалося отримати текст для елемента '{self.description}'."
        )

    def click(self):
        self.logger.info(f"Клік на елемент '{self.description}'")
        self.waiter.until(
            lambda _ : self.__get().click() or True,
            message=f"Не вдалось клікнути на елемент '{self.description}'."
        )

    def clear_value(self):
        self.logger.info(f"Очищення значення елемента '{self.description}'")
        self.waiter.until(
            lambda _ : self.__get().clear() or True,
            message=f"Не вдалось очистити значення елементу '{self.description}'"
        )

    def enter_value(self, value):
        self.logger.info(f"Введення значення '{value}' в елемент '{self.description}'")
        self.waiter.until(
            lambda _ : self.__get().send_keys(value) or True,
            message=f"Не вдалось увести значення '{value}' в елемент '{self.description}'"
        )

    def select_option_by_value(self, option):
        self.logger.info(f"Вибір опції за значенням '{option}' в елементі '{self.description}'")
        self.waiter.until(
            lambda _: Select(self.__get()).select_by_value(option) or True,
            message=f"Не вдалось обрати опцію за значенням '{option}' в елементі '{self.description}'"
        )

    def assert_is_visible(self):
        self.logger.info(f"Перевірка, що елемент '{self.description}' видимий")
        self.waiter.until(
            lambda _: self.__get().is_displayed(),
            message=f"Елемент '{self.description}' не є видимим."
        )

    def assert_text(self, expected_text):
        self.logger.info(f"Перевірка, що текст елемента '{self.description}' дорівнює '{expected_text}'")
        self.waiter.until(
            lambda _: self.__get().text == expected_text,
            message=f"Не вдалося дочекатися тексту '{expected_text}' для елемента '{self.description}'."
        )

    def assert_text_contains(self, expected_text):
        self.logger.info(f"Перевірка, що текст елемента '{self.description}' містить '{expected_text}'")
        self.waiter.until(
            lambda _: expected_text in self.__get().text,
            message=f"Не вдалося дочекатися, поки текст елемента '{self.description}' міститиме '{expected_text}'."
        )