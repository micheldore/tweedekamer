# tweedekamer

A pypi package for retrieving Dutch parliamentary debate data.

Using this package you can download Dutch parliament debates and subtitles. It is based on the website <https://debatgemist.tweedekamer.nl>. This package is not affiliated with the Dutch parliament. It is not allowed to use this package for commercial purposes.

 This package is no longer in beta, but you still might expect bugs and missing features as the testing library is not finished.

## Installation

Install this package through pip.
The package requires Python >=3.7.9

```bash
  pip install tweedekamer
```

## Usage/Examples

### Retrieving subtitles

```python
from tweedekamer import Search

results = Search("belasting 2022", limit=1).result
results[0].subtitle.text
```

### Retrieving video link

```python
from tweedekamer import Search

results = Search("belasting 2022", limit=1).result
results[0].video.url
```

### Retrieving speaker information

For each debate there is a list of speakers

```python
from tweedekamer import Search

results = Search("belasting 2022", limit=1).result
results[0].speakers[0].name
results[0].speakers[0].party

results[0].speakers[0].speach.text
results[0].speakers[0].speach.subtitle
results[0].speakers[0].speach.tokenized
```

### Retrieve from list of URLs

It's also possible to retrieve data from a list of URLs.
These URLs can be retrieved from the website <https://debatgemist.tweedekamer.nl>.
Every URL should be a string in a list and should start with `https://debatgemist.tweedekamer.nl/debatten/`.

```python
from tweedekamer import Search

Search(urls=["https://debatgemist.tweedekamer.nl/debatten/vreemdelingen-en-asielbeleid-10"]).result
```

### Export to CSV

Export the results of your query to CSV, separate the data by speaker or keep the entire debate per row

```python
from tweedekamer import Search

Search("belasting 2022", limit=1).to_csv("entire_debate")
Search("belasting 2022", limit=1).to_csv("debate_per_speaker", separate_speakers=True)
```

## Features

- Retrieve date and info on debate
- Search debates by query, date range, and debate type
- Retrieve subtitle data
- Retrieve video data

## Run Locally

Use these instructions if you want to edit the package locally.

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
