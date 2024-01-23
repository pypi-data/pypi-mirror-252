import pathlib
import setuptools


setuptools.setup(
    name ="aditya-102103464",
    version = "1.1.1",
    description= "Topsis Package",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Aditya Goel",
    author_email="agoel3_be21@thapar.edu",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    install_requires=["pandas","numpy"],
    packages = setuptools.find_packages(),
    include_package_data=True,
)