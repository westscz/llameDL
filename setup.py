import os

from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open('requirements/requirements-prod.txt') as f:
    required = f.read().splitlines()


setup(
    name="LlameDL",
    version="0.2.1",
    author="Jaroslaw Piszczala",
    author_email="jaroslawpiszczala@gmail.com",
    description="Download music from YouTube and add tags",
    install_requires=required,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "llamedl = llamedl:llamedl_cli",
            "llametagger = llamedl:tagger_cli",
        ]
    },
    packages=["llamedl", "tests"],
    package_data={"llamedl/tagsproviders": ["tagsproviders/whitelist.cfg"]},
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python 3",
        "Topic :: Multimedia :: Audio",
    ],
    test_suite="tests",
)
