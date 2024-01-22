import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="topsis-taanisha-10210323",
    version="1.1.2",
    description="TOPSIS implementation by Divyam Malik",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/taanisha/topsis-taanisha-102103123",
    author="Taanisha Agarwal",
    author_email="taanisha777@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "pandas",
    ],
    entry_points={
        "console_scripts": [
            "topsis=Topsis.__main__:main",
        ],
    },
)
