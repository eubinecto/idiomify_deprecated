from setuptools import setup, find_packages

setup(
    name='idiomify',
    version='0.0.1',
    author='Eu-Bin KIM',
    author_email='tlrndk123@gmail.com',
    license='MIT LICENSE',
    # this is needed to include the subdirectories in the library
    # will include all subdirectories that include __init__.py file.
    # https://stackoverflow.com/a/43254082
    packages=find_packages()
)
