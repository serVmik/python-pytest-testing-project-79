import re
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from .logger_config import logger

"""
        Developer Notes

    1. Optimize code!

"""


def change_view(view):
    return re.sub('[^a-z0-9]', '-', view.lower())


def get_dir_name(page_url: str) -> str:
    base_path, _ = os.path.splitext(page_url)
    _, base_path = base_path.split('//')
    return f'{change_view(base_path)}_files'


def get_dir_path(page_url: str, download_path: str) -> str:
    _, base_path = page_url.split('//')
    dir_path = os.path.join(download_path, change_view(base_path))
    return f'{dir_path}_files'


def get_file_name(page_url: str) -> str:
    if not page_url.endswith('html'):
        page_url += '.html'
    base_path, extension = os.path.splitext(page_url)
    _, base_path = base_path.split('//')
    return f'{change_view(base_path)}{extension}'


def get_attr_name(page_url: str, attr: str) -> str:
    url_parse = urlparse(page_url)
    url_netloc = url_parse.netloc

    attr, extension = os.path.splitext(attr)
    if attr.startswith('http'):
        attr_path = urlparse(attr).path
    else:
        attr_path = attr
    attr_name = change_view(url_netloc + attr_path)

    return f'{attr_name}{extension}'


def get_paths(page_url, download_path=None, attr=None):
    """Creates dirs and paths for downloaded content and resources"""

    download_path = '' if not download_path else download_path
    attr = '' if not attr else attr

    paths = {
        'page_name': get_file_name(page_url),
        'page_path': f'{download_path}/{get_file_name(page_url)}',
        'resources_dir_name': get_dir_name(page_url),
        'resources_dir_path': get_dir_path(page_url, download_path),
        'attr_name': get_attr_name(page_url, attr),
        'attr_path': f'{get_dir_path(page_url, download_path)}/'
                     f'{get_attr_name(page_url, attr)}',
    }
    return paths


def replace_attr(page_url: str, page_data: str):
    """Replaces the value of attributes in web page tags,
       creates list of links to resources."""

    soup = BeautifulSoup(page_data, 'html.parser')
    desired_attr_and_tags = {
        'src': soup.find_all({'img', 'script'}, src=True),
        'href': soup.find_all({'link', 'script'}, href=True),
    }
    links = []

    for attr_name, tags in desired_attr_and_tags.items():
        for tag in tags:
            attr = tag[attr_name]
            _, extension = os.path.splitext(attr)

            if not extension:
                attr += '.html'

            if not attr.startswith('http'):
                attr = urljoin(page_url, attr)

            if urlparse(attr).netloc == 'ru.hexlet.io':
                links.append(attr)

                tag[attr_name] = get_paths(
                    page_url,
                    attr=attr,
                )['attr_path']

    changed_page_data = soup.prettify()
    return changed_page_data, links


def download_resources(page_url: str, download_dir: str, links: list) -> None:
    """Download resources from links"""

    paths = get_paths(page_url, download_dir)

    if not os.path.exists(paths['resources_dir_name']):
        logger.debug(f'Directory {download_dir} does not exist')
        os.mkdir(paths["resources_dir_path"])
        logger.debug(f'Directory {paths["resources_dir_path"]} created')

    for link in links:
        paths = get_paths(
            page_url,
            download_path=download_dir,
            attr=link
        )
        resource = requests.get(link)

        with open(paths['attr_path'], 'wb') as fr:
            fr.write(resource.content)


def download(page_url: str, download_dir: str) -> str:
    """Downloads the page and its resources, saves them locally"""

    page_path = get_paths(page_url, download_dir)['page_path']
    page_data = requests.get(page_url).text
    changed_page_data, links = replace_attr(page_url, page_data)

    if not os.path.exists(download_dir):
        os.mkdir(download_dir)
    with open(page_path, 'w') as f:
        f.write(changed_page_data)

    download_resources(page_url, download_dir, links)
    return page_path
