from setuptools import find_packages, setup

# 读取版本号
version = {}
with open("version.py") as fp:
    exec(fp.read(), version)

setup(
    name="protium",
    version=version["__version__"],
    author="Haohui",
    author_email="harveyquery@gmail.com",
    description="A simple example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Mile-Away/PROTIUM",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "ptm=protium.cli:cli",
        ],
    },
)
