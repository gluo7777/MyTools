from setuptools import setup, find_packages

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mytools',
    version='1.0.0',
    author="William Luo",
    author_email="gluo7777@gmail.com",
    description="Utilities for local automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click'
        ,'colorama',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        mytools=cli.scripts.main:entry
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.1'
)