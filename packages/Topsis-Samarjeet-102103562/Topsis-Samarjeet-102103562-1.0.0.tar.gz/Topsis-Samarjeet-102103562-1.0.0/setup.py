import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Topsis-Samarjeet-102103562",
    version="1.0.0",
    description="A Python package designed for performing Topsis analysis in the context of multiple-criteria decision making (MCDM). This package generates Topsis scores and ranks items accordingly.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Samarjeet09/Topsis-python-package",
    author="Samarjeet Singh",
    author_email="singhsamarjeet09@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["Topsis_Samarjeet_102103562"],
    include_package_data=True,
    install_requires="pandas",
    entry_points={
    "console_scripts": [
        "topsis=Topsis_Samarjeet_102103562:main",
    ]
},
)
