# setup.py

from setuptools import setup, find_packages

setup(
    name="AudioNest",
    version="0.2.0",  # Updated version
    packages=find_packages(),
    install_requires=[
        "vosk",
        "ffmpeg-python",
    ],
    author="Anudeep Satya Sai",
    author_email="edaradeepu74@gmail.com",
    description="Convert any audio file to text with AudioNest",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/audionest",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
