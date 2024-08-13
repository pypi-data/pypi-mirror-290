from setuptools import setup, find_packages

setup(
    name="pynetdiscover",
    version="0.1.0",
    description="A Python module to scan devices on the network.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Oxcanga",
    author_email="ilgcreatny@gmail.com",
    packages=find_packages(),
    install_requires=[
        "scapy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
