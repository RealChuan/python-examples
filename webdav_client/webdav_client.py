import webdav_client_api as WebdavClientApi

import unittest


class WebdavClient(WebdavClientApi):
    def __init__(self, url, username, password, verify_ssl=False):
        super(WebdavClient, self).__init__(url, username, password, verify_ssl)

    def get_file(self, url, local_path, **kwargs):
        return self._get_file(url, local_path, **kwargs)

    def put_file(self, url, local_path, **kwargs):
        return self._put_file(url, local_path, **kwargs)

    def delete_file(self, url, **kwargs):
        return self._delete_file(url, **kwargs)

    def move_file(self, url, destination, **kwargs):
        return self._move_file(url, destination, **kwargs)

    def copy_file(self, url, destination, **kwargs):
        return self._copy_file(url, destination, **kwargs)

    def mkcol_file(self, url, **kwargs):
        return self._mkcol_file(url, **kwargs)

    def lock_file(self, url, **kwargs):
        return self._lock_file(url, **kwargs)

    def unlock_file(self, url, **kwargs):
        return self._unlock_file(url, **kwargs)

    def checkout_file(self, url, **kwargs):
        return self._checkout_file(url, **kwargs)

    def checkin_file(self, url, **kwargs):
        return self._checkin_file(url, **kwargs)

    def propfind_file(self, url, **kwargs):
        return self._propfind_file(url, **kwargs)

    def proppatch_file(self, url, **kwargs):
        return self._proppatch_file(url, **kwargs)

    def search_file(self, url, **kwargs):
        return self._search_file(url, **kwargs)

    def patch_file(self, url, **kwargs):
        return self._patch_file(url, **kwargs)

    def purge_file(self, url, **kwargs):
        return self._purge_file(url, **kwargs)

    def link_file(self, url, **kwargs):
        return self._link_file(url, **kwargs)

    def unlink_file(self, url, **kwargs):
        return self._unlink_file(url, **kwargs)

    def mkactivity_file(self, url, **kwargs):
        return self._mkactivity_file(url, **kwargs)

    def mkcalendar_file(self, url, **kwargs):
        return self._mkcalendar_file(url, **kwargs)

    def subscribe_file(self, url, **kwargs):
        return self._subscribe_file(url, **kwargs)

    def unsubscribe_file(self, url, **kwargs):
        return self._unsubscribe_file(url, **kwargs)

    def rebind_file(self, url, **kwargs):
        return self._rebind_file(url, **kwargs)

    def unbind_file(self, url, **kwargs):
        return self._unbind_file(url, **kwargs)

    def acl_file(self, url, **kwargs):
        return self._acl_file(url, **kwargs)

    def report_file(self, url, **kwargs):
        return self._report_file(url, **kwargs)

    def get_file_content(self, url, **kwargs):
        return self._get_file_content(url, **kwargs)

    def get_file_content_range(self, url, start, end, **kwargs):
        return self._get_file_content_range(url, start, end, **kwargs)

    def get_file_content_length(self, url, **kwargs):
        return self._get_file_content_length(url, **kwargs)

    def get_file_content_length_range(self, url, start, end, **kwargs):
        return self._get_file_content_length_range(url, start, end, **kwargs)


class WebdavTest(unittest.TestCase):
    def setUp(self):
        self.url = "https://localhost:8080"
        self.username = "admin"
        self.password = "admin"
        self.verify_ssl = False
        self.webdav = WebdavClient(
            self.url, self.username, self.password, self.verify_ssl
        )

    def tearDown(self):
        pass

    def test_get_file(self):
        url = "%s/test.txt" % self.url
        local_path = "test.txt"
        self.webdav.get_file(url, local_path)

    def test_put_file(self):
        url = "%s/test.txt" % self.url
        local_path = "test.txt"
        self.webdav.put_file(url, local_path)

    def test_delete_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.delete_file(url)

    def test_move_file(self):
        url = "%s/test.txt" % self.url
        destination = "%s/test2.txt" % self.url
        self.webdav.move_file(url, destination)

    def test_copy_file(self):
        url = "%s/test.txt" % self.url
        destination = "%s/test2.txt" % self.url
        self.webdav.copy_file(url, destination)

    def test_mkcol_file(self):
        url = "%s/test" % self.url
        self.webdav.mkcol_file(url)

    def test_lock_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.lock_file(url)

    def test_unlock_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.unlock_file(url)

    def test_checkout_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.checkout_file(url)

    def test_checkin_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.checkin_file(url)

    def test_propfind_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.propfind_file(url)

    def test_proppatch_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.proppatch_file(url)

    def test_search_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.search_file(url)

    def test_patch_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.patch_file(url)

    def test_purge_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.purge_file(url)

    def test_link_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.link_file(url)

    def test_unlink_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.unlink_file(url)

    def test_mkactivity_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.mkactivity_file(url)

    def test_mkcalendar_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.mkcalendar_file(url)

    def test_subscribe_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.subscribe_file(url)

    def test_unsubscribe_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.unsubscribe_file(url)

    def test_rebind_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.rebind_file(url)

    def test_unbind_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.unbind_file(url)

    def test_acl_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.acl_file(url)

    def test_report_file(self):
        url = "%s/test.txt" % self.url
        self.webdav.report_file(url)

    def test_get_file_content(self):
        url = "%s/test.txt" % self.url
        self.webdav.get_file_content(url)

    def test_get_file_content_range(self):
        url = "%s/test.txt" % self.url
        start = 0
        end = 10
        self.webdav.get_file_content_range(url, start, end)

    def test_get_file_content_length(self):
        url = "%s/test.txt" % self.url
        self.webdav.get_file_content_length(url)

    def test_get_file_content_length_range(self):
        url = "%s/test.txt" % self.url
        start = 0
        end = 10
        self.webdav.get_file_content_length_range(url, start, end)


if __name__ == "__main__":
    unittest.main()
