from setuptools import setup, find_packages

VERSION = '0.0.1'

setup(
    name='audio_sleuth',
    version=VERSION,
    author='theadamsabra (Adam Sabra)',
    description='an open-source framework for detecting audio generated from generative systems',
    packages=find_packages(),
    install_requires=['torch', 'torchaudio', 'librosa', 'numpy']
)