from setuptools import find_packages, setup

setup(
    name="jfunctions",
    version="0.0.1",
    description="A python package of function that a regularly use",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description_content_type="text/markdown",
    url="https://github.com/Morganjake/JFunctions",
    author="Jake Morgan",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    install_requires=["bson >= 0.5.10"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
)
