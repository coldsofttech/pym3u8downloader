from setuptools import setup

import pym3u8downloader

setup(
    name=pym3u8downloader.__name__,
    version=pym3u8downloader.__version__,
    packages=[
        pym3u8downloader.__name__
    ],
    url='https://github.com/coldsofttech/pym3u8downloader',
    license='MIT',
    author='coldsofttech',
    description=pym3u8downloader.__description__,
    install_requires=[
        "requests",
        "pyloggermanager"
    ],
    requires_python=">=3.10",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=["m3u8-playlist", "m3u8", "m3u8-downloader"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ]
)
