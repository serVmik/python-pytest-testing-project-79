import os
import requests_mock
import tempfile

from page_loader import page_loader


class TestPageLoader:
    page_url = 'https://ru.hexlet.io/courses'
    current_path = os.path.dirname(__file__)
    path_temp = '/var/tmp'
    file_name = 'ru-hexlet-io-courses.html'
    expected_path = os.path.join(current_path, 'fixtures', file_name)
    def test_create_path(self):
        path_assert = '/var/tmp/ru-hexlet-io-courses.html'
        path_created = page_loader.create_path(self.page_url, self.path_temp)
        assert path_assert == path_created

    def test_download(self):
        with open(self.expected_path, 'r') as page:
            data = page.read()
        with requests_mock.Mocker() as mock:
            mock.get(self.page_url, text=data)
        with tempfile.TemporaryDirectory() as directory:
            page_loader.download(self.page_url, directory)
            expected_path = os.path.join(directory, self.file_name)
        with open(expected_path) as file:
            file_data = file.read()
        assert data == file_data




# __file__ - это путь к файлу, из которого загружен модуль.
# Соответственно, если не пользоваться данной конструкцией,
# то при обращении из разных каталогов,
# он будет принимать разные значения.
# # И он не всегда содержит абсолютный путь к файлу.
# Использование __file__ в сочетании с различными модулями os.path
# позволяет всем путям относиться к местоположению каталога текущего модуля.
# Это позволяет переносить ваши модули / проекты на другие компьютеры.
