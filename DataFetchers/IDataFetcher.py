from abc import abstractmethod
from typing import List


class IDataFetcher:
    """
    Interface that defines a method used to return a list of poems in a string format.
    """
    def __init__(self):
        self.number_of_poems_processed = 0

    @abstractmethod
    def get_list_of_poems(self) -> List[str]:
        """
        Adds poems to the poetry list based on the number requested then returns the formatted
        poetry list.
        :return: A list of poems.
        """
        pass

    @property
    @abstractmethod
    def number_of_poems(self):
        pass

    def update_and_print_progress_bar(self):
        self.number_of_poems_processed += 1
        self.print_progress_bar(self.number_of_poems_processed, prefix='Progress:', suffix='Complete', length=50)

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
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(self.number_of_poems)))
        filled_length = int(length * iteration // self.number_of_poems)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}')
        # Print New Line on Complete
        if iteration == self.number_of_poems:
            print()