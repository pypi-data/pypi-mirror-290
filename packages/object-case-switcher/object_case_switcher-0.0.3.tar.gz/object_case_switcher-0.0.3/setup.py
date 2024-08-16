from setuptools import setup, find_packages
import os

NAME = "object_case_switcher"
VERSION = "0.0.3"

setup(
    version=VERSION,
    name=NAME,
    description="The easiest way to switch case of prop in return of your functions",

    long_description=open(os.path.join(os.path.dirname(__file__), './README.md')).read(),
    long_description_content_type='text/markdown',
    
    packages=find_packages(),

    keywords=["python", "switch", "switcher", "case", "snake", "camel"],

    author="Aleksandrychev Andrey",
    author_email="aleks-andr-19@yandex.ru",
    url="https://github.com/Alex-Andr-19/case_switcher",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
