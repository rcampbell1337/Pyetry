from selenium import webdriver
from typing import List
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class PoemScraper:
    """
    Class contains all methods necessary to scrape a poetry website for a list of poems.
    """
    def __init__(self):
        self.driver = self.setup_chrome_driver(["--headless"])
        self.list_of_poems: List[str] = []
        self.url = f"https://www.poetryfoundation.org/poems/browse#page=1&sort_by=recently_added"

    def scrape_poetry_page_and_get_poems(self) -> List[str]:
        """
        Scrapes a given poetry page and returns all of the poems on that page in a list format.
        :return: A list of poems.
        """
        self.driver.get(self.url)
        elements: WebElement = self.driver.find_element(By.CLASS_NAME, "c-assetViewport")
        poem_links: List[WebElement] = elements.find_elements(By.TAG_NAME, "a")
        all_links: List[str] = [x.get_attribute("href") for x in poem_links]
        list_of_poems: List[str] = []
        for link in all_links:
            self.add_valid_poem_to_list(link)
        return self.remove_useless_formatting(list_of_poems)

    def add_valid_poem_to_list(self, link: str) -> None:
        """
        Checks that a poem has content then if it does add it to the list of poems.
        :param link: The link for the poem page.
        :return: None.
        """
        self.driver.get(link)
        selected_poem: List[WebElement] = self.driver.find_elements(By.CLASS_NAME, "o-poem")
        if len(selected_poem) > 0:
            self.list_of_poems.append(selected_poem[0].get_attribute("innerText"))

    @staticmethod
    def remove_useless_formatting(poems: List[str]) -> List[str]:
        """
        An actually quite tricky method, has to remove all of the unnecessary unicode formatting provided by
        https://www.poetryfoundation.org/ (Thanks for that!!!)
        Removes all of the escape characters, and foreign languages from the list of poems retrieved.
        :param poems: The list of poems to be formatted.
        :return: A list of beautifully formatted poems for CSV conversion.
        """
        escapes = ''.join([chr(char) for char in range(1, 32)])
        translator = str.maketrans('', '', escapes)

        # Remove any extra jazz from the strings
        return [poem.translate(translator).replace("\u2003", " ").replace("\xa0", " ") for poem in poems]

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

    def write_poetry_page_to_txt_file(self, file_name: str) -> None:
        """
        Writes all of the poems in a poem list to a file.
        :param file_name: The name of the file.
        :return: None.
        """
        for poem in self.list_of_poems:
            self.write_line_to_file(file_name, poem.replace("\n", " ")) if poem is not None else None

    def convert_alot_of_poetry_to_csv(self):
        """
        The factory method which will generate all of the poetry data for the AI.
        :return: None.
        """
        for index in range(2):
            self.write_poetry_page_to_txt_file("poetry_csvs/poetry_list.txt")
        self.convert_file_to_csv("poetry_csvs/poetry_list.txt", "poetry_csvs/poetry_list.csv")

    @staticmethod
    def convert_file_to_csv(txt_file: str, csv_file: str) -> None:
        """
        Converts a file to a .csv file.
        :param txt_file: The original .txt file.
        :param csv_file: The new .csv file name and location.
        :return: None.
        """
        read_file = pd.read_csv(txt_file, encoding='cp1252')
        read_file.to_csv(csv_file, index=None)

    @staticmethod
    def write_line_to_file(file_name: str, poem: str) -> None:
        """
        Appends a given poem to a file.
        :param file_name: The name of the file.
        :param poem: The poem to be written.
        :return: None.
        """
        f = open(file_name, "a")
        f.write(poem)
        f.close()


print(PoemScraper().scrape_poetry_page_and_get_poems())
