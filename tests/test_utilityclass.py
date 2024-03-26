# Copyright (c) 2024 coldsofttech
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import tempfile
import unittest
from unittest.mock import patch

import requests

from commonclass import CommonClass
from pym3u8downloader.__main__ import UtilityClass


class TestUtilityClass(unittest.TestCase):
    """Unit test cases for UtilityClass"""

    def test_are_paths_on_same_disk_valid_on_same_disk(self):
        """Test if are paths on same disk works as expected"""
        path1, path2 = CommonClass.generate_sample_file_paths(True)
        self.assertTrue(UtilityClass.are_paths_on_same_disk(path1, path2))

    def test_are_paths_on_same_disk_valid_on_different_disk(self):
        """Test if are paths on same disk works as expected"""
        if len(CommonClass.get_available_disks()) > 1:
            path1, path2 = CommonClass.generate_sample_file_paths(False)
            self.assertFalse(UtilityClass.are_paths_on_same_disk(path1, path2))
        else:
            self.skipTest('Skipping test_are_paths_on_same_disk_valid_on_different_disk: Only one disk available.')

    def test_are_paths_on_same_disk_invalid_path1(self):
        """Test if are paths on same disk raises TypeError"""
        with self.assertRaises(TypeError):
            UtilityClass.are_paths_on_same_disk(100, 'Test')

    def test_are_paths_on_same_disk_invalid_path2(self):
        """Test if are paths on same disk raises TypeError"""
        with self.assertRaises(TypeError):
            UtilityClass.are_paths_on_same_disk('Test', 100)

    @patch('requests.get')
    def test_is_internet_connected_connected(self, mock_get):
        """Test if is internet connected works as expected"""
        mock_get.return_value.status_code = 200
        self.assertTrue(UtilityClass.is_internet_connected())

    @patch('requests.get')
    def test_is_internet_connected_disconnected(self, mock_get):
        """Test if is internet connected works as expected"""
        mock_get.side_effect = requests.ConnectionError
        self.assertFalse(UtilityClass.is_internet_connected())

    def test_is_m3u8_url_valid(self):
        """Test if is m3u8 url works as expected"""
        url = f'{CommonClass.get_git_test_parent_url()}/sample_index.m3u8'
        self.assertTrue(UtilityClass.is_m3u8_url(url))

    def test_is_m3u8_url_invalid(self):
        """Test if is m3u8 url works as expected"""
        url = f'{CommonClass.get_git_test_parent_url()}/sample_video1.mp4'
        self.assertFalse(UtilityClass.is_m3u8_url(url))

    def test_is_m3u8_url_invalid_url(self):
        """Test if is m3u8 url raises TypeError"""
        with self.assertRaises(TypeError):
            UtilityClass.is_m3u8_url(100)

    def test_is_url_valid_http(self):
        """Test if is url works as expected"""
        url = f'{CommonClass.get_git_test_parent_url()}/sample_index.m3u8'
        self.assertTrue(UtilityClass.is_url(url))

    def test_is_url_valid_https(self):
        """Test if is url works as expected"""
        url = f'{CommonClass.get_git_test_parent_url()}/sample_index.m3u8'
        self.assertTrue(UtilityClass.is_url(url))

    def test_is_url_invalid(self):
        """Test if is url works as expected"""
        url = f'junk//{CommonClass.get_git_test_parent_url()}/sample_index.m3u8'
        self.assertFalse(UtilityClass.is_url(url))

    def test_is_url_invalid_url(self):
        """Test if is url raises TypeError"""
        with self.assertRaises(TypeError):
            UtilityClass.is_url(100)

    def test_random_string_valid_single(self):
        """Test if random string works as expected"""
        return_value = UtilityClass.random_string()
        self.assertIsInstance(return_value, str)
        self.assertEqual(10, len(return_value))

    def test_random_string_valid_multiple(self):
        """Test if random string works as expected"""
        return_value1 = UtilityClass.random_string()
        return_value2 = UtilityClass.random_string()
        self.assertNotEqual(return_value1, return_value2)

    def test_random_string_invalid(self):
        """Test if random string raises TypeError"""
        with self.assertRaises(TypeError):
            UtilityClass.random_string('length10')

    def test_download_file_valid(self):
        """Test if download file works as expected"""
        url = f'{CommonClass.get_git_test_parent_url()}/sample_index.m3u8'
        file_name = CommonClass.generate_name('m3u8')
        try:
            UtilityClass.download_file(url, file_name)
            with open(file_name, 'r') as file:
                file_content = file.read()
                self.assertIn('#EXTM3U', file_content)
        finally:
            try:
                os.remove(file_name)
            except (FileNotFoundError, PermissionError, IsADirectoryError):
                pass

    def test_download_file_invalid_file(self):
        """Test if download file works as expected"""
        url = f'{CommonClass.get_git_test_parent_url()}/junk.m3u8'
        file_name = CommonClass.generate_name('m3u8')
        try:
            UtilityClass.download_file(url, file_name)
            self.assertFalse(os.path.exists(file_name))
        finally:
            try:
                os.remove(file_name)
            except (FileNotFoundError, PermissionError, IsADirectoryError):
                pass

    @patch('requests.get')
    def test_download_file_invalid(self, mock_get):
        """Test if download file raises RequestException"""
        mock_get.side_effect = requests.RequestException('Connection error')
        url = f'{CommonClass.get_git_test_parent_url()}/junk.m3u8'
        file_name = CommonClass.generate_name('m3u8')
        try:
            with self.assertRaises(requests.RequestException):
                UtilityClass.download_file(url, file_name)
        finally:
            try:
                os.remove(file_name)
            except (FileNotFoundError, PermissionError, IsADirectoryError):
                pass

    def test_download_file_invalid_url(self):
        """Test if download file raises TypeError"""
        url = 100
        file_name = CommonClass.generate_name('m3u8')
        try:
            with self.assertRaises(TypeError):
                UtilityClass.download_file(url, file_name)
        finally:
            try:
                os.remove(file_name)
            except (FileNotFoundError, PermissionError, IsADirectoryError):
                pass

    def test_download_file_invalid_file_name(self):
        """Test if download file raises TypeError"""
        url = f'{CommonClass.get_git_test_parent_url()}/sample_index.m3u8'
        file_name = 100
        with self.assertRaises(TypeError):
            UtilityClass.download_file(url, file_name)

    def test_get_content_length_valid(self):
        """Test if the get content length works as expected"""
        url = f'{CommonClass.get_git_test_parent_url()}/sample_index.m3u8'
        size = UtilityClass.get_content_length(url)
        assert size > 0

    def test_get_content_length_invalid1(self):
        """Test if the get content length works as expected"""
        url = f'{CommonClass.get_git_test_parent_url()}/junk.m3u8'
        size = UtilityClass.get_content_length(url)
        assert size == 0

    @patch('requests.get')
    def test_get_content_length_invalid2(self, mock_get):
        """Test if the get content length works as expected"""
        mock_get.side_effect = requests.RequestException('Connection error')
        url = f'{CommonClass.get_git_test_parent_url()}/junk.m3u8'
        size = UtilityClass.get_content_length(url)
        assert size == 0

    def test_get_content_length_invalid_file(self):
        """Test if get content length raises TypeError"""
        url = 100
        with self.assertRaises(TypeError):
            UtilityClass.get_content_length(url)

    def test_is_space_available_valid_space(self):
        """Test if is space available works as expected"""
        folder_name = tempfile.gettempdir()
        self.assertTrue(UtilityClass.is_space_available(folder_name, 10))

    def test_is_space_available_invalid_space(self):
        """Test if is space available works as expected"""
        folder_name = tempfile.gettempdir()
        self.assertFalse(UtilityClass.is_space_available(folder_name, 2000000000000))

    def test_is_space_available_invalid_folder_path(self):
        """Test if is space available raises TypeError"""
        with self.assertRaises(TypeError):
            UtilityClass.is_space_available(100, 100)

    def test_is_space_available_invalid_required(self):
        """Test if is space available raises TypeError"""
        folder_name = tempfile.gettempdir()
        with self.assertRaises(TypeError):
            UtilityClass.is_space_available(folder_name, 100.10)


if __name__ == "__main__":
    unittest.main()
