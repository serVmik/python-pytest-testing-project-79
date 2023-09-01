import re
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

"""
        Optimize code!
"""


def get_paths(page_url: str, download_dir=None, resource_name=None, tag=None) -> dict:
    """Creates dirs and paths for downloaded content and resources"""

    def change_view(view: str) -> str:
        return re.sub('[^a-z0-9]', '-', view.lower())

    download_dir: str = '' if not download_dir else download_dir
    resource_name: str = '' if not resource_name else resource_name
    tag: str = '' if not tag else tag

    _, base_url = page_url.split('//')
    base_url = change_view(base_url)
    base_path = os.path.join(download_dir, base_url)
    resource, ext = os.path.splitext(resource_name)

    if resource_name.startswith('http'):
        url_parse = urlparse(resource)
        resource = change_view(url_parse.netloc + url_parse.path)
    else:
        base_url = change_view(urlparse(page_url).netloc)
        resource = f'{base_url}{change_view(resource)}'

    if tag == 'link' and not ext:
        resource = resource + '.html'

    paths = {
        'page_path': f'{base_path}.html',
        'resources_dir': f'{base_path}_files',
        'resource_path': f'{base_path}_files/{resource}{ext}',
    }
    return paths


def replace_attr(page_data: str, page_url: str, ):
    """
    Replaces the value of attributes in web page tags,
    creates list of links to resources.
    """

    soup = BeautifulSoup(page_data, 'html.parser')
    desired_attr_and_tags = {
        'src': soup.find_all({'img', 'script'}, src=True),
        'href': soup.find_all({'link', 'script'}, href=True),
    }
    links = []

    for attr_name, tags in desired_attr_and_tags.items():
        for tag in tags:
            attr = tag[attr_name]
            if not attr.startswith('http'):
                attr = urljoin(page_url, attr)

            """Fix this magic"""
            if attr.endswith('.html'):
                attr += '.html'

            if urlparse(attr).netloc == 'ru.hexlet.io':
                links.append(attr)

                tag[attr_name] = get_paths(
                    page_url,
                    resource_name=attr,
                    tag=tag.name,
                )['resource_path']

    changed_page_data = soup.prettify()
    return changed_page_data, links


def download_resource(page_url: str, download_dir: str, links: list) -> None:
    paths = get_paths(page_url, download_dir)
    if not os.path.exists(paths['resources_dir']):
        os.mkdir(paths['resources_dir'])

    for link in links:
        paths = get_paths(
            page_url,
            download_dir=download_dir,
            resource_name=link
        )
        resource = requests.get(link)

        with open(paths['resource_path'], 'wb') as fr:
            fr.write(resource.content)


def download(page_url: str, download_dir: str) -> str:
    """Downloads the page and its resources, saves them locally"""

    paths = get_paths(page_url, download_dir)
    page_path = paths.get('page_path')
    page_data = requests.get(page_url).text
    changed_page_content, links = replace_attr(page_data, page_url)

    if not os.path.exists(download_dir):
        os.mkdir(download_dir)
    with open(paths['page_path'], 'w') as f:
        f.write(changed_page_content)

    download_resource(page_url, download_dir, links)

    return page_path
