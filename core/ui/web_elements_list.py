import logging
from typing import TypeVar, Generic, Type

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from core.ui.web_element import WebElement

T = TypeVar("T", bound=WebElement)

class WebElementsList(Generic[T]):
    def __init__(
        self,
        browser,
        locator,
        description,
        element_class: Type[T] = WebElement,
        parent = None
    ):
        self.browser = browser
        self.driver = browser.driver
        self.description = description
        self.element_class = element_class

        if parent:
            self.locator = parent.locator + locator
        else:
            self.locator = locator

        self.waiter = WebDriverWait(self.driver, 30)
        self.logger = logging.getLogger()

    def __get_elements(self):
        raw_elements = self.driver.find_elements(By.XPATH, self.locator)
        elements_list = []
        
        for index, raw_element in enumerate(raw_elements):
            web_element = self.element_class(
                browser=self.browser,
                locator=f"({self.locator})[{index + 1}]",
                description=f"Елемент '{self.description}' з індексом [{index + 1}]",
            )
            elements_list.append(web_element)
            
        return elements_list

    def __len__(self):
        length = len(self.__get_elements())
        return length

    def __getitem__(self, index):
        return self.waiter.until(
            lambda _: elements[index - 1] 
            if len(elements := self.__get_elements()) >= index 
            else False,
            message=f"Елемент з індексом '{index}' не було знайдено."
        )

    def assert_that_length_is_equal_to(self, length_value):
        self.logger.info(f"Перевірка, що довжина списку '{self.description}' дорівнює '{length_value}'")
        self.waiter.until(
            lambda _ : len(self) == length_value,
            message=f"Перевірка не пройдена: довжина '{self.description}' мала бути {length_value}."
        )