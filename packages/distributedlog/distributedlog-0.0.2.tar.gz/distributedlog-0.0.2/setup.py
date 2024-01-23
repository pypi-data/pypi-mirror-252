from setuptools import setup, find_packages

setup(
    name="distributedlog",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[],
    extras_require={},
    license="MIT",
    description="A Python module that provides a configurable class for writing local and remote errors and logs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Javier Romay",
    author_email="javi.romay@gmail.com",
    keywords=["python", "module", "class"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)