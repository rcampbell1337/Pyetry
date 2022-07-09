from selenium import webdriver
from typing import List
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from decouple import config

def scrape_poetry_page_and_get_poems(url: str) -> List[str]:
    driver = setup_chrome_driver(["--headless"])
    driver.get(url)
    elements = driver.find_elements(By.TAG_NAME, "a")
    [print(x.get_attribute("href")) for x in elements]
    # soup: bs = bs(page.content, "html.parser")
    # poem_links = remove_user_links([td.find('a')["href"] for td in soup.findAll('td')])
    # full_poems = []
    # for link in poem_links:
    #     single_page_link: str = f"https://www.poetry.com{link}"
    #     single_page: requests.Response = requests.get(single_page_link)
    #     single_page_soup = bs(single_page.content, "html.parser")
    #     print(single_page_soup)
    #     full_poems.append(single_page_soup)
    # return clean_poetry_data(full_poems)
    

def setup_chrome_driver(option_set: List[str]) -> webdriver:
    options = Options()
    for option in option_set:
        options.add_argument(option)
    return webdriver.Chrome(executable_path=config("CHROMEDRIVER_PATH"), options=options)


def remove_user_links(link_list: List[str]) -> List[str]:
    return filter(None, [link if not link.__contains__("user") else None for link in link_list])


def clean_poetry_data(list_of_poems: List[str]) -> List[str]:
    return [poem + ";" for poem in list_of_poems]


def write_line_to_file(file_name: str, poem: str) -> None:
    f = open(file_name, "a")
    f.write(poem)
    f.close()
    
    
def write_poetry_page_to_txt_file(file_name: str, poetry_list: List[str]) -> None:
    for poem in poetry_list:
        write_line_to_file(file_name, poem.replace("\n", " ")) if poem is not None else None


def convert_file_to_csv(txt_file: str, csv_file: str) -> None:
    read_file = pd.read_csv(txt_file, encoding='cp1252')
    read_file.to_csv(csv_file, index=None)


def convert_alot_of_poetry_to_csv():
    for index in range(2):
        write_poetry_page_to_txt_file("poetry_csvs/poetry_list.txt",
                                      scrape_poetry_page_and_get_poems(f"https://www.poetry.com/justadded"))
    convert_file_to_csv("poetry_csvs/poetry_list.txt", "poetry_csvs/poetry_list.csv")


scrape_poetry_page_and_get_poems("https://www.poetry.com/justadded")
