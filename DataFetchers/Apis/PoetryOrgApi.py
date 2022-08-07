from typing import List
from DataFetchers.IDataFetcher import IDataFetcher
import requests


class PoetryOrgApi(IDataFetcher):
    """
    Class contains all methods necessary to fetch the poetry org
    api for a list of poems.
    """
    __doc__ = IDataFetcher.__doc__ + __doc__

    def __init__(self):
        super().__init__()
        self.titles = requests.get("https://poetrydb.org/title").json()["titles"]

    def get_list_of_poems(self):
        poem_list: List[str] = []
        for title in self.titles:
            poem = requests.get(f"https://poetrydb.org/title/{title}")
            poem_list.append("\n".join(poem.json()[0]["lines"]))
            self.update_and_print_progress_bar()
        return poem_list

    @property
    def number_of_poems(self):
        return len(self.titles)

