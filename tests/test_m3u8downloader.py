import io
import os
import sys
import tempfile
import unittest

from commonclass import CommonClass
from pym3u8downloader import M3U8Downloader, M3U8DownloaderError


class TestM3U8Downloader(unittest.TestCase):
    """Unit test cases for M3U8Downloader"""

    def setUp(self) -> None:
        self.input_file_path = f'{CommonClass.get_git_test_parent_url()}/sample_index.m3u8'
        self.input_file_path_updated = f'{CommonClass.get_git_test_parent_url()}/sample_master.m3u8'
        self.output_file_path = CommonClass.generate_sample_file_paths(True, None)[0]
        self.output_file_path_updated = CommonClass.generate_sample_file_paths(True, None)[0]
        self.output_file_path_with_mp4 = CommonClass.generate_sample_file_paths(True, 'mp4')[0]
        self.debug_file_path = CommonClass.generate_sample_file_paths(True, 'log')[0]
        self.debug_file_path_updated = CommonClass.generate_sample_file_paths(True, 'log')[0]
        self.max_threads = 10
        self.max_threads_updated = 20

    def tearDown(self) -> None:
        files = [
            self.output_file_path,
            self.output_file_path_updated,
            self.output_file_path_with_mp4,
            self.debug_file_path,
            self.debug_file_path_updated,
            'video_0.ts.mp4',
            'video_1.ts.mp4',
            'video_2.ts.mp4'
        ]

        for file in files:
            try:
                os.remove(file)
            except (PermissionError, FileNotFoundError, IsADirectoryError):
                pass

    def test_init_invalid_input_file_path(self):
        """Test if init raises TypeError"""
        with self.assertRaises(TypeError):
            M3U8Downloader(100, self.output_file_path)

    def test_init_invalid_output_file_path(self):
        """Test if init raises TypeError"""
        with self.assertRaises(TypeError):
            M3U8Downloader(self.input_file_path, 100)

    def test_init_invalid_skip_space_check(self):
        """Test if init raises TypeError"""
        with self.assertRaises(TypeError):
            M3U8Downloader(self.input_file_path, self.output_file_path, 100)

    def test_init_invalid_debug(self):
        """Test if init raises TypeError"""
        with self.assertRaises(TypeError):
            M3U8Downloader(self.input_file_path, self.output_file_path, False, 100)

    def test_init_invalid_debug_file_path(self):
        """Test if init raises TypeError"""
        with self.assertRaises(TypeError):
            M3U8Downloader(self.input_file_path, self.output_file_path, False, True, 100)

    def test_init_invalid_max_threads(self):
        """Test if init raises TypeError"""
        with self.assertRaises(TypeError):
            M3U8Downloader(self.input_file_path, self.output_file_path, max_threads='100')

    def test_init_valid_params(self):
        """Test if init works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        self.assertEqual(self.input_file_path, downloader.input_file_path)
        self.assertEqual(self.output_file_path, downloader.output_file_path)
        self.assertFalse(downloader.skip_space_check)
        self.assertEqual(self.max_threads, downloader.max_threads)

    def test_init_valid_params_skip_and_debug(self):
        """Test if init works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path, True, True, self.debug_file_path)
        self.assertEqual(self.input_file_path, downloader.input_file_path)
        self.assertEqual(self.output_file_path, downloader.output_file_path)
        self.assertTrue(downloader.skip_space_check)
        self.assertTrue(downloader.debug)
        self.assertEqual(self.debug_file_path, downloader.debug_file_path)
        self.assertEqual(self.max_threads, downloader.max_threads)

    def test_init_valid_params_max_threads(self):
        """Test if init works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path, max_threads=self.max_threads_updated)
        self.assertEqual(self.input_file_path, downloader.input_file_path)
        self.assertEqual(self.output_file_path, downloader.output_file_path)
        self.assertFalse(downloader.skip_space_check)
        self.assertEqual(self.max_threads_updated, downloader.max_threads)

    def test_input_file_path_property_valid_get(self):
        """Test if input file path property works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        self.assertEqual(self.input_file_path, downloader.input_file_path)

    def test_input_file_path_property_valid_set(self):
        """Test if input file path property works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        downloader.input_file_path = self.input_file_path_updated
        self.assertEqual(self.input_file_path_updated, downloader.input_file_path)

    def test_input_file_path_property_invalid_set(self):
        """Test if input file path property raises TypeError"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        with self.assertRaises(TypeError):
            downloader.input_file_path = 100

    def test_output_file_path_property_valid_get(self):
        """Test if output file path property works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        self.assertEqual(self.output_file_path, downloader.output_file_path)

    def test_output_file_path_property_valid_set_no_mp4(self):
        """Test if output file path property works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        downloader.output_file_path = self.output_file_path_updated
        self.assertEqual(f'{self.output_file_path_updated}.mp4', downloader.output_file_path)

    def test_output_file_path_property_valid_set_with_mp4(self):
        """Test if output file path property works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        downloader.output_file_path = self.output_file_path_with_mp4
        self.assertEqual(self.output_file_path_with_mp4, downloader.output_file_path)

    def test_output_file_path_property_invalid_set(self):
        """Test if output file path property raises TypeError"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        with self.assertRaises(TypeError):
            downloader.output_file_path = 100

    def test_skip_space_check_valid_get(self):
        """Test if skip space check works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        self.assertFalse(downloader.skip_space_check)

    def test_skip_space_check_valid_set(self):
        """Test if skip space check works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        downloader.skip_space_check = True
        self.assertTrue(downloader.skip_space_check)

    def test_skip_space_check_invalid_set(self):
        """Test if skip space check raises TypeError"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        with self.assertRaises(TypeError):
            downloader.skip_space_check = 100

    def test_debug_valid_get(self):
        """Test if debug works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        self.assertFalse(downloader.debug)

    def test_debug_valid_set(self):
        """Test if debug works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        downloader.debug = True
        self.assertTrue(downloader.debug)

    def test_debug_invalid_set(self):
        """Test if debug raises TypeError"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        with self.assertRaises(TypeError):
            downloader.debug = 100

    def test_debug_file_path_valid_get(self):
        """Test if debug file path works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path, False, True, self.debug_file_path)
        self.assertEqual(self.debug_file_path, downloader.debug_file_path)

    def test_debug_file_path_valid_set(self):
        """Test if debug file path works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path, False, True, self.debug_file_path)
        downloader.debug_file_path = self.debug_file_path_updated
        self.assertEqual(self.debug_file_path_updated, downloader.debug_file_path)

    def test_debug_file_path_invalid_set(self):
        """Test if debug file path raises TypeError"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path, False, True, self.debug_file_path)
        with self.assertRaises(TypeError):
            downloader.debug_file_path = 100

    def test_max_threads_valid_get(self):
        """Test if max threads works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path, max_threads=self.max_threads_updated)
        self.assertEqual(self.max_threads_updated, downloader.max_threads)

    def test_max_threads_valid_set(self):
        """Test if max threads works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        downloader.max_threads = self.max_threads_updated
        self.assertEqual(self.max_threads_updated, downloader.max_threads)

    def test_max_threads_invalid_set(self):
        """Test if max threads raises TypeError"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        with self.assertRaises(TypeError):
            downloader.max_threads = '100'

    def test__check_required_disk_space_invalid_space_required(self):
        """Test if check required disk space raises TypeError"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        downloader._create_temp_directory()
        with self.assertRaises(TypeError):
            downloader._check_required_disk_space('10GB')
        downloader._remove_temp_directory()

    def test__check_required_disk_space_valid_same_disk_available(self):
        """Test if check required disk space works as expected"""
        path1, path2 = CommonClass.generate_sample_file_paths(True, 'mp4')
        downloader = M3U8Downloader(self.input_file_path, path1)
        downloader._create_temp_directory()
        space_required = 10
        try:
            downloader._check_required_disk_space(space_required)
        except OSError as e:
            self.fail(str(e))
        finally:
            downloader._remove_temp_directory()

    def test__create_temp_directory(self):
        """Test if create temp directory works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        try:
            downloader._create_temp_directory()
            self.assertTrue(os.path.exists(downloader._temp_directory_path))
            self.assertIn(tempfile.gettempdir(), downloader._temp_directory_path)
        finally:
            downloader._remove_temp_directory()

    def test__check_required_disk_space_valid_same_disk_unavailable(self):
        """Test if check required disk space works as expected"""
        path1, path2 = CommonClass.generate_sample_file_paths(True, 'mp4')
        downloader = M3U8Downloader(self.input_file_path, path1)
        downloader._create_temp_directory()
        space_required = 2000000000000
        with self.assertRaises(OSError):
            downloader._check_required_disk_space(space_required)
        downloader._remove_temp_directory()

    def test__check_required_disk_space_valid_different_disk_available(self):
        """Test if check required disk space works as expected"""
        if len(CommonClass.get_available_disks()) > 1:
            path1, path2 = CommonClass.generate_sample_file_paths(False, 'mp4')
            downloader = M3U8Downloader(self.input_file_path, path2)
            downloader._create_temp_directory()
            space_required = 10
            try:
                downloader._check_required_disk_space(space_required)
            except OSError as e:
                self.fail(str(e))
            finally:
                downloader._remove_temp_directory()
        else:
            self.skipTest(
                'Skipping test__check_required_disk_space_valid_different_disk_available: Only one disk available'
            )

    def test__check_required_disk_space_valid_different_disk_unavailable(self):
        """Test if check required disk space works as expected"""
        if len(CommonClass.get_available_disks()) > 1:
            path1, path2 = CommonClass.generate_sample_file_paths(False, 'mp4')
            downloader = M3U8Downloader(self.input_file_path, path2)
            downloader._create_temp_directory()
            space_required = 2000000000000
            with self.assertRaises(OSError):
                downloader._check_required_disk_space(space_required)
            downloader._remove_temp_directory()
        else:
            self.skipTest(
                'Skipping test__check_required_disk_space_valid_different_disk_unavailable: Only one disk available'
            )

    def test__configure_debug_logger_valid(self):
        """Test if configure debug logger works as expected"""
        downloader = M3U8Downloader(
            self.input_file_path, self.output_file_path, debug=True, debug_file_path=self.debug_file_path
        )
        downloader._configure_debug_logger()
        self.assertTrue(os.path.exists(self.debug_file_path))
        expected_output = 'sample content'
        downloader._debug_logger.debug(expected_output)
        with open(self.debug_file_path, 'r') as file:
            file_content = file.read()
            self.assertIn(expected_output, file_content)

    def test__configure_debug_logger_invalid(self):
        """Test if configure debug logger raises AttributeError"""
        downloader = M3U8Downloader(
            self.input_file_path, self.output_file_path, debug=False, debug_file_path=self.debug_file_path
        )
        downloader._configure_debug_logger()
        self.assertFalse(os.path.exists(self.debug_file_path))
        with self.assertRaises(AttributeError):
            downloader._debug_logger.debug('sample content')

    def test__get_index_file_name_valid1(self):
        """Test if the get index file name works as expected"""
        expected_output = 'sample_index.m3u8'
        self.input_file_path = f'{CommonClass.get_git_test_parent_url()}/{expected_output}'
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        self.assertEqual(expected_output, downloader._get_index_file_name())

    def test__get_index_file_name_valid2(self):
        """Test if the get index file name works as expected"""
        expected_output = ' '
        self.input_file_path = f'{CommonClass.get_git_test_parent_url()}/sample_index.m3u8/ '
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        self.assertTrue(expected_output, downloader._get_index_file_name())

    def test__get_parent_url_valid(self):
        """Test if the get parent url works as expected"""
        expected_output = CommonClass.get_git_test_parent_url()
        self.input_file_path = f'{expected_output}/sample_index.m3u8'
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        self.assertEqual(expected_output, downloader._get_parent_url())

    def test__remove_temp_directory(self):
        """Test if remove temp directory works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        downloader._create_temp_directory()
        downloader._download_index_file()
        self.assertTrue(os.path.exists(downloader._temp_directory_path))
        downloader._remove_temp_directory()
        self.assertFalse(os.path.exists(downloader._temp_directory_path))

    def test__is_master_file_invalid(self):
        """Test if is master file works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        downloader._create_temp_directory()
        try:
            downloader._download_index_file()
            self.assertFalse(downloader._is_master_file())
        finally:
            downloader._remove_temp_directory()

    def test__is_master_file_valid(self):
        """Test if is master file works as expected"""
        self.input_file_path = f'{CommonClass.get_git_test_parent_url()}/sample_master.m3u8'
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        downloader._create_temp_directory()
        try:
            downloader._download_index_file()
            self.assertTrue(downloader._is_master_file())
        finally:
            downloader._remove_temp_directory()

    def test__is_playlist_file_invalid(self):
        """Test if is playlist file works as expected"""
        self.input_file_path = f'{CommonClass.get_git_test_parent_url()}/sample_master.m3u8'
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        downloader._create_temp_directory()
        try:
            downloader._download_index_file()
            self.assertFalse(downloader._is_playlist_file())
        finally:
            downloader._remove_temp_directory()

    def test__is_playlist_file_valid(self):
        """Test if is playlist file works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        downloader._create_temp_directory()
        try:
            downloader._download_index_file()
            self.assertTrue(downloader._is_playlist_file())
        finally:
            downloader._remove_temp_directory()

    def test__validate_invalid_url(self):
        """Test if validate raises ValueError"""
        self.input_file_path = f'junk//{CommonClass.get_git_test_parent_url()}/sample_index.m3u8'
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        with self.assertRaises(ValueError):
            downloader._validate()

    def test__validate_invalid_m3u8_url(self):
        """Test if validate raises ValueError"""
        self.input_file_path = f'{CommonClass.get_git_test_parent_url()}/sample_index.html'
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        with self.assertRaises(ValueError):
            downloader._validate()

    def test__download_index_file_valid(self):
        """Test if download index file works as expected"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        downloader._create_temp_directory()
        try:
            self.assertTrue(downloader._download_index_file())
            expected_output = os.path.join(downloader._temp_directory_path, 'index.m3u8')
            self.assertTrue(os.path.exists(expected_output))
        finally:
            downloader._remove_temp_directory()

    def test__download_index_file_invalid(self):
        """Test if download index file works as expected"""
        self.input_file_path = f'junk//{CommonClass.get_git_test_parent_url()}/junk.m3u8'
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        downloader._create_temp_directory()
        try:
            self.assertFalse(downloader._download_index_file())
        finally:
            downloader._remove_temp_directory()

    def test__download_and_write_invalid_sequence(self):
        """Test if download and write raises TypeError"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        downloader._create_temp_directory()
        try:
            with self.assertRaises(TypeError):
                downloader._download_index_file()
                files = open(os.path.join(downloader._temp_directory_path, 'index.m3u8'))
                downloader._download_and_write('seq', 'url', files)
        finally:
            files.close()
            downloader._remove_temp_directory()

    def test__download_and_write_invalid_url(self):
        """Test if download and write raises TypeError"""
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        downloader._create_temp_directory()
        try:
            with self.assertRaises(TypeError):
                downloader._download_index_file()
                files = open(os.path.join(downloader._temp_directory_path, 'index.m3u8'))
                downloader._download_and_write(0, 100, files)
        finally:
            files.close()
            downloader._remove_temp_directory()

    def test_download_playlist_with_skip_space_check(self):
        """Test if download playlist works as expected"""
        self.input_file_path = f'{CommonClass.get_git_test_parent_url()}/index.m3u8'
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path_with_mp4, True)
        try:
            output_buffer = io.StringIO()
            sys.stdout = output_buffer
            self.assertTrue(downloader.skip_space_check)
            downloader.download_playlist()
            sys.stdout = sys.__stdout__
            self.assertTrue(downloader.is_download_complete)
            self.assertNotIn('Verify', output_buffer.getvalue())
            self.assertIn('Download', output_buffer.getvalue())
            self.assertIn('Build', output_buffer.getvalue())
            self.assertTrue(os.path.exists(self.output_file_path_with_mp4))
            self.assertEqual(5589428, os.path.getsize(self.output_file_path_with_mp4))
            self.assertFalse(os.path.exists(downloader._temp_directory_path))
        finally:
            try:
                downloader._remove_temp_directory()
            except FileNotFoundError:
                pass

    def test_download_playlist_without_skip_space_check(self):
        """Test if download playlist works as expected"""
        self.input_file_path = f'{CommonClass.get_git_test_parent_url()}/index.m3u8'
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path_with_mp4, False)
        try:
            output_buffer = io.StringIO()
            sys.stdout = output_buffer
            self.assertFalse(downloader.skip_space_check)
            downloader.download_playlist()
            sys.stdout = sys.__stdout__
            self.assertTrue(downloader.is_download_complete)
            self.assertIn('Verify', output_buffer.getvalue())
            self.assertIn('Download', output_buffer.getvalue())
            self.assertIn('Build', output_buffer.getvalue())
            self.assertTrue(os.path.exists(self.output_file_path_with_mp4))
            self.assertEqual(5589428, os.path.getsize(self.output_file_path_with_mp4))
            self.assertFalse(os.path.exists(downloader._temp_directory_path))
        finally:
            try:
                downloader._remove_temp_directory()
            except FileNotFoundError:
                pass

    def test_download_playlist_without_merge(self):
        """Test if download playlist works as expected"""
        self.input_file_path = f'{CommonClass.get_git_test_parent_url()}/index.m3u8'
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path_with_mp4)
        try:
            output_buffer = io.StringIO()
            sys.stdout = output_buffer
            self.assertFalse(downloader.skip_space_check)
            downloader.download_playlist(merge=False)
            sys.stdout = sys.__stdout__
            self.assertTrue(downloader.is_download_complete)
            self.assertIn('Verify', output_buffer.getvalue())
            self.assertIn('Download', output_buffer.getvalue())
            self.assertIn('Build', output_buffer.getvalue())
            dir_name = os.path.dirname(self.output_file_path_with_mp4)
            self.assertTrue(os.path.exists(dir_name))
            self.assertEqual(1860448, os.path.getsize(os.path.join(dir_name, 'video_0.ts.mp4')))
            self.assertEqual(1868344, os.path.getsize(os.path.join(dir_name, 'video_1.ts.mp4')))
            self.assertEqual(1860636, os.path.getsize(os.path.join(dir_name, 'video_2.ts.mp4')))
            self.assertFalse(os.path.exists(downloader._temp_directory_path))
        finally:
            try:
                downloader._remove_temp_directory()
            except FileNotFoundError:
                pass

    def test_download_playlist_with_debug(self):
        """Test if download playlist works as expected"""
        self.input_file_path = f'{CommonClass.get_git_test_parent_url()}/index.m3u8'
        downloader = M3U8Downloader(
            self.input_file_path, self.output_file_path_with_mp4, False, True, self.debug_file_path
        )
        try:
            output_buffer = io.StringIO()
            sys.stdout = output_buffer
            self.assertFalse(downloader.skip_space_check)
            self.assertTrue(downloader.debug)
            downloader.download_playlist()
            sys.stdout = sys.__stdout__
            self.assertTrue(downloader.is_download_complete)
            self.assertIn('Verify', output_buffer.getvalue())
            self.assertIn('Download', output_buffer.getvalue())
            self.assertIn('Build', output_buffer.getvalue())
            self.assertTrue(os.path.exists(self.output_file_path_with_mp4))
            self.assertEqual(5589428, os.path.getsize(self.output_file_path_with_mp4))
            self.assertFalse(os.path.exists(downloader._temp_directory_path))
            assert os.path.getsize(self.debug_file_path) > 0
            with open(self.debug_file_path, 'r') as debug_file:
                file_content = debug_file.read()
                self.assertIn('video_0.ts', file_content)
                self.assertIn('video_1.ts', file_content)
                self.assertIn('video_2.ts', file_content)
        finally:
            try:
                downloader._remove_temp_directory()
            except FileNotFoundError:
                pass

    def test_download_master_playlist_with_no_params(self):
        """Test if download master playlist works as expected"""
        self.input_file_path = f'{CommonClass.get_git_test_parent_url()}/master.m3u8'
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        try:
            with self.assertRaises(UserWarning):
                downloader.download_master_playlist()
        finally:
            try:
                downloader._remove_temp_directory()
            except FileNotFoundError:
                pass

    def test_download_master_playlist_with_no_params(self):
        """Test if download master playlist works as expected"""
        self.input_file_path = f'{CommonClass.get_git_test_parent_url()}/master.m3u8'
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        try:
            with self.assertRaises(UserWarning):
                downloader.download_master_playlist()
        finally:
            try:
                downloader._remove_temp_directory()
            except FileNotFoundError:
                pass

    def test_download_master_playlist_no_name_available(self):
        """Test if download master playlist works as expected"""
        self.input_file_path = f'{CommonClass.get_git_test_parent_url()}/master.m3u8'
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        try:
            with self.assertRaises(M3U8DownloaderError):
                downloader.download_master_playlist(name='720')
        finally:
            try:
                downloader._remove_temp_directory()
            except FileNotFoundError:
                pass

    def test_download_master_playlist_no_bandwidth_available(self):
        """Test if download master playlist works as expected"""
        self.input_file_path = f'{CommonClass.get_git_test_parent_url()}/master.m3u8'
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        try:
            with self.assertRaises(M3U8DownloaderError):
                downloader.download_master_playlist(bandwidth='1300000')
        finally:
            try:
                downloader._remove_temp_directory()
            except FileNotFoundError:
                pass

    def test_download_master_playlist_no_resolution_available(self):
        """Test if download master playlist works as expected"""
        self.input_file_path = f'{CommonClass.get_git_test_parent_url()}/master.m3u8'
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path)
        try:
            with self.assertRaises(M3U8DownloaderError):
                downloader.download_master_playlist(resolution='320x240')
        finally:
            try:
                downloader._remove_temp_directory()
            except FileNotFoundError:
                pass

    def test_download_master_playlist_with_valid_params(self):
        """Test if download master playlist works as expected"""
        self.input_file_path = f'{CommonClass.get_git_test_parent_url()}/master.m3u8'
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path_with_mp4)
        try:
            output_buffer = io.StringIO()
            sys.stdout = output_buffer
            self.assertFalse(downloader.skip_space_check)
            downloader.download_master_playlist(resolution='960x540')
            sys.stdout = sys.__stdout__
            self.assertTrue(downloader.is_download_complete)
            self.assertIn('Verify', output_buffer.getvalue())
            self.assertIn('Download', output_buffer.getvalue())
            self.assertIn('Build', output_buffer.getvalue())
            self.assertTrue(os.path.exists(self.output_file_path_with_mp4))
            self.assertEqual(5589428, os.path.getsize(self.output_file_path_with_mp4))
            self.assertFalse(os.path.exists(downloader._temp_directory_path))
        finally:
            try:
                downloader._remove_temp_directory()
            except FileNotFoundError:
                pass

    def test_download_master_playlist_with_valid_params_and_no_merge(self):
        """Test if download master playlist works as expected"""
        self.input_file_path = f'{CommonClass.get_git_test_parent_url()}/master.m3u8'
        downloader = M3U8Downloader(self.input_file_path, self.output_file_path_with_mp4)
        try:
            output_buffer = io.StringIO()
            sys.stdout = output_buffer
            self.assertFalse(downloader.skip_space_check)
            downloader.download_master_playlist(resolution='960x540', merge=False)
            sys.stdout = sys.__stdout__
            self.assertTrue(downloader.is_download_complete)
            self.assertIn('Verify', output_buffer.getvalue())
            self.assertIn('Download', output_buffer.getvalue())
            self.assertIn('Build', output_buffer.getvalue())
            dir_name = os.path.dirname(self.output_file_path_with_mp4)
            self.assertTrue(os.path.exists(dir_name))
            self.assertEqual(1860448, os.path.getsize(os.path.join(dir_name, 'video_0.ts.mp4')))
            self.assertEqual(1868344, os.path.getsize(os.path.join(dir_name, 'video_1.ts.mp4')))
            self.assertEqual(1860636, os.path.getsize(os.path.join(dir_name, 'video_2.ts.mp4')))
            self.assertFalse(os.path.exists(downloader._temp_directory_path))
        finally:
            try:
                downloader._remove_temp_directory()
            except FileNotFoundError:
                pass


if __name__ == "__main__":
    unittest.main()
