from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
requires = [
    "tortoise-orm==0.21.0",
    "disnake==2.9.2",
    "aiofiles==23.2.1",
    "loguru==0.7.2",
]


setup(
    name="crxsnake",
    version="1.3.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="CRX-DEV",
    author_email="cherniq66@gmail.com",
    url="https://discord.gg/EEp67FWQDP",
    license="MIT License",
    packages=find_packages(),
    install_requires=requires,
)
