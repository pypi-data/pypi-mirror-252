from setuptools import setup, find_packages
with open("README.md","r") as f:
    description=f.read()
setup(
    name='generic-validator',
    version='0.2',
    author='Garbi Youssef',
    author_email='gharbiyoussef884@gmail.com',
    description="Is a tool for validating, transforming, and controlling data.",
    license="MIT",
    packages=find_packages(),
    long_description=description,
    long_description_content_type='text/markdown'
)
