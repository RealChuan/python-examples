import requests
import logging
import urllib3
import xml.etree.ElementTree as ET


# disable ssl warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def logResponse(response):
    logger.debug("Content-Type: %s" % response.headers["Content-Type"])
    logger.debug("Content-Length: %s" % response.headers["Content-Length"])
    logger.debug("Content-Disposition: %s" % response.headers["Content-Disposition"])
    logger.debug("Content-Encoding: %s" % response.headers["Content-Encoding"])
    logger.debug("Content-Language: %s" % response.headers["Content-Language"])
    logger.debug("Content-Range: %s" % response.headers["Content-Range"])
    logger.debug("Last-Modified: %s" % response.headers["Last-Modified"])
    logger.debug("Creation-Date: %s" % response.headers["Creation-Date"])
    logger.debug("Expires: %s" % response.headers["Expires"])
    logger.debug("ETag: %s" % response.headers["ETag"])
    logger.debug("Cache-Control: %s" % response.headers["Cache-Control"])
    logger.debug("Expires: %s" % response.headers["Expires"])
    logger.debug("Age: %s" % response.headers["Age"])
    logger.debug("Allow: %s" % response.headers["Allow"])
    logger.debug("Headers: %s" % response.headers)
    logger.debug("Status: %s" % response.status_code)
    logger.debug("Reason: %s" % response.reason)
    logger.debug("Raw: %s" % response.raw)
    logger.debug("Json: %s" % response.json())
    logger.debug("Text: %s" % response.text)
    logger.debug("IterLines: %s" % response.iter_lines())
    logger.debug("IterContent: %s" % response.iter_content())
    logger.debug("Content-MD5: %s" % response.headers["Content-MD5"])
    logger.debug("Content-SHA1: %s" % response.headers["Content-SHA1"])
    logger.debug("Content-SHA256: %s" % response.headers["Content-SHA256"])
    logger.debug("Content-SHA512: %s" % response.headers["Content-SHA512"])


