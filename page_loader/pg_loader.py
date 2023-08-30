import re
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_paths(page_url: str, download_dir=None, resource_name=None) -> dict:
    """Creates dirs and paths for downloaded content and resources"""

    def change_view(view: str) -> str:
        return re.sub('[^a-z0-9]', '-', view.lower())

    download_dir: str = '' if not download_dir else download_dir
    resource_name: str = '' if not resource_name else resource_name

    _, base_url = page_url.split('//')
    base_path = os.path.join(download_dir, change_view(base_url))
    url_parse = urlparse(page_url)
    netloc_path = change_view(url_parse.netloc)
    resource_name, ext = os.path.splitext(resource_name)
    resource_name = change_view(resource_name)

    return {
        'page_path': f'{base_path}.html',
        'resources_dir': f'{base_path}_files',
        'resource_path': f'{base_path}_files/{netloc_path}{resource_name}{ext}',
    }


def replace_attr(page_data: str, tag: str, attr: str, page_url: str) -> str:
    """Replaces the value of attributes in the web page tags"""

    soup = BeautifulSoup(page_data, 'html.parser')
    img_tags = soup.find_all(tag)

    for img_tag in img_tags:
        img_tag[attr] = get_paths(
            page_url,
            resource_name=img_tag[attr]
        )['resource_path']

    changed_page_data = soup.prettify()
    return changed_page_data


def download(page_url: str, download_dir: str) -> str:
    """Downloads the page and its resources, saves them locally"""

    paths = get_paths(page_url, download_dir)
    page_path = paths.get('page_path')
    page_data = requests.get(page_url).text
    changed_page_content = replace_attr(page_data, 'img', 'src', page_url)

    with open(paths['page_path'], 'w') as f:
        f.write(changed_page_content)

    os.mkdir(paths['resources_dir'])

    return page_path
