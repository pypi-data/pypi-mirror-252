from setuptools import setup, find_packages

with open("Readme.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name='EntityExtractor',
    author='Ankit Mor',
    version='0.1.4',
    packages=find_packages(),
    description='Extract specific entities from a text. Give text and get a JSON formatted output data.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'pandas>=2.0.3',
        'numpy>=1.24.3',
        'nltk>=3.8.1',
        'requests',
        'BeautifulSoup4',
        'spacy>=3.7.2',
    ],
)
