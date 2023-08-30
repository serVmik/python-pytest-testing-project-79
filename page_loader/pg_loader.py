import re
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_paths(page_url, download_dir=None, resource_dir=None):
    """Creates directories and paths for downloaded content and resources"""
    def change_view(view):
        return re.sub('[^a-z0-9]', '-', view.lower()).rstrip()

    download_dir = '' if not download_dir else download_dir
    resource_dir = '' if not resource_dir else resource_dir

    _, base_url = page_url.split('//')
    base_path = os.path.join(download_dir, change_view(base_url))
    url_parse = urlparse(page_url)
    netloc_path = change_view(url_parse.netloc)
    resource_dir = change_view(resource_dir).replace('-png', '.png')

    return {
        'download_dir': download_dir,
        'local_page_path': f'{base_path}.html',
        'local_resources_dir': f'{base_path}_files',
        'local_img_path': f'{base_path}_files/{netloc_path}{resource_dir}',
    }


def replace_attr(page_content: str, tag: str, attr: str, page_url: str) -> str:
    """Replaces attributes in the web page tags"""
    soup = BeautifulSoup(page_content, 'html.parser')
    img_tags = soup.find_all(tag)

    for img_tag in img_tags:
        img_tag[attr] = get_paths(
            page_url,
            resource_dir=img_tag[attr]
        )['local_img_path']

    changed_page_content = soup.prettify()
    return changed_page_content


def save_page_data(page_data: str, file_path: str) -> None:
    """Save html to file path"""
    with open(file_path, 'w') as f:
        f.write(page_data)


def create_dir_local_resources(dir_name):
    os.mkdir(dir_name)


def download(page_url: str, given_dir: str) -> str:
    # Get paths
    paths = get_paths(page_url, given_dir)
    file_path = paths.get('local_page_path')

    # Create dir for local resources
    # os.mkdir(file_path)

    # Get content for save
    page_data: str = requests.get(page_url).text
    changed_page_content = replace_attr(page_data, 'img', 'src', page_url)
    save_page_data(changed_page_content, file_path)

    return file_path
