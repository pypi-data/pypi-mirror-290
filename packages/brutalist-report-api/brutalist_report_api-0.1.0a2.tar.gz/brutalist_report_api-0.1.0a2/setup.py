from setuptools import setup, find_packages

with open('README.md', "r", encoding="utf8") as desc:
    long_description = desc.read()

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: Implementation :: CPython",
    "Operating System :: OS Independent",
]

install_requires = [
    "beautifulsoup4",
    "aiohttp",
    "requests",
    "lxml",
]


setup(
    name='brutalist_report_api',
    description="An scraper api for the brutalist.report website.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='0.1.0-alpha2',
    packages=find_packages(),
    url='https://github.com/BeastImran/brutalist.report-api',
    author='BeastImran',
    author_email='imsalmanran789@gmail.com',
    install_requires=install_requires,
    classifiers=classifiers,
    python_requires='>=3.6',
    platforms='any',
)