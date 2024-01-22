import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
with open(HERE / "README.md", "r", encoding="utf-8") as readme_file:
    README = readme_file.read()

# This call to setup() does all the work
setup(
    name="Topsis-Rohan-102103108",
    version="1.1.1",
    description="Topsis-Rohan-102103108",
    long_description=README,
    long_description_content_type="text/markdown",  # Specify the content type
    url="https://github.com/Rohan1405/Topsis-Rohan-102103108",
    author="Rohan Gulati",
    author_email="gulatirohan2003@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "Topsis=Topsis.__main__:main",  # Update the module path
        ]
    },
)
