# encoding: utf-8
#
import sys
from setuptools import setup

with open("README.md", "r", encoding="utf8") as readme_file:
    readme = readme_file.read()

setup_requirements = [
    "setuptools_scm==3.5.0",
]

install_requires = [
    "requests >= 2.18",
    "sseclient-py >= 1.7",
    "pytz",
    "pandas >= 0.21",
    "future >= 0.16",
]
if sys.version_info < (3,):
    install_requires.append("configparser >= 3.5")

setup(
    name="ampdata",
    packages=["ampdata"],
    install_requires=install_requires,
    tests_require=[
        "pytest",
        "pytest-cov >= 2.5",
        "requests-mock >= 1.3",
    ],
    use_scm_version=True,
    setup_requires=setup_requirements,
    description="Ampiato AmpData Python library.",
    long_description=readme,
    author="Ampiato",
    author_email="info@ampiato.com",
    url="https://ampiato.com.com",
    package_data={"ampdata": ["VERSION"]},
)
