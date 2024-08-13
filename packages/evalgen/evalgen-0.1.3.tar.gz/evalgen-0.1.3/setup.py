import os
import sys
from setuptools import setup, find_packages

thisdir = os.path.dirname(__file__)
readme = open(os.path.join(thisdir, "README.md")).read()

setup(
    name='evalgen',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'click',
        'sqlalchemy',
        'langchain',
        'openai',
        'mkdocs',
        'mkdocstrings[python]',
        'mkdocs-material',
        'python-dotenv',
        'pandas',
        'pyyaml',
        'tabulate'
    ],
    entry_points={
        'console_scripts': [
            'evalgen=evalgen.cli:main',
        ],
    },
    # Additional metadata
    author='Scribble Data, Inc',
    author_email='support@scribbledata.io',
    description='Generate eval datasets from arbitrary sources',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/scribbledata/evalgen',  # Replace with your repository URL
    license='MIT',  # Replace with your license
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
