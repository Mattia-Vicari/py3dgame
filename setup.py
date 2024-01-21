from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name = "py3dgame",
    version = "0.0.1",
    description = "",
    long_description = long_description,
    url = "https://github.com/Mattia-Vicari/py3dgame",
    author = "Vicarius",
    author_email = "",
    classifiers = [
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords = "",
    package_dir = {"py3dgame": "py3dgame"},
    python_requires = ">= 3.10",
    install_requires = ["numpy", "pygame"],
    project_urls = {
        "Bug Reports": "https://github.com/Mattia-Vicari/py3dgame/issues",
    }
)