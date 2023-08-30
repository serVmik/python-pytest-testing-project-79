import os
import requests_mock
import tempfile

from page_loader import pg_loader

page_url = 'https://ru.hexlet.io/courses'
current_path = os.path.dirname(__file__)


class TestDownload:
    expected_file_name = 'ru-hexlet-io-courses.html'
    temp_path = '/var/tmp'
    expected_path = '/var/tmp/ru-hexlet-io-courses.html'
    path_mock_data = './tests/fixtures/page_mock.html'
    path_expected_data = os.path.join(current_path, 'fixtures',
                                      expected_file_name)

    def test_create_file_name(self):
        file_name = pg_loader.create_file_name(page_url)
        assert self.expected_file_name == file_name

    def test_create_file_path(self):
        file_path = pg_loader.create_file_path(
            self.temp_path,
            self.expected_file_name
        )
        assert self.expected_path == file_path

    def test_download(self):
        # read expected_data from fixture
        with open(self.path_expected_data) as fe:
            expected_data = fe.read()
        # read page_mock_data from fixture
        with open(self.path_mock_data, 'r') as fm:
            page_mock_data = fm.read()
        # add page_mock_data to mock
        with requests_mock.Mocker() as mock:
            mock.get(page_url, text=page_mock_data)
            # create temp directory
            with tempfile.TemporaryDirectory() as directory:
                # run download()
                # get temp_file_path
                # save page_mock_data to temp_file
                temp_file_path = pg_loader.download(page_url, directory)
                # is temp_file exists
                assert os.path.exists(temp_file_path) is True
                # read page_mock_data from temp_file
                with open(temp_file_path) as fc:
                    current_data = fc.read()
                assert current_data == expected_data


class TestDownloadImages:
    path_page_before_download = './tests/fixtures/before_download.html'
    path_page_after_download = './tests/fixtures/after_download.html'
    expected_dir_name = 'ru-hexlet-io-courses_files'
    expected_img_name = 'ru-hexlet-io-assets-professions-python.png'
    expected_img_path = os.path.join(expected_dir_name, expected_img_name)

    def test_create_dir_name(self):
        dir_name = pg_loader.create_dir_name(page_url)
        assert self.expected_dir_name == dir_name

    def test_create_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir_name:
            dir_name = pg_loader.create_dir_name(page_url)
            current_dir_name = os.path.join(temp_dir_name, dir_name)
            pg_loader.create_dir(current_dir_name)
            assert os.path.exists(current_dir_name) is True

    def test_create_img_name(self):
        current_img_name = pg_loader.create_local_img_name(page_url)
        assert self.expected_img_name == current_img_name

    def test_download_img(self):
        pass

    def test_download(self):
        with open(self.path_page_before_download) as fb:
            page_data_before_download: str = fb.read()
        with open(self.path_page_after_download) as fa:
            page_data_after_download = fa.read()
        with tempfile.TemporaryDirectory() as temp_dir:
            with requests_mock.Mocker() as mock:
                mock.get(page_url, text=page_data_before_download)
                temp_path_file_html = pg_loader.download(page_url, temp_dir)
                # does temp_html exists
                assert os.path.exists(temp_path_file_html) is True
                # does temp_img exists
                temp_img_path = os.path.join(temp_dir, self.expected_img_path)
                assert os.path.exists(temp_img_path)
                # does change page_data
                with open(temp_path_file_html) as fc:
                    current_data = fc.read()
                assert current_data == page_data_after_download
