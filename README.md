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
- `is_download_complete`: Getter property for the download completion status.

#### Methods

- `__init__(input_file_path: str, output_file_path: str, skip_space_check: Optional[bool] = False, debug: Optional[bool] = False, debug_file_path: Optional[str] = 'debug.log')`:
  Initializes the M3U8Downloader object with the specified parameters.
- `download_playlist()`: Downloads and concatenates the video files from the M3U8 playlist.

### `M3U8DownloaderError`

This error class is employed to signal any issues or errors encountered during the execution of M3U8Downloader methods.

#### Methods

- `__init__(message: str)`: Initialize a ConfigurationManagerError

# Limitations

This package currently only supports M3U8 playlists and does not support master playlists.