import pathlib
import setuptools


setuptools.setup(
    name ="Topsis-Pranav-102103438",
    version = "0.1.0",
    description= "Topsis Package",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    # url="https://github.com/pranav2811",
    author="Pranav Powar",
    author_email="powar.pranav29@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    install_requires=["pandas","numpy","os"],
    packages = setuptools.find_packages(),
    include_package_data=True,
)