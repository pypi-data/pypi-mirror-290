from setuptools import setup, find_packages

setup(
    name="eyvitel_lambda_sdk",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    description="Lambda Workflow AI",
    author="Shankar Narayan G",
    license="MIT"
)