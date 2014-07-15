from distutils.core import setup
setup(
    name = 'asyncaws',
    packages = ['asyncaws'],
    version = '0.1.0',
    description = 'Asynchronous AWS library in Python',
    author = 'Anton Caceres',
    author_email = 'm@e5t.ro',
    url = 'http://caceres.me/asyncaws',
    download_url = 'https://github.com/MA3STR0/asyncaws/tarball/v0.1',
    keywords = ['aws', 'sqs', 'sns', 'tornado', 'boto'],
    classifiers = [],
    install_requires=[
        "tornado",
        "lxml",
        "futures"
    ],
)
