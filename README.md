# `pym3u8downloader`

M3U8 Downloader is a Python class designed to download and concatenate video files from M3U8 playlists, including master
playlists. This class offers comprehensive functionality for managing M3U8 playlist files, downloading video segments,
optionally combining them into a single video file, and handling various error conditions.

## Installation

M3U8Downloader can be installed using pip:

```bash
pip install pym3u8downloader
```

## Usage

````python
from pym3u8downloader import M3U8Downloader

# Initialize the downloader
downloader = M3U8Downloader(
    input_file_path="http://example.com/video.m3u8",
    output_file_path="output_video"
)

# Download and concatenate the playlist
downloader.download_playlist()

# Download and concatenate the master playlist
downloader.download_master_playlist(name='720')

# Output
# Verify  : [##################################################] 100%
# Download: [##################################################] 100%
# Build   : [##################################################] 100%
````

# Documentation

## `pym3u8downloader`

### `M3U8Downloader`

#### Constructors

- `M3U8Downloader(input_file_path: str, output_file_path: str, skip_space_check: Optional[bool] = False, debug: Optional[bool] = False, debug_file_path: Optional[str] = 'debug.log', max_threads: Optional[int] = 10)`:
  Initializes the M3U8Downloader object with the specified parameters.

#### Methods

- `download_playlist(merge: bool = True)`: Downloads video files from an M3U8 playlist. The optional `merge`
  parameter determines the handling of the downloaded segments. When `merge` is set to `True`, the method downloads and
  concatenates all video segments into a single output file. If `merge` is `False`, it only downloads the segments
  without concatenating them, keeping each segment as an individual file.
- `download_master_playlist(name: Optional[str] = None, bandwidth: Optional[str] = None, resolution: Optional[str] = None, merge: bool = True)`:
  Downloads video files from an M3U8 master playlist, with the specific variant selected based on optional parameters
  such as `name`, `bandwidth`, and `resolution`. The optional `merge` parameter determines the handling of the
  downloaded segments. When `merge` is set to `True`, the method downloads and concatenates all video segments into a
  single output file. If `merge` is `False`, it only downloads the segments without concatenating them, keeping each
  segment as an individual file.

#### Properties

- `input_file_path`: Getter/setter property for the input file path.
- `output_file_path`: Getter/setter property for the output file path.
- `skip_space_check`: Getter/setter property for the skip space check flag.
- `debug`: Getter/setter property for the debug flag.
- `debug_file_path`: Getter/setter property for the debug file path.
- `max_threads`: Getter/setter property for the maximum number of threads that can be executed in parallel.
- `is_download_complete`: Getter property for the download completion status.

### `M3U8DownloaderError`

This error class is employed to signal any issues or errors encountered during the execution of M3U8Downloader methods.

#### Constructors

- `M3U8DownloaderError(message: str)`: Initialize a M3U8DownloaderError.

# Troubleshooting Guide

For detailed troubleshooting guide, please refer to [TROUBLESHOOTING](TROUBLESHOOTING.md).

# License

Please refer to the [MIT License](LICENSE) within the project for more information.

# Contributing

We welcome contributions from the community! Whether you have ideas for new features, bug fixes, or enhancements, feel
free to open an issue or submit a pull request on [GitHub](https://github.com/coldsofttech/pym3u8downloader).