# setup.py

from setuptools import setup, find_packages

setup(
    name="AudioNest",
    version="0.1.0",
    description="A package to convert audio files to text.",
    author="Anudeep Saty Sai",
    author_email="eadaradeepu74@gmail.com",
    url="https://github.com/AnudeepSatyaSai/audionest",  # Update with your actual URL
    packages=find_packages(),
    install_requires=[
        "pydub",
        "SpeechRecognition"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
