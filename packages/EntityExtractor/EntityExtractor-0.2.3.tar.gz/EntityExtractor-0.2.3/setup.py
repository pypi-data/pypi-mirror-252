from setuptools import setup, find_packages

setup(
    name='EntityExtractor',
    author='Ankit Mor',
    version='0.2.3',
    packages=find_packages(),
    description='Extract specific entities from a text. Give text and get a JSON formatted output data.',
    long_description="nltk.download('punkt') , nltk.download('stopwords') , spacy.cli.download('web_en_core_lg')",
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
