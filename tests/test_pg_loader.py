import os
import requests_mock
import tempfile
from bs4 import BeautifulSoup

from page_loader import pg_loader


class TestDownloadImages:
    page_url = 'https://ru.hexlet.io/courses'
    path_page_before = './tests/fixtures/before_download.html'
    path_page_after = './tests/fixtures/after_download.html'
    expected_dir_name = 'ru-hexlet-io-courses_files'
    expected_img_name = 'ru-hexlet-io-assets-professions-python.png'
    expected_img_path = os.path.join(expected_dir_name, expected_img_name)
    img_src_before = '/assets/professions/python.png'
    img_src_after = 'ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-python.png'

    def test_create_dir_name(self):
        dir_name = pg_loader.get_paths(self.page_url)['local_resources_dir']
        assert self.expected_dir_name == dir_name

    def test_create_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir_name:
            paths = pg_loader.get_paths(self.page_url)
            dir_name = paths['local_resources_dir']
            current_dir_name = os.path.join(temp_dir_name, dir_name)
            pg_loader.create_dir_local_resources(current_dir_name)
            assert os.path.exists(current_dir_name) is True

    def test_create_local_img_src(self):
        current_img_src = pg_loader.get_paths(
            self.page_url,
            resource_dir=self.img_src_before
        )['local_img_path']
        assert self.img_src_after == current_img_src

    def test_replace_attr(self):
        with open(self.path_page_before) as fpb:
            page_content_before = fpb.read()
            current_content = pg_loader.replace_attr(
                page_content_before, 'img', 'src', self.page_url)
            current_soup = BeautifulSoup(current_content, 'html.parser')
            current_tags = current_soup.find_all('img')
        with open(self.path_page_after) as fpa:
            page_content_after = fpa.read()
            expected_soup = BeautifulSoup(page_content_after, 'html.parser')
            expected_tags = expected_soup.find_all('img')
        assert expected_tags == current_tags

    def test_download(self):
        with open(self.path_page_before) as fb:
            page_data_before_download: str = fb.read()
        with open(self.path_page_after) as fa:
            page_data_after_download = fa.read()
            page_after = BeautifulSoup(
                page_data_after_download,
                'html.parser'
            ).prettify()
        with requests_mock.Mocker() as mock:
            mock.get(self.page_url, text=page_data_before_download)
            with tempfile.TemporaryDirectory() as directory:
                temp_path_file_html = pg_loader.download(self.page_url, directory)
                with open(temp_path_file_html) as fc:
                    current_data = fc.read()
                    page_current = BeautifulSoup(
                        current_data,
                        'html.parser'
                    ).prettify()
                assert page_current == page_after
