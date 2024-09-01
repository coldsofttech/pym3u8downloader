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

        :param message: A human-readable error message describing the exception
        :type message: str
        """
        validate_type(message, str, 'message should be a string.')
        self.message = message
        super().__init__(self.message)
