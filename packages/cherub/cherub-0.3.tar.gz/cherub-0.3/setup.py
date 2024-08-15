# setup.py

from setuptools import setup, find_packages

setup(
    name="cherub",
    version="0.3",
    author="Cherub",
    author_email="zhaungxinwei@gmail.com",
    description="A simple example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/mypackage",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        # List your dependencies here, e.g.:
        # 'requests',
    ],
)
