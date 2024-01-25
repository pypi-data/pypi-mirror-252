from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="OhlcvAnalyser",
    version="0.0.1",
    author='jackmappotion',
    author_email='jackmappotion@gmail.com',
    description='ohlcv analyser',
    long_description=long_description,    
)
