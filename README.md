# `pym3u8downloader`

M3U8 Downloader is a Python class designed to download and concatenate video files from M3U8 playlists. This class
provides functionality to handle M3U8 playlist files, download video segments, concatenate them into a single video
file, and manage various error conditions.

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

# Output
# Verify  : [##################################################] 100%
# Download: [##################################################] 100%
# Build   : [##################################################] 100%
````

# Documentation

## `pym3u8downloader`

### `M3U8Downloader`

#### Properties

- `input_file_path`: Getter/setter property for the input file path.
- `output_file_path`: Getter/setter property for the output file path.
- `skip_space_check`: Getter/setter property for the skip space check flag.
- `debug`: Getter/setter property for the debug flag.
- `debug_file_path`: Getter/setter property for the debug file path.
- `max_threads`: Getter/setter property for the maximum number of threads that can be executed in parallel.
- `is_download_complete`: Getter property for the download completion status.

#### Methods

- `__init__(input_file_path: str, output_file_path: str, skip_space_check: Optional[bool] = False, debug: Optional[bool] = False, debug_file_path: Optional[str] = 'debug.log', max_threads: Optional[int] = 10)`:
  Initializes the M3U8Downloader object with the specified parameters.
- `download_playlist(merge: bool = True)`: Downloads video files from an M3U8 playlist. The optional `merge`
  parameter determines the handling of the downloaded segments. When `merge` is set to `True`, the method downloads and
  concatenates all video segments into a single output file. If `merge` is `False`, it only downloads the segments
  without concatenating them, keeping each segment as an individual file.

### `M3U8DownloaderError`

This error class is employed to signal any issues or errors encountered during the execution of M3U8Downloader methods.

#### Methods

- `__init__(message: str)`: Initialize a ConfigurationManagerError

# Limitations

This package currently only supports M3U8 playlists and does not support master playlists.