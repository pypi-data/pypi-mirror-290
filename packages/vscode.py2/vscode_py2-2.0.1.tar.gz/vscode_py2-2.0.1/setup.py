import os
from setuptools import setup, find_packages

version = "2.0.1"

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

if os.path.isfile("vscode/extcode.js"):
    with open("vscode/extcode.js", "r", encoding="utf-8") as js_file:
        data = f"'''{js_file.read()}'''"

    with open("vscode/extcode.py", "w", encoding="utf-8") as data_py:
        data_py.write(data)

setup(
    name="vscode.py2",
    version=version,
    description="Create VSCode Extensions with python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="kidandcat",
    author_email="kidandcat@gmail.com",
    packages=find_packages(),
    url="https://github.com/kidandcat/vscode.py",
    project_urls={
        "Issue tracker": "https://github.com/kidandcat/vscode.py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    install_requires=["websockets"],
    python_requires=">=3.8",
)
