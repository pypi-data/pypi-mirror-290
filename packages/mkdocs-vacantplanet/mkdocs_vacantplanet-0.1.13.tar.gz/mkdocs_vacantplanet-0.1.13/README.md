MkDocs Vacant Planet Theme
=========================

This is a theme for MkDocs which is mainly used in [VacantPlanet](https://vacantplanet.dev) projects 

## Installation

Install the package from PyPi using `pip`:

    pip install mkdocs-vacantplanet

Add the theme to your `mkdocs.yml` file:

    theme:
        name: vacantplanet

## Development server

    mkdocs serve -w theme   

## Styles

Install Dart Sass via `npm install -g sass`. During develompment:

    sass --watch styles:theme

## Deploy to PyPi

Install `twine` and `build` if not already done. Bump version number in `setup.py`, then:

    git tag -a vX.X.X -m "Version X.X.X"
    git push origin vX.X.X
    sass --style=compressed --no-source-map styles:theme
    python -m build
    python -m twine upload dist/*
