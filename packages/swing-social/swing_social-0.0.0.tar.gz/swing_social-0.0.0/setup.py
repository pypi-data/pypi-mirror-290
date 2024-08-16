from setuptools import setup, find_packages

setup(
    name="swing_social",
    version="0.0.0",
    author="Swing Collection",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/swing-collection/swing-social",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)