class WebdavClientApi(object):
    def __init__(self, url, username, password, verify_ssl=False):
        self.url = url
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self.session.verify = self.verify_ssl
        self.session.auth = (self.username, self.password)
        self.session.headers.update({"Content-Type": "application/json"})

    def _request(self, method, url, **kwargs):
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s" % e)
            raise e
        except requests.exceptions.ConnectionError as e:
            logger.error("ConnectionError: %s" % e)
            raise e
        except requests.exceptions.Timeout as e:
            logger.error("Timeout: %s" % e)
            raise e
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)
            raise e
        return response

    def _get_file(self, url, local_path, **kwargs):
        try:
            response = self.session.request("GET", url, stream=True, **kwargs)
            response.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s" % e)
            raise e
        except requests.exceptions.ConnectionError as e:
            logger.error("ConnectionError: %s" % e)
            raise e
        except requests.exceptions.Timeout as e:
            logger.error("Timeout: %s" % e)
            raise e
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)
            raise e
        return response

    def _put_file(self, url, local_path, **kwargs):
        try:
            with open(local_path, "rb") as f:
                response = self.session.request("PUT", url, data=f, **kwargs)
                response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s" % e)
            raise e
        except requests.exceptions.ConnectionError as e:
            logger.error("ConnectionError: %s" % e)
            raise e
        except requests.exceptions.Timeout as e:
            logger.error("Timeout: %s" % e)
            raise e
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)
            raise e
        return response

    def _delete_file(self, url, **kwargs):
        try:
            response = self.session.request("DELETE", url, **kwargs)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s" % e)
            raise e
        except requests.exceptions.ConnectionError as e:
            logger.error("ConnectionError: %s" % e)
            raise e
        except requests.exceptions.Timeout as e:
            logger.error("Timeout: %s" % e)
            raise e
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)
            raise e
        return response

    def _move_file(self, url, destination, **kwargs):
        try:
            headers = {"Destination": destination}
            response = self.session.request("MOVE", url, headers=headers, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s" % e)
            raise e
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)
            raise e

    def _copy_file(self, url, destination, **kwargs):
        try:
            headers = {"Destination": destination}
            response = self.session.request("COPY", url, headers=headers, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s" % e)
            raise e
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)
            raise e

    def _mkcol_file(self, url, **kwargs):
        try:
            response = self.session.request("MKCOL", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s" % e)
            raise e
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)
            raise e

    def _lock_file(self, url, **kwargs):
        try:
            response = self.session.request("LOCK", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s" % e)
            raise e
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)
            raise e

    def _unlock_file(self, url, **kwargs):
        try:
            response = self.session.request("UNLOCK", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s" % e)
            raise e
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)
            raise e

    def _checkout_file(self, url, **kwargs):
        try:
            response = self.session.request("CHECKOUT", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s" % e)
            raise e
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)
            raise e

    def _checkin_file(self, url, **kwargs):
        try:
            response = self.session.request("CHECKIN", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s" % e)
            raise e
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)
            raise e

    def _propfind_file(self, url, **kwargs):
        try:
            response = self.session.request("PROPFIND", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s" % e)
            raise e
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)
            raise e

    def _proppatch_file(self, url, **kwargs):
        try:
            response = self.session.request("PROPPATCH", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s" % e)
            raise e
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)
            raise e

    def _search_file(self, url, **kwargs):
        try:
            response = self.session.request("SEARCH", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s" % e)
            raise e

    def _patch_file(self, url, **kwargs):
        try:
            response = self.session.request("PATCH", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s" % e)
            raise e

    def _purge_file(self, url, **kwargs):
        try:
            response = self.session.request("PURGE", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s" % e)
            raise e

    def _link_file(self, url, **kwargs):
        try:
            response = self.session.request("LINK", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s" % e)
            raise e

    def _unlink_file(self, url, **kwargs):
        try:
            response = self.session.request("UNLINK", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.HTTPError as e:
            logger.error("HTTPError: %s" % e)

    def _mkactivity_file(self, url, **kwargs):
        try:
            response = self.session.request("MKACTIVITY", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)

    def _mkcalendar_file(self, url, **kwargs):
        try:
            response = self.session.request("MKCALENDAR", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)

    def _subscribe_file(self, url, **kwargs):
        try:
            response = self.session.request("SUBSCRIBE", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)

    def _unsubscribe_file(self, url, **kwargs):
        try:
            response = self.session.request("UNSUBSCRIBE", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)

    def _rebind_file(self, url, **kwargs):
        try:
            response = self.session.request("REBIND", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)

    def _unbind_file(self, url, **kwargs):
        try:
            response = self.session.request("UNBIND", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)

    def _acl_file(self, url, **kwargs):
        try:
            response = self.session.request("ACL", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)

    def _report_file(self, url, **kwargs):
        try:
            response = self.session.request("REPORT", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Location"]
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)

    def _get_file_content(self, url, **kwargs):
        try:
            response = self.session.request("GET", url, stream=True, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.content
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)

    def _get_file_content_range(self, url, start, end, **kwargs):
        try:
            headers = {"Range": "bytes=%s-%s" % (start, end)}
            response = self.session.request(
                "GET", url, headers=headers, stream=True, **kwargs
            )
            response.raise_for_status()
            logResponse(response)
            return response.content
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)

    def _get_file_content_length(self, url, **kwargs):
        try:
            response = self.session.request("HEAD", url, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Content-Length"]
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)

    def _get_file_content_length_range(self, url, start, end, **kwargs):
        try:
            headers = {"Range": "bytes=%s-%s" % (start, end)}
            response = self.session.request("HEAD", url, headers=headers, **kwargs)
            response.raise_for_status()
            logResponse(response)
            return response.headers["Content-Length"]
        except requests.exceptions.RequestException as e:
            logger.error("RequestException: %s" % e)
