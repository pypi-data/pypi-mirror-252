from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mycreds_package",
    version="0.0.3",
    packages=find_packages(),
    install_requires=[
        "reportlab>=4.0.9",
        "selenium>=4.16.0",
    ],
    package_data={
        "mycreds_package": ["certMaker/fonts/*.ttf", "certMaker/templates/*.jpg"],
    },
    author="David Wong",
    author_email="d78wong@uwaterloo.ca",
    description="MyCreds Project Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    url="https://github.com/wongd1532/MyCreds/",
)