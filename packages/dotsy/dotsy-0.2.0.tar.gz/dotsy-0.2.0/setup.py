from setuptools import setup, find_packages

setup(
    name="dotsy", 
    version="0.2.0",  
    author="Levi Davis",
    author_email="levi.davis.co@gmail.com",
    description="dot-accessible dictionaries (dicy) and dictionary-containing encyclopedia classes (ency)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lcdavis13/dotsy", 
    packages=find_packages(), 
    classifiers=[
        "Programming Language :: Python :: 3", 
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent", 
    ], 
    python_requires='>=3.6', 
)
