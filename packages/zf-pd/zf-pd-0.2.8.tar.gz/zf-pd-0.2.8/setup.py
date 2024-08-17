from os import path as os_path
from subprocess import run as os_run

from loguru import logger
from setuptools import find_packages
from setuptools import setup

PACKAGE_NAME = 'zf-pd'
AUTHOR_NAME = 'Zeff Muks'
AUTHOR_EMAIL = 'zeffmuks@gmail.com'

logger.debug(f"Building {PACKAGE_NAME} documentation")
os_run(['python', 'docs.py'], capture_output=True, text=True)


def read_long_description():
    with open('README.md', 'r') as f:
        long_description = f.read()
    return long_description


def read_version():
    version_file = os_path.join(os_path.dirname(__file__), 'pd', 'version.py')
    with open(version_file) as file:
        exec(file.read())
    version = locals()['__version__']
    logger.debug(f"Building {PACKAGE_NAME} v{version}")
    return version


def get_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()


setup(
    name=PACKAGE_NAME,
    version=read_version(),
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description='pd supercharges your development workflows',
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={
        'pd.config': [
            'templates/*'
        ],
        'pd.init': [
            'templates/*',
        ],
        'pd.nginx': [
            'templates/*'
        ],
    },
    install_requires=get_requirements(),
    packages=find_packages(
        include=[
            'pd',
            'pd.*'
        ],
        exclude=[
            'venv',
            'venv.*'
        ]
    ),
    entry_points={
        'console_scripts': [
            'pd=pd.__main__:main'
        ]
    },
)
