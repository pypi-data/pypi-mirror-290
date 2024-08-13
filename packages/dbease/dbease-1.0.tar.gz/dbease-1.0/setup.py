from setuptools import setup, find_packages

setup(
    name="dbease",
    version="1.0", 
    author="Mohammad Mohammadi Bijaneh", 
    author_email="hiostad6@gmail.com", 
    description="This is a program designed to facilitate communication with the database, preventing unnecessary congestion in the source.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
    python_requires='>=3.8',
    install_requires=[

    ],
)
