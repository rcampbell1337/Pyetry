from FileHandlers.FileHandler import FileHandler
from Webscapers.SeleniumPoetryFoundation import SeleniumPoetryFoundation

if __name__ == '__main__':
    # FileHandler(SeleniumPoetryFoundation(50)).write_poems_to_txt_file("./poetry_csvs/poems.txt")
    FileHandler.convert_file_to_csv("./poetry_csvs/poems.txt", "./poetry_csvs/poems.csv")
