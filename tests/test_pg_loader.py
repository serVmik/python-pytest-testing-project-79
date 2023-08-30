import requests_mock
import tempfile
from bs4 import BeautifulSoup

from page_loader import pg_loader


class TestDownloadImages:
    page_url = 'https://ru.hexlet.io/courses'
    download_dir = '/var/tmp'
    page_path = '/var/tmp/ru-hexlet-io-courses.html'
    resources_dir = '/var/tmp/ru-hexlet-io-courses_files'
    resource_path = ('/var/tmp/ru-hexlet-io-courses_files/'
                     'ru-hexlet-io-assets-professions-python.png')

    fixture_loaded_page_data = './tests/fixtures/before_download.html'
    fixture_saved_page_data = './tests/fixtures/after_download.html'

    loaded_tag_attr = '/assets/professions/python.png'
    saved_tag_attr = '/var/tmp/ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-python.png'

    def test_get_paths(self):
        paths = pg_loader.get_paths(
            self.page_url,
            self.download_dir,
            self.loaded_tag_attr
        )
        assert self.page_path == paths['page_path']
        assert self.resources_dir == paths['resources_dir']
        assert self.saved_tag_attr == paths['resource_path']

    def test_download(self):
        with open(self.fixture_loaded_page_data) as fb:
            loaded_page_data: str = fb.read()
        with open(self.fixture_saved_page_data) as fa:
            saved_page_data = fa.read()
            saved_page_data_prettify = BeautifulSoup(
                saved_page_data,
                'html.parser'
            ).prettify()

        with requests_mock.Mocker() as mock:
            mock.get(self.page_url, text=loaded_page_data)
            with tempfile.TemporaryDirectory() as temp_dir:
                path_current_page_data = pg_loader.download(
                    self.page_url,
                    temp_dir
                )
                with open(path_current_page_data) as fc:
                    current_page_data = fc.read()
                    current_page_data_prettify = BeautifulSoup(
                        current_page_data,
                        'html.parser'
                    ).prettify()

                assert current_page_data_prettify == saved_page_data_prettify
