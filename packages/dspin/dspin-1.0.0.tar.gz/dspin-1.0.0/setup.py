from setuptools import find_packages, setup
import os

install_requires = [
    "anndata",
    "matplotlib",
    "scanpy",
    "tqdm",
    "igraph",
    "leidenalg",
]

version = "1.0.0"  

readme = open("README.md").read()  

setup(
    name="dspin",
    version=version,
    description="Short description of dspin",
    author="Jialong Jiang, Yingying Gong",
    author_email="your.email@example.com",
    packages=find_packages(),
    license="Apache License 2.0",
    python_requires=">=3.6, <3.12",
    install_requires=install_requires,
    # extras_require={"test": test_requires, "doc": doc_requires},
    test_suite="nose2.collector.collector",  
    long_description=readme,
    url="https://github.com/YingyGong/dspin",  
    download_url="https://github.com/YingyGong/dspin/archive/v{}.tar.gz".format(
        version
    ),
    keywords=[
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
