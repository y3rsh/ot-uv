# Opentrons Simulate with `uv` versus `pyenv + pipenv`

- inspired by [Python Bytes](https://pythonbytes.fm/episodes/show/415/just-put-the-fries-in-the-bag-bro)
- [Trey Hunter article](https://treyhunner.com/2024/12/lazy-self-installing-python-scripts-with-uv/?featured_on=pythonbytes)

Loving uv.  The below with uv works on Windows and Linux.

## uv

- [Install uv](https://docs.astral.sh/uv/getting-started/installation/)

### uv tool to call opentrons_simulate at the command line

> see [uv tool vs uvx](https://docs.astral.sh/uv/concepts/tools/#tool-environments)

- `uv tool install opentrons@8.3.0a2 --python 3.10 --prerelease=allow`
  - note that when I tried this without the `--prerelease=allow` I got an excellent error message from uv.
- `uv run opentrons_simulate --version --python 3.10`
- `uv run opentrons_simulate --help --python 3.10`

### Programmatic simulate with uv

example1.py and example2.py have this at the top:

```python
# /// script
# requires-python = "==3.10.*"
# dependencies = [
#     "opentrons==8.3.0a2",
#     "opentrons-shared-data==8.3.0a2",
# ]
# ///
```

> uv will read this [script with embedded metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/#example) and get you the right python (if you didn't already have it) and dependencies.

- `uv run example1.py`
- `uv run example2.py`

## pyenv + pipenv

An effective setup.  These are great tools we have trusted for years but uv is easier and faster.

1. [have pyenv and pipenv and then 3.10.* installed with pyenv](https://github.com/Opentrons/opentrons/blob/edge/DEV_SETUP.md#2-install-pyenv-and-python)
1. `pyenv local 3.10`
1. `pipenv install`

### opentrons_simulate installed script with pipenv

- `pipenv run opentrons_simulate --help`
- `pipenv run opentrons_simulate IDT_xGen_EZ_48x_v8.py`

### programmatic simulate with pipenv

- `pipenv run python example1.py`
- `pipenv run python example2.py`
