import setuptools

setuptools.setup(
    name="tweedekamer",
    version="0.0.1-beta1",
    author="Michel Doré",
    author_email="",
    description="A package to download Dutch parliament debates and subtitles",
    long_description="Using this package you can download Dutch parliament debates and subtitles. It is based on the website https://debatgemist.tweedekamer.nl. This package is not affiliated with the Dutch parliament. It is not allowed to use this package for commercial purposes.\n This package is still in beta, so expect bugs and missing features.",
    package_dir={'': 'tweedekamer'},
    packages=setuptools.find_packages(where='tweedekamer'),
)