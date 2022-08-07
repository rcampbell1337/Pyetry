from DataFetchers.Apis.PoetryOrgApi import PoetryOrgApi
from FileHandlers.FileHandler import FileHandler

if __name__ == '__main__':
    FileHandler(PoetryOrgApi()).write_poems_to_txt_file("./poetry_csvs/long_poetry_list.txt")
    FileHandler.convert_file_to_csv("./poetry_csvs/long_poetry_list.txt", "./poetry_csvs/long_poetry_list.csv")
