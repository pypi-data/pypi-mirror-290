from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dlsys",
    version="0.1.5",  # Update this version number manually
    author="Mark Powers",
    author_email="mpoweru@lifsys.com",
    description="A versatile downloader for various types of internet content",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lifsys/dlsys",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "yt-dlp",
        "requests",
        "pydub",
    ],
    entry_points={
        "console_scripts": [
            "dlsys=dlsys.cli:main",
        ],
    },
)
