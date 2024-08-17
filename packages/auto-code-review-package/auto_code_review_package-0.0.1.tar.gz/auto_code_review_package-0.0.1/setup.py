from setuptools import setup

VERSION = '0.0.1' 
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'


setup(
    name="auto-code-review-package",
    version='0.0.1',
    install_requires=[
"python-gitlab", "sagemaker","langchain", "langchain_core","langchain_community","langchain_openai", "boto3", "utils", "atlassian-python-api", "markdownify", "httpx", "requests",
    ],
description = "A tool that integrates with Gitlab CICD pipelines to perform automated code reviews on commits and MRs",
)