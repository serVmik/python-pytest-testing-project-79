import os
import requests_mock
import tempfile
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from page_loader import pg_loader

"""
        Developer Notes

    1. Optimize code!

"""


class TestDownload:
    page_url_absolute = 'https://ru.hexlet.io/courses'
    page_url_relative = '/courses'
    download_path = '/var/tmp'
    page_name = 'ru-hexlet-io-courses.html'
    resources_dir_name = 'ru-hexlet-io-courses_files'
    resources_dir_path = '/var/tmp/ru-hexlet-io-courses_files'
    page_path = os.path.join(download_path, page_name)

    fixture_loaded_page = './tests/fixtures/step3_page_before.html'
    fixture_expected_page = './tests/fixtures/step3_page_after.html'
    fixture_saved_img = './tests/fixtures/ru-hexlet-io-assets-professions-python.png'
    fixture_saved_script = './tests/fixtures/ru-hexlet-io-packs-js-runtime.js'
    fixture_saved_css = './tests/fixtures/ru-hexlet-io-assets-application.css'
    fixture_saved_html = './tests/fixtures/ru-hexlet-io-courses.html'

    img_loaded_path = '/assets/professions/python.png'
    img_name = 'ru-hexlet-io-assets-professions-python.png'
    img_saved_path = '/var/tmp/ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-python.png'
    img_resource_url = 'https://ru.hexlet.io/assets/professions/python.png'

    script_loaded_path = 'https://ru.hexlet.io/packs/js/runtime.js'
    script_name = 'ru-hexlet-io-packs-js-runtime.js'
    script_saved_path = os.path.join(download_path, resources_dir_name, script_name)
    script_resource_url = urljoin(page_url_absolute, script_loaded_path)

    css_loaded_path = 'https://ru.hexlet.io/assets/application.css'
    css_name = 'ru-hexlet-io-assets-application.css'
    css_saved_path = os.path.join(download_path, resources_dir_name, css_name)
    css_resource_url = urljoin(page_url_absolute, css_loaded_path)

    html_loaded_path = '/courses.html'
    html_name = 'ru-hexlet-io-courses.html'
    html_saved_path = os.path.join(download_path, resources_dir_name, html_name)
    html_resource_url = urljoin(page_url_absolute, html_loaded_path)

    def test_get_paths(self):
        paths = pg_loader.get_paths(
            page_url=self.page_url_absolute,
            download_path=self.download_path,
            attr=self.img_loaded_path
        )
        assert self.page_name == paths['page_name']
        assert self.page_path == paths['page_path']
        assert self.resources_dir_name == paths['resources_dir_name']
        assert self.resources_dir_path == paths['resources_dir_path']
        assert self.img_name == paths['attr_name']
        assert self.img_saved_path == paths['attr_path']

    def test_download(self):
        with open(self.fixture_loaded_page) as f_load_page:
            loaded_page_data = f_load_page.read()
        with open(self.fixture_saved_img, 'rb') as f_img:
            expected_img = f_img.read()
        with open(self.fixture_saved_script, 'rb') as f_src:
            expected_script = f_src.read()
        with open(self.fixture_saved_css, 'rb') as f_css:
            expected_css = f_css.read()
        with open(self.fixture_saved_html, 'rb') as f_html:
            expected_html = f_html.read()

        with open(self.fixture_expected_page) as f_expected_page:
            expected_page_data = f_expected_page.read()
            expected_page_data_prettify = BeautifulSoup(
                expected_page_data,
                'html.parser'
            ).prettify()

        with requests_mock.Mocker() as mock:
            mock.get(self.page_url_absolute, text=loaded_page_data)
            mock.get(self.img_loaded_path, content=expected_img)
            mock.get(self.html_loaded_path, content=expected_html)
            mock.get(self.script_loaded_path, content=expected_script)
            mock.get(self.css_loaded_path, content=expected_css)

            # Call func download, save page data
            with tempfile.TemporaryDirectory() as temp_dir:
                path_current_page_data = pg_loader.download(
                    self.page_url_absolute,
                    temp_dir
                )
                # Read downloaded page data
                with open(path_current_page_data) as fc:
                    current_page_data = fc.read()
                    current_page_data_prettify = BeautifulSoup(
                        current_page_data,
                        'html.parser'
                    ).prettify()

                # Does exist download directory
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
                        self.resources_dir_name
                    )
                )

                # Get path to downloaded img
                # Does exist img
                path_current_img = os.path.join(
                    temp_dir,
                    self.resources_dir_name,
                    self.img_name
                )
                assert os.path.exists(path_current_img)

                # Get path to downloaded script
                # Does exist script
                path_current_script = os.path.join(
                    temp_dir,
                    self.resources_dir_name,
                    self.script_name
                )
                assert os.path.exists(path_current_script)

                # Get path to downloaded css
                # Does exist css
                path_current_css = os.path.join(
                    temp_dir,
                    self.resources_dir_name,
                    self.css_name
                )
                assert os.path.exists(path_current_css)

                # Get path to downloaded html
                # Does exist html
                path_current_html = os.path.join(
                    temp_dir,
                    self.resources_dir_name,
                    self.html_name,
                )
                assert os.path.exists(path_current_html)

                # Reade current img data
                with open(path_current_img, 'rb') as frc:
                    current_resource = frc.read()

                # Saved page content test
                assert expected_page_data_prettify == current_page_data_prettify
                # Saved page resource test
                assert expected_img == current_resource
