import os
import platform
import random
import shutil
import string
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, TextIO
from urllib.parse import urlparse


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
        if not isinstance(path1, str):
            raise TypeError('path1 should be a string.')
        elif not isinstance(path2, str):
            raise TypeError('path2 should be a string.')

        mount_point1 = os.path.abspath(path1)
        while not os.path.ismount(mount_point1):
            mount_point1 = os.path.dirname(mount_point1)

        mount_point2 = os.path.abspath(path2)
        while not os.path.ismount(mount_point2):
            mount_point2 = os.path.dirname(mount_point2)

        return mount_point1 == mount_point2

    @staticmethod
    def download_file(url: str, file_name: str) -> None:
        """
        Download a file from a URL and save it to disk.

        :param url: The URL to download the file from.
        :type url: str
        :param file_name: The name of the file to save.
        :type file_name: str
        """
        if not isinstance(url, str):
            raise TypeError('url should be a string.')
        elif not isinstance(file_name, str):
            raise TypeError('file_name should be a string.')

        import requests

        try:
            response = requests.get(url)
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

        if not isinstance(file, str):
            raise TypeError('file should be a string.')

        import requests

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
        if not isinstance(value, str):
            raise TypeError('value should be a string.')

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
        if not isinstance(folder_path, str):
            raise TypeError('folder_path should be a string.')
        elif not isinstance(required, int):
            raise TypeError('required should be an integer.')

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
        if not isinstance(value, str):
            raise TypeError('value should be a string.')

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
        if not isinstance(length, int):
            raise TypeError('length should be an integer.')

        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))


class M3U8DownloaderError(RuntimeError):
    """
    An exception raised by the M3U8Downloader class or its methods.

    This exception is used to indicate errors that occur during the operation
    of the M3U8Downloader class or its methods.
    """

    def __init__(self, message: str) -> None:
        """
        Initialize a new instance of M3U8DownloaderError.

        :param message: A human-readable error message describing the exception
        :type message: str
        """
        if not isinstance(message, str):
            raise TypeError('message should be a string.')

        self.message = message
        super().__init__(self.message)


