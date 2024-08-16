from setuptools import setup, find_packages

setup(
    name='jolescraper',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'requests'
    ],
    description='A simple web scraper made using BeautifulSoup and requests libraries.',
    author='Joel Crasta',
    python_requires='>=3.6'
)