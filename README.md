# Opentrons Simulate with uv vs pipenv + pyenv

- inspired by [Python Bytes](https://pythonbytes.fm/episodes/show/415/just-put-the-fries-in-the-bag-bro)
- [Trey Hunter article](https://treyhunner.com/2024/12/lazy-self-installing-python-scripts-with-uv/?featured_on=pythonbytes)

Loving uv.  The below with uv works on Windows and Linux.

## uv

- [Install uv](https://docs.astral.sh/uv/getting-started/installation/)

### uv tool to call opentrons_simulate at the command line

> see [uv tool vs uvx](https://docs.astral.sh/uv/concepts/tools/#tool-environments)

- `uv tool install opentrons@8.3.0a2 --python 3.10 --prerelease=allow`
- `uv run opentrons_simulate --version --python 3.10`
- `uv run opentrons_simulate --help --python 3.10`

### Programmatic simulate with uv

> uv will read the [script with embedded metadata](https://packaging.python.org/en/latest/specifications/inline-script-metadata/#example) in the python file and get you the right python and dependencies.

- `uv run example1.py`
- `uv run example2.py`

## pipenv + pyenv

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
