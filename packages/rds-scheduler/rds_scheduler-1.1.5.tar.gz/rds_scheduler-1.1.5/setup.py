import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "rds-scheduler",
    "version": "1.1.5",
    "description": "Automatic Start and Stop Scheduler for AWS RDS",
    "license": "Apache-2.0",
    "url": "https://github.com/badmintoncryer/cdk-rds-scheduler.git",
    "long_description_content_type": "text/markdown",
    "author": "Kazuho CryerShinozuka<malaysia.cryer@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/badmintoncryer/cdk-rds-scheduler.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "rds_scheduler",
        "rds_scheduler._jsii"
    ],
    "package_data": {
        "rds_scheduler._jsii": [
            "cdk-rds-scheduler@1.1.5.jsii.tgz"
        ],
        "rds_scheduler": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.144.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.102.0, <2.0.0",
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
