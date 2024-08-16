# Licensed under the LGPL 3.0 License.
# tkxml by numlinka.
# setup

# site
from setuptools import setup


setup(
    name = "tkxml",
    version = "1.0.0",
    description = "Using XML to layout tkinter widgets.",
    long_description = open("README_PyPI.md", "r", encoding="utf-8").read(),
    long_description_content_type = "text/markdown",
    author = "numlinka",
    author_email = "numlinka@163.com",
    url = "https://github.com/numlinka/pytkxml",
    package_dir={"": "src"},
    packages = ["tkxml"],
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 3",
    ],
    license = "LGPLv3",
    keywords = ["tkinter", "xml"],
    install_requires = []
)
