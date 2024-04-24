from distutils.core import setup
import os


def read_file(fname):
    with open(fname, encoding='utf-8') as f:
        return f.read()


REQUIREMENTS = []

setup(
    name='tingxie',
    version='0.0.1',
    packages=['tingxie'],
    url='',
    license='',
    author='stern',
    author_email='',
    description='',
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'tingxie=tingxie:main',
            'phonics=tingxie:phonics',
        ],
    },
    package_data={
        'tingxie': [
            'words_alpha.txt'
        ]
    }
)
