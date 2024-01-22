import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Topsis-Swasti-102103285",
    version="1.0.0",
    description="Performs TOPSIS",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sswasti1903/Topsis-Swasti-102103285",
    author="Swasti",
    author_email="sswasti_be21@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["Topsis"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "Topsis=Topsis.__main__:main",
        ]
    },
)