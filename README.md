# WoodokuLearn

## Develop & Contribution

This python repository uses `pipenv` to manage package dependencies, it accompanies the config file `Pipfile` that lists all package dependencies.

To get started:

1. Install [Python](https://www.python.org/downloads/) 
2. Ensure you have added to the environment variables to run `pip`
4. `cd` to the repo
5. Install virtual environment and all package dependency with `pipenv`

```Shell
# Install all package dependency for development
pip install pipenv
pipenv install --dev 
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

### Installing third-party packages
Same as using `pip` but with `pipenv` it will automatically update `Pipfile`
```Shell
# To install packages essential to run the game
pipenv install <package-name>
# To install packages that are only used during development
pipenv install --dev <package-name>
```

### Imports
To allow a simulated experience of namespace in python it is important to note
that the core component of this project is packed into local packages defined in
`setup.cfg` using

    pipenv install -e .

This command is also automated when you run `pipenv install`, but stated here
for clarity

#### Example
Given the similar experience to using namespaces with local packages, import
statements from package `woodoku` should be similar to the following:
```python
from woodoku.entity.woodoku_board import WoodokuBoard
```
Note we start with the package name to the file name according to the file
structure


## TODO
- Add an overview of Woodoku
- Add instructions on creating tests

