from setuptools import setup, find_packages

setup(
    name='varsync',
    version='1.0-alpha',
    description='A package for managing user variables with a web UI',
    author='Sriharan',
    author_email='sriharan2544@gmail.com',
    packages=find_packages(),
    install_requires=[
        'mysql-connector-python',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'varsync=cli:main',
        ],
    },
)
