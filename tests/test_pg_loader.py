import os
import requests_mock
import pytest
import tempfile
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from page_loader import pg_loader


class TestDownload:
    page_url = 'https://ru.hexlet.io/courses'
    download_path = '/var/tmp'
    page_name = 'ru-hexlet-io-courses.html'
    dir_resources_name = 'ru-hexlet-io-courses_files'
    page_path = os.path.join(download_path, page_name)

    fixture_pages = [
        ('./tests/fixtures/step3_page_before.html',
         './tests/fixtures/step3_page_after.html',
         './tests/fixtures/ru-hexlet-io-assets-professions-python.png',
         './tests/fixtures/ru-hexlet-io-packs-js-runtime.js'),
    ]

    loaded_path_img = '/assets/professions/python.png'
    img_name = 'ru-hexlet-io-assets-professions-python.png'
    saved_path_img = os.path.join(download_path, dir_resources_name, img_name)
    img_path = os.path.join(download_path, dir_resources_name)
    img_resource_url = urljoin(page_url, loaded_path_img)

    loaded_path_script = 'https://ru.hexlet.io/packs/js/runtime.js'
    script_name = 'ru-hexlet-io-packs-js-runtime.js'
    saved_path_script = os.path.join(download_path, dir_resources_name, script_name)
    script_path = os.path.join(download_path, dir_resources_name)
    script_resource_url = urljoin(page_url, loaded_path_script)

    def test_get_paths(self):
        paths = pg_loader.get_paths(
            self.page_url,
            self.download_path,
            self.loaded_path_img
        )
        assert self.page_path == paths['page_path']
        assert self.img_path == paths['resources_dir']
        assert self.saved_path_img == paths['resource_path']

    @pytest.mark.parametrize('fixture_loaded_page, fixture_saved_page,'
                             'fixture_saved_img, fixture_saved_script',
                             fixture_pages)
    def test_download(self, fixture_loaded_page, fixture_saved_page,
                      fixture_saved_img, fixture_saved_script):
        with open(fixture_loaded_page) as fb:
            loaded_page_data = fb.read()
        with open(fixture_saved_page) as fa:
            saved_page_data = fa.read()
            saved_page_data_prettify = BeautifulSoup(
                saved_page_data,
                'html.parser'
            ).prettify()
        with open(fixture_saved_img, 'rb') as fi:
            expected_img = fi.read()
        with open(fixture_saved_script, 'rb') as fs:
            expected_script = fs.read()

        with requests_mock.Mocker() as mock:
            mock.get(self.page_url, text=loaded_page_data)
            mock.get(self.img_resource_url, content=expected_img)
            mock.get(self.script_resource_url, content=expected_script)

            # Call func download, save page data
            with tempfile.TemporaryDirectory() as temp_dir:
                path_current_page_data = pg_loader.download(
                    self.page_url,
                    temp_dir
                )
                # Read downloaded page data
                with open(path_current_page_data) as fc:
                    current_page_data = fc.read()
                    current_page_data_prettify = BeautifulSoup(
                        current_page_data,
                        'html.parser'
                    ).prettify()

                # Get path to downloaded resource
                path_current_resource = os.path.join(
                    temp_dir,
                    self.dir_resources_name,
                    self.img_name
                )
                # Does exists download directory
                assert os.path.exists(temp_dir)
                # Does exists page
                assert os.path.exists(
                    os.path.join(
                        temp_dir,
                        self.page_name
                    )
                )
                # Does exists resources directory
                assert os.path.exists(
                    os.path.join(
                        temp_dir,
                        self.dir_resources_name
                    )
                )
                # Does exists resource
                assert os.path.exists(path_current_resource)

                with open(path_current_resource, 'rb') as frc:
                    current_resource = frc.read()

                # Saved page content test
                assert saved_page_data_prettify == current_page_data_prettify
                # Saved page resource test
                assert expected_img == current_resource
