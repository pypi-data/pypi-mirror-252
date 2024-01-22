import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
with open(HERE / "README.md", "r", encoding="utf-8") as readme_file:
    README = readme_file.read()

# This call to setup() does all the work
setup(
    name="Topsis-Abhinandan-102103110",
    version="0.0.1",
    description="Topsis-Abhinandan-102103110",
    long_description=README,
    long_description_content_type="text/markdown",  # Specify the content type
    url="https://github.com/Abhinandan2003/Topsis-Abhinandan-102103110",
    author="Abhinandan Sharma",
    author_email="sabhi2003@gmail.com",
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
