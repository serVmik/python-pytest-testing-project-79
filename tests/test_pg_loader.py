import os
import requests_mock
import tempfile
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from page_loader import pg_loader


class TestDownloadImages:
    page_url = 'https://ru.hexlet.io/courses'
    download_path = '/var/tmp'
    page_name = 'ru-hexlet-io-courses.html'
    page_path = os.path.join(download_path, page_name)

    fixture_loaded_page = './tests/fixtures/before_download.html'
    fixture_saved_page = './tests/fixtures/after_download.html'
    fixture_saved_resource = ('./tests/fixtures/'
                              'ru-hexlet-io-assets-professions-python.png')

    loaded_path_resource = '/assets/professions/python.png'
    saved_path_resource = '/var/tmp/ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-python.png'
    resources_dir_name = 'ru-hexlet-io-courses_files'
    resources_path = os.path.join(download_path, resources_dir_name)
    resource_name = 'ru-hexlet-io-assets-professions-python.png'
    resource_url = urljoin(page_url, loaded_path_resource)
    resource_path = os.path.join(download_path, resources_path,
                                 resource_name)

    def test_get_paths(self):
        paths = pg_loader.get_paths(
            self.page_url,
            self.download_path,
            self.loaded_path_resource
        )
        assert self.page_path == paths['page_path']
        assert self.resources_path == paths['resources_dir']
        assert self.saved_path_resource == paths['resource_path']

    def test_download(self):
        with open(self.fixture_loaded_page) as fb:
            loaded_page_data = fb.read()
        with open(self.fixture_saved_page) as fa:
            saved_page_data = fa.read()
            saved_page_data_prettify = BeautifulSoup(
                saved_page_data,
                'html.parser'
            ).prettify()
        with open(self.fixture_saved_resource, 'rb') as fre:
            expected_resource = fre.read()

        with requests_mock.Mocker() as mock:
            mock.get(self.page_url, text=loaded_page_data)
            mock.get(self.resource_url, content=expected_resource)

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

                path_current_resource = os.path.join(
                    temp_dir,
                    self.resources_dir_name,
                    self.resource_name
                )

                assert os.path.exists(temp_dir)
                assert os.path.exists(
                    os.path.join(temp_dir, self.page_name)
                )
                assert os.path.exists(
                    os.path.join(temp_dir, self.resources_dir_name)
                )
                assert os.path.exists(
                    os.path.join(temp_dir,
                                 self.resources_dir_name,
                                 self.resource_name)
                )
                assert os.path.exists(path_current_resource)

                with open(path_current_resource, 'rb') as frc:
                    current_resource = frc.read()

                assert saved_page_data_prettify == current_page_data_prettify
                assert expected_resource == current_resource
