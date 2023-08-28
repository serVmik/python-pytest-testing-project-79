import re
import os
import requests


def gat_page_data(page_url: str) -> str:
    return requests.get(page_url).text


def create_file_name(page_url: str) -> str:
    _, url_without_schema = page_url.split('//')
    file_name = re.sub('[^a-z0-9]', '-', url_without_schema.lower()) + '.html'
    return file_name


def create_file_path(directory: str, file_name: str) -> str:
    return os.path.join(directory, file_name)


def save_page_data(page_data: str, file_path: str) -> None:
    with open(file_path, 'w') as f:
        f.write(page_data)


def download(page_url: str, directory: str) -> str:
    page_data: str = gat_page_data(page_url)
    file_name: str = create_file_name(page_url)
    file_path = create_file_path(directory, file_name)
    save_page_data(page_data, file_path)
    return file_path
