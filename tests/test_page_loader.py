from page_loader import page_loader


class TestPageLoader:
    url_for_path = 'https://ru.hexlet.io/courses'
    path_dir = '/var/tmp'

    def test_create_path(self):
        path_assert = '/var/tmp/ru-hexlet-io-courses.html'
        path_created = page_loader.create_path(self.url_for_path, self.path_dir)
        assert path_assert == path_created
