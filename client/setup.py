import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

req_fn = HERE / "requirements.txt"
with open(req_fn, "r") as f:
    requirements = [ln.strip() for ln in f.readlines()]

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ddbclient",
    version="0.0.5",
    description="A wrapper for API calls to DispimDB",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/samrkinn/ddbclient",
    author="Sam Kinn",
    author_email="samrkinn@gmail.com",
    packages=["ddbclient"],
    include_package_data=True,
    install_requires=requirements,
)
