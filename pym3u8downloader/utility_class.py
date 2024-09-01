import os
import platform
import random
import shutil
import string
import warnings
from typing import Optional
from urllib.parse import urlparse

from pym3u8downloader.validations import validate_type


class UtilityClass:
    """
    Utility class containing static methods for common tasks such as file download, checking internet connection,
    generating random strings, etc.
    """

    @staticmethod
    def are_paths_on_same_disk(path1: str, path2: str) -> bool:
        """
        Check if two paths are on the same disk.

        :param path1: The first path.
        :type path1: str
        :param path2: The second path.
        :type path2: str
        :return: True if the paths are on the same disk, False otherwise.
        :rtype: bool
        """
        validate_type(path1, str, 'path1 should be a string.')
        validate_type(path2, str, 'path2 should be a string.')

        mount_point1 = os.path.abspath(path1)
        while not os.path.ismount(mount_point1):
            mount_point1 = os.path.dirname(mount_point1)

        mount_point2 = os.path.abspath(path2)
        while not os.path.ismount(mount_point2):
            mount_point2 = os.path.dirname(mount_point2)

        return mount_point1 == mount_point2

    @staticmethod
    def download_file(url: str, file_name: str, verify_ssl: bool = True) -> None:
        """
        Download a file from a URL and save it to disk.

        :param url: The URL to download the file from.
        :type url: str
        :param file_name: The name of the file to save.
        :type file_name: str
        :param verify_ssl: A flag to verify SSL for https-based input URLs
        :type verify_ssl: bool
        """
        import requests

        validate_type(url, str, 'url should be a string.')
        validate_type(file_name, str, 'file_name should be a string.')
        validate_type(verify_ssl, bool, 'verify_ssl should be a boolean.')

        parsed_url = urlparse(url)
        if not verify_ssl and parsed_url.scheme == 'https':
            warnings.filterwarnings('ignore', message='Unverified HTTPS request')

        try:
            response = requests.get(url, verify=verify_ssl)
            if response.status_code == 200:
                with open(file_name, 'wb') as downloaded_file:
                    downloaded_file.write(response.content)
        except requests.RequestException as e:
            raise e

    @staticmethod
    def get_content_length(file: str) -> int:
        """
        Get the content length of a file from its URL.

        :param file: The URL of the file.
        :type file: str
        :return: The content length of the file, or 0 if the file is not found or cannot be accessed.
        :rtype: int
        """
        import requests

        def get_final_url(url: str) -> str:
            """
            Get the final URL after following redirects.

            :param url: The original URL
            :type url: str
            :return: The final URL after following redirects, or the original URL if no redirect occurred
            :rtype: str
            """
            try:
                final_url_response = requests.head(url, allow_redirects=True)
                return final_url_response.url
            except requests.RequestException:
                return url

        validate_type(file, str, 'file should be a string.')

        try:
            final_url = get_final_url(file)
            response = requests.head(final_url)
            if response.status_code == 200:
                content_length = response.headers.get('Content-Length')
                if content_length is not None:
                    return int(content_length)
        except requests.RequestException:
            pass

        return 0

    @staticmethod
    def is_internet_connected() -> bool:
        """
        Check if the internet connection is available.

        :return: True if the internet connection is available, False otherwise.
        :rtype: bool
        """
        import requests

        try:
            requests.get('http://www.github.com', timeout=5)
            return True
        except requests.ConnectionError:
            return False

    @staticmethod
    def is_m3u8_url(value: str) -> bool:
        """
       Check if a URL ends with ".m3u8".

       :param value: The URL to check.
       :type value: str
       :return: True if the URL ends with ".m3u8", False otherwise.
       :rtype: bool
       """
        validate_type(value, str, 'value should be a string.')
        return value.endswith('.m3u8')

    @staticmethod
    def is_space_available(folder_path: str, required: int) -> bool:
        """
        Check if there is enough free space available in a folder.

        :param folder_path: The path to the folder.
        :type folder_path: str
        :param required: The required amount of free space in bytes.
        :type required: int
        :return: True if there is enough free space, False otherwise.
        :rtype: bool
        """
        validate_type(folder_path, str, 'folder_path should be a string.')
        validate_type(required, int, 'required should be an integer.')

        if platform.system().lower() == 'windows':
            folder_path = os.path.dirname(folder_path)

        while not os.path.exists(folder_path):
            folder_path = os.path.dirname(folder_path)
            if not folder_path:
                return False

        total, used, free = shutil.disk_usage(folder_path)
        return free >= required

    @staticmethod
    def is_url(value: str) -> bool:
        """
        Check if a string is a valid URL.

        :param value: The string to check.
        :type value: str
        :return: True if the string is a valid URL, False otherwise.
        :rtype: bool
        """
        validate_type(value, str, 'value should be a string.')
        parsed_url = urlparse(value)
        return bool(parsed_url.scheme) and bool(parsed_url.netloc)

    @staticmethod
    def random_string(length: Optional[int] = 10) -> str:
        """
        Generate a random string of specified length.

        :param length: The length of the random string (default is 10).
        :type length: Optional[int]
        :return: The randomly generated string.
        :rtype: str
        """
        validate_type(length, int, 'length should be an integer.')
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
