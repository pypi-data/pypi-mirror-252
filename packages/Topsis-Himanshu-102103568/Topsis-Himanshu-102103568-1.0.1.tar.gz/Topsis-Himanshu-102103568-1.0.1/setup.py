from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

VERSION = '1.0.1'
DESCRIPTION = 'Implementation of Topsis'

setup(
    name="Topsis-Himanshu-102103568",
    version=VERSION,
    author="Himanshu Bansal",
    author_email="himu90505@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['Topsis', 'Topsis-Himanshu-102103568', 'Himanshu', 'Topsis-Himanshu', '102103568'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)