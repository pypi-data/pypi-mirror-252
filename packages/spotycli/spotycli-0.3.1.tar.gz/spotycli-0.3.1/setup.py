# setup.py
from setuptools import setup, find_packages

try:
   import pypandoc
   long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
   long_description = open('README.md').read()

setup(
    name='spotycli',
    version='0.3.1',
    author="micheledinelli",
    author_email="dinellimichele00@gmail.com",

    long_description_content_type="text/markdown",

    long_description=long_description,

    package_dir={'': 'src'},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=[
        'typer',
        'spotipy',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'spotycli = spotycli.main:app',
        ],
    },
)
