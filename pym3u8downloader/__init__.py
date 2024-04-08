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

__all__ = [
    "M3U8Downloader",
    "M3U8DownloaderError",
    "__author__",
    "__description__",
    "__name__",
    "__version__"
]
__author__ = "coldsofttech"
__description__ = """
M3U8 Downloader is a Python class designed to download and concatenate video files from M3U8 playlists.
This class provides functionality to handle M3U8 playlist files, download video segments, concatenate them
into a single video file, and manage various error conditions.
"""
__name__ = "pym3u8downloader"
__version__ = "0.1.0"

from pym3u8downloader.__main__ import M3U8Downloader, M3U8DownloaderError
