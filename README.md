# Opentrons with uv

## Find robots on your network

### Install uv

- [Install uv](https://docs.astral.sh/uv/getting-started/installation/)

### Run the script

- Clone this repo
- In this directory
  - `uv run robots.py`

## Opentrons Simulate or Analyze with `uv`

- inspired by [Python Bytes](https://pythonbytes.fm/episodes/show/415/just-put-the-fries-in-the-bag-bro)
- [Trey Hunter article](https://treyhunner.com/2024/12/lazy-self-installing-python-scripts-with-uv/?featured_on=pythonbytes)

Loving uv.  The below with uv works on Linux and Windows.

## YouTube video of how to

<https://youtu.be/sOkQarSADIc>

## uv

- [Install uv](https://docs.astral.sh/uv/getting-started/installation/)

## Analyze your protocol

1. drop your protocols in the `protocols` directory
1. put you custom labware in the `custom_labware` directory
1. `uv run analyze.py`
1. look in the results directory for the analysis output JSON files

## Simulate your protocol

1. drop your protocols in the `protocols` directory
1. put you custom labware in the `custom_labware` directory
1. `uv run simulate.py`
1. look in the results directory for the analysis output .txt files

## Notes

### Script with embedded metadata

```python
# /// script
# requires-python = "==3.10.*"
# dependencies = [
#     "opentrons==8.3.0",
#     "opentrons-shared-data==8.3.0",
# ]
# ///
```

> uv will read this [script with embedded metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/#example) and get you the right python (if you didn't already have it) and dependencies.

### uv tool to call opentrons_simulate at the command line

> see [uv tool vs uvx](https://docs.astral.sh/uv/concepts/tools/#tool-environments)

- `uv tool install opentrons@8.3.0a2 --python 3.10 --prerelease=allow`
  - note that when I tried this without the `--prerelease=allow` I got an excellent error message from uv.
- `uv run opentrons_simulate --version --python 3.10`
- `uv run opentrons_simulate --help --python 3.10`