class M3U8Downloader:
    """
    A class for downloading and concatenating video files from M3U8 playlists.

    This class provides functionality to download video files from M3U8 playlists,
    concatenate them into a single video file, and handle various error conditions.
    """

    _debug = False
    _debug_file_path = None
    _debug_logger = None
    _input_file_path = None
    _output_file_path = None
    _skip_space_check = False
    _download_complete = False
    _cancelled = False

    def __init__(
            self,
            input_file_path: str,
            output_file_path: str,
            skip_space_check: Optional[bool] = False,
            debug: Optional[bool] = False,
            debug_file_path: Optional[str] = 'debug.log'
    ) -> None:
        """
        Initializes the M3U8Downloader object with the specified parameters.

        :param input_file_path: The path to the input M3U8 playlist file.
        :type input_file_path: str
        :param output_file_path: The path to the output video file.
        :type output_file_path: str
        :param skip_space_check: A flag indicating whether to skip disk space checking. Defaults to False.
        :type skip_space_check: bool
        :param debug: A flag indicating whether debug mode is enabled. Defaults to False.
        :type debug: bool
        :param debug_file_path: The file path for storing debug logs. Defaults to 'debug.log'.
        :type debug_file_path: str
        """
        if not isinstance(input_file_path, str):
            raise TypeError('input_file_path should be a string.')
        elif not isinstance(output_file_path, str):
            raise TypeError('output_file_path should be a string.')
        elif not isinstance(skip_space_check, bool):
            raise TypeError('skip_space_check should be a boolean.')
        elif not isinstance(debug, bool):
            raise TypeError('debug should be a boolean.')
        elif not isinstance(debug_file_path, str):
            raise TypeError('debug_file_path should be a string.')

        self._debug = debug
        self._debug_file_path = debug_file_path
        self._configure_debug_logger()
        self._input_file_path = input_file_path
        self._debug_logger.debug(f'Input File Path: {self._input_file_path}') if self._debug else None
        self._output_file_path = (
            output_file_path if output_file_path.endswith('.mp4') else f'{output_file_path}.mp4'
        )
        self._debug_logger.debug(f'Output File Path: {self._output_file_path}') if self._debug else None
        self._skip_space_check = skip_space_check
        self._debug_logger.debug(f'Skip Space Check: {self._skip_space_check}') if self._debug else None
        self._index_file_name = ''
        self._parent_url = ''
        self._playlist_files = []

    @property
    def input_file_path(self) -> str:
        """
        Getter property for the input file path.

        :return: The input file path.
        :rtype: str
        """
        return self._input_file_path

    @input_file_path.setter
    def input_file_path(self, value: str) -> None:
        """
        Setter property for the input file path.

        :param value: The new input file path.
        :type value: str
        """
        if not isinstance(value, str):
            raise TypeError('input_file_path should be a string.')

        self._input_file_path = value
        self._debug_logger.debug(f'Input File Path: {self._input_file_path}') if self._debug else None

    @property
    def output_file_path(self) -> str:
        """
        Getter property for the output file path.

        :return: The output file path.
        :rtype: str
        """
        return self._output_file_path

    @output_file_path.setter
    def output_file_path(self, value: str) -> None:
        """
        Setter property for the output file path.

        :param value: The new output file path.
        :type value: str
        """
        if not isinstance(value, str):
            raise TypeError('output_file_path should be a string.')

        self._output_file_path = (
            value if value.endswith('.mp4') else f'{value}.mp4'
        )
        self._debug_logger.debug(f'Output File Path: {self._output_file_path}') if self._debug else None

    @property
    def skip_space_check(self) -> bool:
        """
        Getter property for the skip space check flag.

        :return: The skip space check flag.
        :rtype: bool
        """
        return self._skip_space_check

    @skip_space_check.setter
    def skip_space_check(self, value: bool) -> None:
        """
        Setter property for the skip space check flag.

        :param value: The new value for the skip space check flag.
        :type value: bool
        """
        if not isinstance(value, bool):
            raise TypeError('skip_space_check should be a boolean.')

        self._skip_space_check = value
        self._debug_logger.debug(f'Skip Space Check: {self._skip_space_check}') if self._debug else None

    @property
    def debug(self) -> bool:
        """
        Getter property for the debug flag.

        :return: The debug flag.
        :rtype: bool
        """
        return self._debug

    @debug.setter
    def debug(self, value: bool) -> None:
        """
        Setter property for the debug flag.

        :param value: The new value for the debug flag.
        :type value: bool
        """
        if not isinstance(value, bool):
            raise TypeError('debug should be a boolean.')

        self._debug = value

    @property
    def debug_file_path(self) -> str:
        """
        Getter property for the debug file path.

        :return: The debug file path.
        :rtype: str
        """
        return self._debug_file_path

    @debug_file_path.setter
    def debug_file_path(self, value: str) -> None:
        """
        Setter property for the debug file path.

        :param value: The new value for debug file path.
        :type value: str
        """
        if not isinstance(value, str):
            raise TypeError('debug_file_path should be a string.')

        self._debug_file_path = value

    @property
    def is_download_complete(self) -> bool:
        """
        Getter property for the download completion status.

        :return: True if the download is complete, False otherwise.
        :rtype: bool
        """
        return self._download_complete

    def _check_required_disk_space(self, space_required: int) -> None:
        """
        Checks if the required disk space is available for downloading the playlist.

        :param space_required: The amount of disk space required in bytes.
        :type space_required: int
        """
        if not isinstance(space_required, int):
            raise TypeError('space_required should be an integer.')

        if UtilityClass.are_paths_on_same_disk(self._temp_directory_path, self._output_file_path):
            if not UtilityClass.is_space_available(self._temp_directory_path, 2 * space_required):
                raise OSError(
                    f'Path "{self._output_file_path}" is low on storage. Required: {2 * space_required} bytes.'
                )
        else:
            if not UtilityClass.is_space_available(self._temp_directory_path, space_required):
                raise OSError(
                    f'Path "{self._temp_directory_path}" is low on storage. Required: {space_required} bytes.'
                )

            if not UtilityClass.is_space_available(self._output_file_path, space_required):
                raise OSError(
                    f'Path "{self._output_file_path}" is low on storage. Required: {space_required} bytes.'
                )

    def _concatenate_video_files(self) -> None:
        """
        Concatenates the downloaded video files into a single video file.
        """
        self._debug_logger.debug('Build started') if self._debug else None
        total_files = len(self._playlist_files)
        completed_files = 0
        playlist_file_path = os.path.join(self._temp_directory_path, 'playlist_files')

        i = 0
        with open(self._output_file_path, 'wb') as output_file:
            with open(playlist_file_path, 'r') as playlist_files:
                for file_line in playlist_files:
                    file_line = file_line.strip().replace('file ', '')
                    file_path = os.path.join(self._temp_directory_path, file_line)
                    with open(file_path, 'rb') as input_file:
                        output_file.write(input_file.read())

                    i += 1
                    completed_files_now = i
                    if completed_files_now > completed_files:
                        completed_files = completed_files_now
                        percentage = completed_files * 100 // total_files
                        progress_bar = "#" * (percentage // 2)
                        sys.stdout.write(f"\rBuild   : [{progress_bar:<50}] {percentage}%")
                        sys.stdout.flush()

                    self._debug_logger.debug(f'Merged {file_path}') if self._debug else None

                    time.sleep(0.1)

                sys.stdout.write("\n")

    def _configure_debug_logger(self) -> None:
        """
        Configures the logger for debugging purposes.
        """
        import pyloggermanager

        if self._debug:
            format_string = (
                '%(time)s :: %(logger_name)s :: %(level_name)s :: %(file_name)s :: %(class_name)s'
                ' :: %(function_name)s :: %(thread_name)s :: %(message)s'
            )
            formatter = pyloggermanager.formatters.DefaultFormatter(format_str=format_string)
            handler = pyloggermanager.handlers.FileHandler(
                file_name=self._debug_file_path,
                level=pyloggermanager.LogLevel.DEBUG,
                formatter=formatter
            )
            self._debug_logger = pyloggermanager.Logger(name='debug_logger', level=pyloggermanager.LogLevel.DEBUG)
            self._debug_logger.add_handler(handler)

    def _create_temp_directory(self) -> None:
        """
        Creates a temporary directory for storing downloaded files.
        """
        self._index_file_name = ''
        self._parent_url = ''
        self._temp_directory = UtilityClass.random_string()
        self._debug_logger.debug(f'Temporary Directory Name: {self._temp_directory}') if self._debug else None
        self._temp_directory_path = os.path.join(tempfile.gettempdir(), self._temp_directory)
        self._debug_logger.debug(f'Temporary Directory Full Path: {self._temp_directory_path}') if self._debug else None
        self._playlist_files = []

        self._debug_logger.debug('Creating temporary directory') if self._debug else None
        os.makedirs(self._temp_directory_path, exist_ok=True)

    def _download_and_write(self, sequence: int, url: str, files: TextIO) -> None:
        """
        Downloads and writes a video file to disk.

        :param sequence: The sequence number of the video file.
        :type sequence: int
        :param url: The URL of the video file.
        :type url: str
        :param files: The file object for writing playlist files.
        :type files: TextIO
        """
        if not isinstance(sequence, int):
            raise TypeError('sequence should be an integer.')
        elif not isinstance(url, str):
            raise TypeError('url should be an integer.')

        import requests

        try:
            file_name = f'file{sequence}.mp4'
            files.write(f'file {file_name}\n')
            file_path = os.path.join(self._temp_directory_path, file_name)
            self._debug_logger.debug(f'Download File Path: {file_path}') if self._debug else None
            UtilityClass.download_file(url, file_path)
            self._debug_logger.debug(f'{file_path} downloaded') if self._debug else None
        except requests.RequestException as e:
            self._debug_logger.debug(f'Download error. {e}') if self._debug else None
            raise e

    def _download_files_with_progress(self):
        """
        Downloads the video files from the playlist with progress indication.
        """
        self._debug_logger.debug('Download started') if self._debug else None
        total_files = len(self._playlist_files)
        completed_files = 0

        with open(os.path.join(self._temp_directory_path, 'playlist_files'), 'w') as files:
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = []
                for counter, url in enumerate(self._playlist_files, start=1):
                    future = executor.submit(self._download_and_write, counter, url, files)
                    futures.append(future)

                while True:
                    completed_files_now = sum(future.done() for future in futures)
                    if completed_files_now > completed_files:
                        completed_files = completed_files_now
                        percentage = completed_files * 100 // total_files
                        progress_bar = "#" * (percentage // 2)
                        sys.stdout.write(f"\rDownload: [{progress_bar:<50}] {percentage}%")
                        sys.stdout.flush()

                    if all(future.done() for future in futures):
                        break
                    time.sleep(0.1)

                sys.stdout.write("\n")

    def _download_index_file(self) -> bool:
        """
        Downloads the index file of the M3U8 playlist.

        :return: True if the download is successful, False otherwise.
        :rtype: bool
        """
        import requests

        try:
            index_file_path = os.path.join(self._temp_directory_path, 'index.m3u8')
            self._debug_logger.debug(f'Index File Path: {index_file_path}') if self._debug else None
            UtilityClass.download_file(self._input_file_path, index_file_path)
            self._debug_logger.debug('Index file downloaded') if self._debug else None
            return True
        except requests.RequestException as e:
            self._debug_logger.debug(f'Index file download failed. {e}') if self._debug else None
            return False

    def _get_index_file_name(self) -> str:
        """
        Extracts the name of the index file from the input file path.

        :return: The name of the index file.
        :rtype: str
        """
        url_parts = self._input_file_path.split('/')
        return url_parts[-1]

    def _get_parent_url(self) -> str:
        """
        Extracts the parent URL from the input file path.

        :return: The parent URL.
        :rtype: str
        """
        url_parts = self._input_file_path.split('/')
        return '/'.join(url_parts[:-1])

    def _get_playlist_files(self) -> list[str]:
        """
        Retrieves the list of video files from the playlist.

        :return: The list of video file URLs.
        :rtype: list[str]
        """
        self._debug_logger.debug('Gathering playlist from input file') if self._debug else None
        playlist_files: list[str] = []
        with open(os.path.join(self._temp_directory_path, 'index.m3u8'), 'r') as index_file:
            for line in index_file:
                line = line.strip()
                if line and not line.startswith('#'):
                    file_path = (
                        f'{self._parent_url}/{line}'
                        if self._parent_url and not line.startswith(('http://', 'https://'))
                        else line
                    )
                    self._debug_logger.debug(f'Playlist File: {file_path}') if self._debug else None
                    playlist_files.append(file_path)

        return playlist_files

    def _get_playlist_size(self) -> int:
        """
        Computes the total size of the playlist files.

        :return: The total size of the playlist files in bytes.
        :rtype: int
        """
        self._debug_logger.debug('Verify started') if self._debug else None
        total_files = len(self._playlist_files)
        completed_files = 0

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for counter, file in enumerate(self._playlist_files, start=1):
                future = executor.submit(UtilityClass.get_content_length, file)
                futures.append(future)

            while True:
                completed_files_now = sum(future.done() for future in futures)
                if completed_files_now > completed_files:
                    completed_files = completed_files_now
                    percentage = completed_files * 100 // total_files
                    progress_bar = "#" * (percentage // 2)
                    sys.stdout.write(f"\rVerify  : [{progress_bar:<50}] {percentage}%")
                    sys.stdout.flush()

                if all(future.done() for future in futures):
                    break
                time.sleep(0.1)

            sys.stdout.write("\n")
            total_size = sum(future.result() for future in futures)

        return total_size

    def _is_master_file(self) -> bool:
        """
        Checks if the input file is a master playlist.

        :return: True if the input file is a master playlist, False otherwise.
        :rtype: bool
        """
        is_master = False
        self._debug_logger.debug('Verifying if input file is master') if self._debug else None
        with open(os.path.join(self._temp_directory_path, 'index.m3u8'), 'r') as index_file:
            for line in index_file:
                if line.startswith('#EXT-X-STREAM-INF'):
                    is_master = True
                    self._debug_logger.debug(f'Identified input file as master. {line}') if self._debug else None
                    break

        return is_master

    def _remove_temp_directory(self) -> None:
        """
        Removes the temporary directory used for storing downloaded files.
        """
        self._debug_logger.debug('Cleaning temporary directory') if self._debug else None
        shutil.rmtree(self._temp_directory_path)

    def _validate(self) -> None:
        """
        Validates the input parameters and conditions before starting the download process.
        """
        if not UtilityClass.is_url(self._input_file_path):
            raise ValueError('input_file_path is not a valid url.')
        elif not UtilityClass.is_m3u8_url(self._input_file_path):
            raise ValueError('input_file_path is not a valid m3u8 url.')
        elif not UtilityClass.is_internet_connected():
            raise M3U8DownloaderError('Internet connection required.')

    def download_playlist(self) -> None:
        """
        Downloads and concatenates the video files from the M3U8 playlist.
        """
        try:
            self._create_temp_directory()
            self._download_complete = False
            self._validate()
            self._index_file_name = self._get_index_file_name()
            self._debug_logger.debug(f'Index File Name: {self._index_file_name}') if self._debug else None
            self._parent_url = self._get_parent_url()
            self._debug_logger.debug(f'Parent URL: {self._parent_url}') if self._debug else None

            if not self._download_index_file():
                raise M3U8DownloaderError(
                    message=f'Unable to download "{self._index_file_name}" file.'
                )

            if self._is_master_file():
                raise M3U8DownloaderError(
                    message=f'File "{self._input_file_path}" is identified as master. '
                            f'Currently, this package does not support downloading master playlist.'
                )

            self._playlist_files = self._get_playlist_files()

            if not self._skip_space_check:
                self._debug_logger.debug('Verifying if required space '
                                         'is available for download') if self._debug else None
                playlist_size = self._get_playlist_size()
                self._debug_logger.debug(f'Required space: {playlist_size}') if self._debug else None
                self._check_required_disk_space(playlist_size)
                self._debug_logger.debug('Required space is available') if self._debug else None
            else:
                self._debug_logger.debug('Verification of space required skipped') if self._debug else None

            self._download_files_with_progress()
            self._concatenate_video_files()
            self._download_complete = True
        finally:
            self._remove_temp_directory()
