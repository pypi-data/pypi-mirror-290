import pathlib


import setuptools

setuptools.setup(
    name="pyworldatlas",
    version="0.0.3",
    description="Brief description.",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://www.example.com",
    author="jcari-dev",
    license="The Unlicense",
    project_urls={
        "Documentation": "https://www.example.com/docs",
        "Source": "https://www.example.com/source"
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities"
    ],
    python_requires=">= 3.10, < 3.12",
    install_requires=["requests"],
    extras_require={
        "excel": ["openpyxl"]
    },
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ["pyworldatlas = pyworldatlas.cli:main"]
    }
)