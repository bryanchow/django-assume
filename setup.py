import os
from setuptools import setup, find_packages

version = '0.1'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-assume',
    version = version,
    description = "Django app that allows administrators to log in to user " \
                  "accounts without having to provide a password",
    long_description = read('README.md'),
    classifiers = [],
    keywords = "",
    author = "Bryan Chow",
    author_email = '',
    url = 'https://github.com/bryanchow/django-assume',
    download_url = 'https://github.com/bryanchow/django-assume/tarball/master',
    license = "WTFPL",
    packages = find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'django',
    ],
)
