# setup.py

from setuptools import setup, find_packages

setup(
    name='seaBlock',
    version='0.1',
    packages=find_packages(),
    description='Sanctioned Encryption Algorithm (SEA)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ritul(void)',
    author_email='codebyritul@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
