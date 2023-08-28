import os
import requests_mock
import tempfile

from page_loader import page_loader


class TestPageLoader:
    page_url = 'https://ru.hexlet.io/courses'
    expected_file_name = 'ru-hexlet-io-courses.html'
    temp_path = '/var/tmp'
    current_path = os.path.dirname(__file__)
    expected_path = '/var/tmp/ru-hexlet-io-courses.html'
    path_mock_data = './tests/fixtures/page_mock.html'
    path_expected_data = os.path.join(current_path, 'fixtures',
                                      expected_file_name)

    def test_create_file_name(self):
        file_name = page_loader.create_file_name(self.page_url)
        assert self.expected_file_name == file_name

    def test_create_file_path(self):
        file_path = page_loader.create_file_path(
            self.temp_path, self.expected_file_name
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
            mock.get(self.page_url, text=page_mock_data)
            # create temp directory
            with tempfile.TemporaryDirectory() as directory:
                # run download()
                # get temp_file_path
                # save page_mock_data to temp_file
                temp_file_path = page_loader.download(self.page_url, directory)
                # is temp_file exists
                assert os.path.exists(temp_file_path) is True
                # read current_data from temp_file
                with open(temp_file_path) as fc:
                    current_data = fc.read()
                assert current_data == expected_data
