import setuptools

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="tweedekamer",
    version="0.0.7-beta1",
    author="Michel Doré",
    author_email="",
    description="A package to download Dutch parliament debates and subtitles",
    long_description=long_description,
    long_description_content_type='text/markdown',
    # package_dir={'': 'tweedekamer'},
    packages=["tweedekamer", "tweedekamer.enums"],
    url="https://github.com/micheldore/tweedekamer",
)