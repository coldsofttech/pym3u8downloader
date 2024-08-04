from pym3u8downloader import M3U8Downloader

if __name__ == "__main__":
    downloader = M3U8Downloader(
        input_file_path='https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8',
        output_file_path=r'C:\Users\pooja\Downloads\test\output.mp4'
    )
    downloader.download_master_playlist()
