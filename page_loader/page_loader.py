import re
import os


def create_file_name(page_url: str) -> str:
    _, url_without_schema = page_url.split('//')
    file_name = re.sub('[^a-z0-9]', '-', url_without_schema.lower()) + '.html'
    return file_name


def create_file_path(temp_path: str, expected_file_name: str) -> str:
    path: str = os.path.join(temp_path, expected_file_name)
    return path
