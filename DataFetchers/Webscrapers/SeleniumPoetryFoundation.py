from selenium import webdriver
from typing import List

from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from DataFetchers.IDataFetcher import IDataFetcher


class SeleniumPoetryFoundation(IDataFetcher):
    """
    Class contains all methods necessary to scrape a the poetry foundation
    website for a list of poems.
    """
    __doc__ = IDataFetcher.__doc__ + __doc__

    def __init__(self, number_of_pages: int):
        super().__init__()
        self.driver = self.setup_chrome_driver(["--headless"])
        self.list_of_poems: List[str] = []
        self.number_of_pages = number_of_pages

    def get_list_of_poems(self) -> List[str]:
        """
        The Poetry Foundation implementation.
        """
        for i in range(1, self.number_of_pages + 1):
            url: str = f"https://www.poetryfoundation.org/poems/browse#page={i}&sort_by=recently_added"
            self.scrape_poetry_page_and_add_to_poetry_list(url)
        return self.format_and_return_a_clean_list_of_poems()

    def number_of_poems(self):
        return self.number_of_pages * 20

    def scrape_poetry_page_and_add_to_poetry_list(self, url) -> None:
        """
        Scrapes a given poetry page and returns all of the poems on that page in a list format.
        :return: A list of poems.
        """
        self.driver.refresh()
        self.driver.get(url)
        received_links = False
        all_links: List[str] = []

        # TODO: Write something actually good here
        while not received_links:
            try:
                elements: WebElement = self.driver.find_element(By.CLASS_NAME, "c-assetViewport")
                poem_links = elements.find_elements(By.TAG_NAME, "a")
                all_links = [link.get_attribute("href") for link in poem_links]
                received_links = True
            except StaleElementReferenceException:
                self.driver.get(url)
                pass

        for link in all_links:
            self.add_valid_poem_to_list(link)

    def add_valid_poem_to_list(self, link: str) -> None:
        """
        Checks that a poem has content then if it does add it to the list of poems.
        :param link: The link for the poem page.
        :return: None.
        """
        self.driver.refresh()
        self.driver.get(link)
        selected_poem: List[WebElement] = self.driver.find_elements(By.CLASS_NAME, "o-poem")
        if len(selected_poem) > 0:
            poem = selected_poem[0].get_attribute("innerText")
            self.list_of_poems.append(poem)
            self.update_and_print_progress_bar()

    def format_and_return_a_clean_list_of_poems(self) -> List[str]:
        """
        An actually quite tricky method, has to remove all of the unnecessary unicode formatting provided by
        https://www.poetryfoundation.org/ (Thanks for that!!!)
        Removes all of the escape characters, and foreign languages from the list of poems retrieved.
        :return: A list of beautifully formatted poems for CSV conversion.
        """
        escapes = ''.join([chr(char) for char in range(1, 32)])
        translator = str.maketrans('', '', escapes)

        # Remove any extra jazz from the strings
        return [poem.translate(translator).replace(";", " ").encode('ascii', errors='ignore').decode("utf-8") + ";" for
                poem in self.list_of_poems]

    @staticmethod
    def setup_chrome_driver(option_set: List[str]):
        """
        Sets up the chrome driver with any necessary config options.
        :param option_set: The list of config options.
        :return: The webdriver.
        """
        options = Options()
        for option in option_set:
            options.add_argument(option)
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
