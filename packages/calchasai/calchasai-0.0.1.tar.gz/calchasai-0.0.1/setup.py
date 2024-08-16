from setuptools import setup, find_packages

# Read the contents of your requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="calchasai",  # Replace with your desired package name
    version="0.0.1",  # Version number
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=requirements,  # Automatically load dependencies from requirements.txt
    author="ktz",
    author_email="your.email@example.com",
    description="A short description of your package",  # Replace with the URL to your package repository
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Adjust as needed
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Adjust the Python version requirement
)