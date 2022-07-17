from Webscapers.IWebscraper import IWebscraper
import pandas as pd
from typing import List


class FileHandler:
    """
    Class writes poetry into a .txt file and can then convert it into .csv
    """
    def __init__(self, webscraper: IWebscraper):
        self.list_of_poems: List[str] = webscraper.scrape_poetry_pages_and_return_a_formatted_poetry_list()

    def write_poems_to_txt_file(self, file_name: str) -> None:
        """
        Writes all of the poems in a poem list to a file.
        :param file_name: The name of the file.
        :return: None.
        """
        for poem in self.list_of_poems:
            self.write_line_to_file(file_name, poem) if poem is not None else None

        # This is deliberately misspelled as a reference to the angry video game nerd:
        # https://youtu.be/Gip-_Fh2Yx0?t=949
        print("CONGLATURATION ! ! !\nYOU HAVE COMPLETED A GREAT POETRY EXPORT."
              "\nAND PROOVED THE JUSTICE OF OUR CULTURE.")

    @staticmethod
    def write_line_to_file(file_name: str, poem: str) -> None:
        """
        Appends a given poem to a file.
        :param file_name: The name of the file.
        :param poem: The poem to be written.
        :return: None.
        """
        f = open(file_name, "a")
        f.write(f"{poem.encode('utf8')}\n")
        f.close()

    @staticmethod
    def convert_file_to_csv(txt_file: str, csv_file: str) -> None:
        """
        Converts a file to a .csv file.
        :param txt_file: The original .txt file.
        :param csv_file: The new .csv file name and location.
        :return: None.
        """
        read_file = pd.read_csv(txt_file, encoding='cp1252', delimiter=';', on_bad_lines='skip')
        read_file.to_csv(csv_file, index=None)