from setuptools import setup, find_packages

setup(
    name="avahi-summarize",
    version="0.1",
    packages=find_packages(),
    description="Summarizes an article with the use of aws bedrock model claude 3 Sonnet",
    install_requires=[
        "boto3"
    ]
)