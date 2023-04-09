from setuptools import setup

setup(
    name="dataschema",
    version="0.0.0",
    packages=["dataschema"],
    author="Christian Winger",
    author_email="c@wingechr.de",
    install_requires=[
        "jsonschema>=4.17",
        "frictionless>=5.10",
        "requests>=2.28",
        "appdirs>=1.4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_data={
        "dataschema": ["data/**"],
    },
)
