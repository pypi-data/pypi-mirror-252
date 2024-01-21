from setuptools import setup, find_packages


setup(
    name="OOPyGUI",
    version="1.0.1",
    author="artandfi (Artem Fisunenko)",
    author_email="artyom.fisunenko@gmail.com",
    description="OOPyGUI is an object-oriented wrapper for DearPyGUI (https://github.com/hoffstadt/DearPyGui).",
    packages=find_packages(),
    install_requires=[line.strip() for line in open("requirements.txt", "r").readlines()],
    keywords=[
        "Python3",
        "GUI"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)
