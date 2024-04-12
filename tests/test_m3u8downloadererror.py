import unittest

from pym3u8downloader import M3U8DownloaderError


class TestM3U8DownloaderError(unittest.TestCase):
    """Unit test cases for M3U8DownloaderError"""

    def test_init_valid(self):
        """Test if init works as expected"""
        with self.assertRaises(M3U8DownloaderError):
            raise M3U8DownloaderError('Test error')


if __name__ == "__main__":
    unittest.main()
