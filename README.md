# tweedekamer

A pypi package for retrieving Dutch parliamentary debate data.

Using this package you can download Dutch parliament debates and subtitles. It is based on the website <https://debatgemist.tweedekamer.nl>. This package is not affiliated with the Dutch parliament. It is not allowed to use this package for commercial purposes.\n This package is still in beta, so expect bugs and missing features.

## Installation

Install this package through pip.
The package requires Python >=3.7.9

```bash
  pip install tweedekamer
```

## Usage/Examples

### Retrieving subtitles

```python
from tweedekamer import Debate, Search

results = Search().getDebates("belasting 2022", limit=1)
results[0].subtitle.text
```

### Retrieving video link

```python
from tweedekamer import Debate, Search

results = Search().getDebates("belasting 2022", limit=1)
results[0].video.link
```

## Features

- Retrieve date and info on debate
- Search debates by query, date range, and debate type
- Retrieve subtitle data
- Retrieve video data

## Run Locally

**Use these instructions if you want to edit the package locally**

Clone the project

```bash
  git clone https://github.com/micheldore/tweedekamer
```

Go to the project directory

```bash
  cd tweedekamer
```

Create the virtual environment (using Python 3)

```bash
  python -m venv env
  source env/bin/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

If you want to install the local version of the package

```bash
  python -m pip install -e .
```
