
from generalfile.test.test_path import PathTest
from generallibrary import Date
from generalpackager.api.package_hosts.pypi import PyPI


class TestPyPI(PathTest):
    def test_exists(self):
        self.assertEqual(True, PyPI("generalpackager").exists())
        self.assertEqual(False, PyPI("random-package_that,cant.exist").exists())

    def test_get_tarball_url(self):
        pypi = PyPI("generalpackager")
        self.assertEqual(True, pypi.name in pypi._get_tarball_url())
        self.assertEqual(True, pypi.name in pypi._get_tarball_url(version="1.0.0"))

    def test_download(self):
        path = PyPI("generalpackager").download(path="repo")
        self.assertTrue(path.exists())

        with self.assertRaises(AttributeError):
            PyPI("generalpackager").download(path="repo", version="0.0.111")

        path = PyPI("generalpackager").download(path="repo", version="0.0.11", overwrite=True)
        self.assertTrue(path.exists())

    def test_get_owners_packages(self):
        github = PyPI()
        self.assertEqual(set(), {"generallibrary", "generalfile", "generalvector", "generalpackager"}.difference(github.get_owners_packages()))

    def test_get_version(self):
        self.assertEqual(True, PyPI("generalpackager").get_version() > "0.2.0")

    def test_get_date(self):
        self.assertLess(PyPI("generalpackager").get_date(), Date.now())























