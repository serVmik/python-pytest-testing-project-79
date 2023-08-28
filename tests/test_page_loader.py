import os

from page_loader import page_loader


class TestPageLoader:
    page_url = 'https://ru.hexlet.io/courses'
    current_path = os.path.dirname(__file__)
    expected_file_name = 'ru-hexlet-io-courses.html'
    path_to_file_with_expected_page = os.path.join(
        current_path, 'fixtures', expected_file_name
        )
    temp_path = '/var/tmp'
    expected_path = '/var/tmp/ru-hexlet-io-courses.html'

    def test_create_file_name(self):
        file_name = page_loader.create_file_name(self.page_url)
        assert self.expected_file_name == file_name

    def test_create_file_path(self):
        file_path = page_loader.create_file_path(
            self.temp_path, self.expected_file_name
            )
        assert self.expected_path == file_path
