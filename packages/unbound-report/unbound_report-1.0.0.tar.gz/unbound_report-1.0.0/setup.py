from setuptools import setup, find_packages
from pathlib import Path
readme = (Path(__file__).parent / "README.md").read_text()


setup(
    name="unbound-report",
    version="1.0.0",  
    author="Prasad Sawant",  
    author_email="sawant.prasad0275@gmail.com",  
    description="A tool to extract test suite data from Robot Framework output.xml and generate HTML reports.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/prasad0275/unbound-report.git",  # Replace with your project's URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "robotframework",
        "Jinja2>=3.1.4",
    ],
    entry_points={
        "console_scripts": [
            "unboundreport=unbound_report.generate_report:main",  # Command to run script
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",  
    zip_safe=False,  
)
