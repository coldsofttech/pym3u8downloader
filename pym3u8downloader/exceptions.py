from typing import Optional, Union

from pym3u8downloader.validations import validate_type


class M3U8DownloaderError(RuntimeError):
    """
    An exception raised by the M3U8Downloader class or its methods.

    This exception is used to indicate errors that occur during the operation
    of the M3U8Downloader class or its methods.
    """

    def __init__(self, message: str) -> None:
        """
        Initialize a new instance of M3U8DownloaderError.

        :param message: A human-readable error message describing the exception.
        :type message: str
        """
        validate_type(message, str, 'message should be a string.')
        self.message = message
        super().__init__(self.message)


class M3U8DownloaderWarning(Warning):
    """
    A warning raised by the M3U8Downloader class or its methods.

    This warning is used to indicate an issue with master playlist resolution that occurs during the operation of the
    M3U8Downloader class or its methods.
    """

    def __init__(self, message: str, json_data: Optional[list] = None) -> None:
        """
        Initialize a new instance of M3U8DownloaderWarning.

        :param message: A human-readable warning message describing the issue.
        :type message: str
        :param json_data: The JSON-formatted data of all available resolutions from master playlist to choose from.
        :type json_data: list
        """
        validate_type(message, str, 'message should be a string.')
        validate_type(json_data, Union[list, None], 'json_data should be a list.')
        self.message = message
        self.json_data = json_data
        super().__init__(self.message)
