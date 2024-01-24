import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-codestarconnection",
    "version": "0.0.13",
    "description": "AWS CDK L2 construct for aws code star connection",
    "license": "Apache-2.0",
    "url": "https://github.com/JumpToTheCloud/aws-codestarconnection",
    "long_description_content_type": "text/markdown",
    "author": "Antonio Márquez Pérez<antonio.marquez@jumptothecloud.tech>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/JumpToTheCloud/aws-codestarconnection"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_codestarconnection",
        "aws_codestarconnection._jsii"
    ],
    "package_data": {
        "aws_codestarconnection._jsii": [
            "aws-codestarconnection@0.0.13.jsii.tgz"
        ],
        "aws_codestarconnection": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.122.0, <3.0.0",
        "constructs>=10.3.0, <11.0.0",
        "jsii>=1.94.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
