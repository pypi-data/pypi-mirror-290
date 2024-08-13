import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "projen_modules",
    "version": "0.0.22",
    "description": "projen-modules",
    "license": "Apache-2.0",
    "url": "https://github.com/daveshepherd/projen-modules.git",
    "long_description_content_type": "text/markdown",
    "author": "Dave Shepherd<dave.shepherd@endor.me.uk>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/daveshepherd/projen-modules.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "projen_modules",
        "projen_modules._jsii"
    ],
    "package_data": {
        "projen_modules._jsii": [
            "projen-modules@0.0.22.jsii.tgz"
        ],
        "projen_modules": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "constructs==10.3.0",
        "jsii>=1.102.0, <2.0.0",
        "projen==0.85.0",
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
