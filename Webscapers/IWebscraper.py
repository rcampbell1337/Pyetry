from typing import List


class IWebscraper:
    """
    Interface that defines a method used to return a list of poems in a string format.
    """
    def scrape_poetry_pages_and_return_a_formatted_poetry_list(self) -> List[str]:
        """
        Adds poems to the poetry list based on the number requested then returns the formatted
        poetry list.
        :return: A list of poems.
        """
        pass
