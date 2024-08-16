from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='datablender',
    version='1.0',
    description='Tools for data.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/MontrealMobilite/datablender.git',
    author='Julien Douville',
    packages=find_packages(),
    zip_safe=False,
    test_suite="tests",
    install_requires =[
        'sqlalchemy',
        'psycopg2',
        'datetime',
        'numpy',
        'pandas',
        'dbf',
        'openpyxl',
        'beautifulsoup4',
        'selenium',
        'webdriver_manager',
        'postgis',
        'python-socketio',
        'dbfread',
        'scipy',
        'scikit-learn',
        'unidecode',
        'geopandas',
        'aiohttp',
        'asyncpg'
    ],
    extras_require={
        'dev': [
            'pytest',
            'build',
            'twine'
        ]
    }
)