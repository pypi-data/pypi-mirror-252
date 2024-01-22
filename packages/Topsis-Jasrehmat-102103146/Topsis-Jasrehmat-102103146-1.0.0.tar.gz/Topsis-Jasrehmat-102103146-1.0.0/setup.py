import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="Topsis-Jasrehmat-102103146",
    version="1.0.0",
    description="Gives the TOPSIS score and rank for your data",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Jasrehmat Kaur",  # Fixed: Added a comma after the author's name
    author_email="jasrehmat2003@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",  # Fixed: Corrected the license classifier
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["Topsis"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "topsis=Topsis.__main__:main",
            ]

    },
)
