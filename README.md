# WoodokuLearn

## Develop & Contribution

This python repository uses `pipenv` to manage package dependencies, it come with configuration file `Pipfile` that list all package dependencies.

To get started:

1. Install [Python](https://www.python.org/downloads/) 
2. Ensure you have added to the environment variables to run `pip`
4. `cd` to the repo
5. Install virtual environment and all package dependency with `pipenv`

```Shell
pip install pipenv
pipenv install --dev # Install all package dependency
pipenv shell 

# Install pre-commit linter
pre-commit install
pre-commit migrate-config 
pre-commit autoupdate
```

### Running the project
```Shell
pipenv shell # starts the virtual environment
python woodoku/game.py
```

### Installing third party packages
Same as using `pip` but with `pipenv` it will automatically update `Pipfile`
```Shell
# To install packages essential to run the game
pipenv install <package-name>
# To install packages that is only use in development
pipenv install --dev <package-name>
```

## TODO
- Add overview of Woodoku
- Add instruction on using `mypy`
- Add instruction on creating tests

