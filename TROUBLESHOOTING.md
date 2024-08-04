# Troubleshooting

This document provides comprehensive guidance on troubleshooting issues related to the package.

## Internet Errors

**Error Message:**

```html
pym3u8downloader.__main__.M3U8DownloaderError: Internet connection required.
```

**Description:**

This error indicates that an internet connection is not available. The functionality of this package relies on a stable
online connection to operate correctly.

**Solution:**

To resolve this issue, ensure that you are connected to the internet and then re-run the script.

## Download Playlist Errors

**Error Message:**

```html
pym3u8downloader.__main__.M3U8DownloaderError: Identified file "***" as master playlist. Please use "download_master_playlist" instead.
```

**Description:**

This error occurs when attempting to download video segments from a master playlist using the `download_playlist`
method. This method is intended for downloading video segments directly from a regular playlist, not a master playlist.

**Solution:**

To download video segments from a master playlist, use the `download_master_playlist` method instead. This method is
specifically designed to handle master playlists. Below is an example demonstrating how to use it:

**Example:**

```python
from pym3u8downloader import M3U8Downloader

downloader = M3U8Downloader(
    input_file_path='https://example.com/master.m3u8',
    output_file_path='output_video.mp4'
)
downloader.download_master_playlist(name='720', bandwidth='2048', resolution='1280x720')  # Replace appropriate values
```

**Error Message:**

```html
pym3u8downloader.__main__.M3U8DownloaderError: Identified file "***" as playlist. Please use "download_playlist" instead.
```

**Description:**

This error occurs when attempting to download video segments from a regular playlist using
the `download_master_playlist` method. This method is intended for downloading video segments directly from a master
playlist, not a regular playlist.

**Solution:**
To download video segments from a regular playlist, use the `download_playlist` method instead. This method is
specifically designed to handle regular playlists. Below is an example demonstrating how to use it:

**Example:**

```python
from pym3u8downloader import M3U8Downloader

downloader = M3U8Downloader(
    input_file_path='https://example.com/index.m3u8',
    output_file_path='output_video.mp4'
)
downloader.download_playlist()
```

**Error Message:**

```html
pym3u8downloader.__main__.M3U8DownloaderError: File "***" is not identified as either playlist or master.
```

**Description:**

This error occurs when attempting to download video segments using either the `download_playlist` method or
the `download_master_playlist` method, and the provided file is not recognized as a valid M3U8 playlist or master
playlist. This typically happens if the input .m3u8 link is either incorrectly formatted or not an M3U8 file.

**Solution:**

Verify that the .m3u8 file is correctly formatted and appropriate for the method being used. If you received the .m3u8
file link from someone else, contact them to ensure that they provide the correct link.

**Error Message:**

```html
pym3u8downloader.__main__.M3U8DownloaderError: Unable to download "***" file.
```

**Description:**

This error occurs when the `download_playlist` or `download_master_playlist` method fails to download the specified
.m3u8 file. This issue may arise due to an unstable internet connection or if the file is not available at the provided
URL.

**Solution:**

Ensure that the file exists at the specified URL and that you have a stable internet connection. Verify the link and
check that the file is accessible. Reattempt the download once these conditions are met.

**Error Message:**

```html
UserWarning: Identified * variants in the master playlist. To download the desired playlist, please provide additional parameters, such as NAME, BANDWIDTH, or RESOLUTION, to identify the specific variant.
For example: use "download_master_playlist(name='720', bandwidth='2149280', resolution='1280x720')".

You can view the available options using the following list:
[
{'bandwidth': '***', 'name': '***', 'resolution': '***'},
...
]
```

**Description:**

This warning is issued when attempting to use the `download_master_playlist` method without specifying the necessary
parameters (name, bandwidth, or resolution) to select a specific variant. When these parameters are not provided, the
package analyzes the master playlist and lists all available variants to assist you in choosing the correct one.

**Solution:**

Review the list of available variants provided in the warning message. Choose the appropriate values for name,
bandwidth, and resolution, and then provide these parameters to download the desired video segments.

**Error Message:**

```html
pym3u8downloader.__main__.M3U8DownloaderError: Selected variant, name="***", bandwidth="***", resolution="***" not found.
```

**Description:**

This error occurs when the specified parameters (name, bandwidth, or resolution) for the `download_master_playlist`
method do not match any of the variants listed in the master playlist.

**Solution:**

Verify that the details for the variant (name, bandwidth, and resolution) are accurate and match one of the available
options in the master playlist. If you are unsure of the available variants, remove the parameters to receive
a `UserWarning` that will provide a list of all available variants from which you can choose.