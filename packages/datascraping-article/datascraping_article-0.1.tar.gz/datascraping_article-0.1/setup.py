from setuptools import setup, find_packages

setup(
    name='datascraping_article',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'selenium',
        'datetime'
    ],
    author="Chesta Dhingra",
    author_email="chestadhingra25@gmail.com",
    license='MIT',
    description="A python package for web scraping the latest articles on popular Data science blogs",
    long_description=open('README.md').read(),
    url="https://github.com/Chesta1/datascience_article_scrapping"  # Replace with your URL or remove if not applicable
)