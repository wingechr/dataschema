from setuptools import setup

setup(
    name="oekolib-schema",
    version="0.0.0",
    packages=["oekolib.schema"],
    author="Christian Winger",
    author_email="c.winger@oeko.de",
    url="http://ek-gitlab.oeko.local/c.winger/oekolib-schema",
    install_requires=["jsonschema", "frictionless"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
