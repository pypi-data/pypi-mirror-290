# For help with building, packaging, and uploading to PyPI, visit:
# https://packaging.python.org/en/latest/tutorials/packaging-projects/
# and
# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/

from setuptools import setup

def get_version(rel_path):
    with open(rel_path) as f:
        exec(f.read())
    return locals()['__version__']

setup(
    version=get_version("apogee_connect_rpi/version.py")
)