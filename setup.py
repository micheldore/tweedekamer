import setuptools

setuptools.setup(
    name="tweedekamer",
    version="0.0.1",
    author="Michel Doré",
    author_email="",
    description="A package to download Dutch parliament debates and subtitles",
    package_dir={'': 'tweedekamer'},
    packages=setuptools.find_packages(where='tweedekamer'),
)