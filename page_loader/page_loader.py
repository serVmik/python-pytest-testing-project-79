import re


def create_file_name(page_url: str) -> str:
    _, url_without_schema = page_url.split('//')
    file_name = re.sub('[^a-z0-9]', '-', url_without_schema.lower()) + '.html'
    return file_name
