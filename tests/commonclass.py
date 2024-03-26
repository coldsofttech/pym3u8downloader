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
import platform
import random
import string


class CommonClass:
    """Utility class for unit tests"""
    override_branch_name = 'main'  # Update this when running tests locally

    @staticmethod
    def get_branch_name():
        """Returns the Git branch name"""
        return os.environ.get('BRANCH_NAME', 'main')

    @staticmethod
    def get_git_test_parent_url():
        """Returns the parent url of the test files"""
        branch_name = (
            CommonClass.override_branch_name
            if CommonClass.override_branch_name.strip() != '' else CommonClass.get_branch_name()
        )
        return (
            f'https://raw.githubusercontent.com/coldsofttech/pym3u8downloader/{branch_name}/tests/files'
        )

    @staticmethod
    def generate_name(extension: str, length: int = 10) -> str:
        """Generates file name based on the extension provided"""
        letters = string.ascii_lowercase
        file_name = ''.join(random.choice(letters) for _ in range(length))
        return f'{file_name}.{extension}'

    @staticmethod
    def get_available_disks():
        """Returns all the available disks"""
        system = platform.system().lower()
        if system == 'windows':
            return [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
        elif system == 'linux':
            return ['/']
        else:
            return []

    @staticmethod
    def generate_sample_file_paths(same_disk: bool = True, extension: str = 'html'):
        """Returns sample source and destination paths based on the provided same_disk value"""
        source_dir = os.getcwd()
        dest_dir = os.path.join(os.path.expanduser('~'), 'Documents')
        source_file_path = os.path.join(source_dir, CommonClass.generate_name(extension))
        available_disks = CommonClass.get_available_disks()

        if not available_disks:
            raise RuntimeError('No available disks found.')

        if same_disk:
            dest_disk = available_disks[0]
        else:
            if len(available_disks) > 1:
                dest_disk = available_disks[1]
            else:
                raise RuntimeError('Insufficient disks available for different disk option.')

        dest_file_path = os.path.join(dest_disk, dest_dir, CommonClass.generate_name('.mp4'))

        return source_file_path, dest_file_path

    @staticmethod
    def generate_sample_index_m3u8_file(file_name: str):
        """Creates a sample index.m3u8 file"""
        content = """
        #EXTM3U
        #EXT-X-VERSION:3
        #EXT-X-TARGETDURATION:10
        #EXT-X-MEDIA-SEQUENCE:0
        #EXTINF:10.000,
        sample_segment_0.ts
        #EXTINF:10.000,
        sample_segment_1.ts
        #EXTINF:10.000,
        sample_segment_2.ts
        #EXT-X-ENDLIST
        """
        with open(file_name, 'w') as file:
            file.write(content)

    @staticmethod
    def generate_sample_master_m3u8_file(file_name: str):
        """Creates a sample master.m3u8 file"""
        content = """
        #EXTM3U
        #EXT-X-STREAM-INF:BANDWIDTH=1280000,RESOLUTION=960x540,CODECS="avc1.42c00d,mp4a.40.2"
        variant_1.m3u8
        #EXT-X-STREAM-INF:BANDWIDTH=2560000,RESOLUTION=1280x720,CODECS="avc1.4d401f,mp4a.40.2"
        variant_2.m3u8
        #EXT-X-STREAM-INF:BANDWIDTH=7680000,RESOLUTION=1920x1080,CODECS="avc1.640028,mp4a.40.2"
        variant_3.m3u8
        """
        with open(file_name, 'w') as file:
            file.write(content)
