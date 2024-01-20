from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

SHORT_DESCRIPTION = 'This package aims to facilitate API integrations of providers present in professional sport'

setup(
    name='sportsapi',
    version='0.1.0',
    author='Bastien Angeloz',
    author_email='bastien.angeloz@sportdatalab.fr',
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/sportdatalab/sportsapi',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
