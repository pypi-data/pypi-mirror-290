from setuptools import setup, find_packages

setup(
    name="byteCaptcha3",
    version="1.0.1",
    description="A Python library for generating complex CAPTCHAs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="h3xcolor",
    author_email="oktk0728@gmail.com",
    url="https://github.com/sjskUw/ByteCaptcha3",
    packages=find_packages(),
    install_requires=[
        "Pillow",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
