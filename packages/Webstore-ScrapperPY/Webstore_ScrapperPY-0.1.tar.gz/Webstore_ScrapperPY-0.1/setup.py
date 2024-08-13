from setuptools import setup, find_packages

setup(
    name="Webstore_ScrapperPY",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Scott Avery",
    author_email="scottavery2001@gmail.com",
    description="A simple wrapper to scrape data from a web store.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/Scottyboi1/Webstore_ScrapperPY",  # Update with your repository URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
