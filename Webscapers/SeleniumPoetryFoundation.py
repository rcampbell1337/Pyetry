from selenium import webdriver
from typing import List

from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from Webscapers.IWebscraper import IWebscraper


class SeleniumPoetryFoundation(IWebscraper):
    """
    Class contains all methods necessary to scrape a the poetry foundation
    website for a list of poems.
    """
    __doc__ = IWebscraper.__doc__ + __doc__

    def __init__(self, number_of_pages: int):
        self.driver = self.setup_chrome_driver(["--headless"])
        self.list_of_poems: List[str] = []
        self.number_of_pages = number_of_pages
        self.number_of_poems_to_process = number_of_pages * 20
        self.number_of_poems_processed = 0

    def scrape_poetry_pages_and_return_a_formatted_poetry_list(self) -> List[str]:
        """
        The Poetry Foundation implementation.
        """
        for i in range(1, self.number_of_pages + 1):
            url: str = f"https://www.poetryfoundation.org/poems/browse#page={i}&sort_by=recently_added"
            self.scrape_poetry_page_and_add_to_poetry_list(url)
        return self.format_and_return_a_clean_list_of_poems()

    def scrape_poetry_page_and_add_to_poetry_list(self, url) -> None:
        """
        Scrapes a given poetry page and returns all of the poems on that page in a list format.
        :return: A list of poems.
        """
        self.driver.refresh()
        self.driver.get(url)
        elements: WebElement = self.driver.find_element(By.CLASS_NAME, "c-assetViewport")
        received_links = False
        all_links: List[str] = []

        # TODO: Write something actually good here
        while not received_links:
            try:
                poem_links = elements.find_elements(By.TAG_NAME, "a")
                all_links = [link.get_attribute("href") for link in poem_links]
                received_links = True
            except StaleElementReferenceException:
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
            self.number_of_poems_processed += 1
            self.print_progress_bar(self.number_of_poems_processed, prefix='Progress:', suffix='Complete', length=50)

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

    def print_progress_bar(self, iteration, prefix='', suffix='', decimals=1, length=100, fill='█',
                           print_end="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(self.number_of_poems_to_process)))
        filled_length = int(length * iteration // self.number_of_poems_to_process)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}')
        # Print New Line on Complete
        if iteration == self.number_of_poems_to_process:
            print()
