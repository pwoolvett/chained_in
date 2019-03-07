===============================
Chained In
===============================

LinkedIn2Latex

Sample Usage
------------

Show available scripts::

  $ python Chained In

Requirements
------------

- User requirements

   + python>=3.6
   + poetry (recommended)

- Development requirements

   + tox
   + docker >=18.09
   + docker-compose >= 1.22


Installation
------------

- User:

   + Install chained_in by running::

      $ poetry install --no-dev -v

   + Alternatively, create a virtualenv and manually install all the requirements
     listed in `./pyproject.toml` -> `tool.poetry.dependencies`

- Development:

   + Create virtualenv and install install chained_in (with
     development libs) by running::

      $ tox -e venv # internally this runs `poetry install -v`

   + Alternatively, create a virtualenv and manually install all the requirements
     listed in `./pyproject.toml` -> `tool.poetry.dependencies` and
     `tool.poetry.dev-dependencies`.


Testing
-------

Without virtualenv activated (!), run `tox` in the project root. This runs the following:

+ Unit tests and developer-designed tests:

   - located in tests/unit
   - run with pytest

+ Integration testing:

   - located in tests/integration
   - might use docker-compose
   - run with pytest

+ [DISABLED BY DEFAULT] User stories testing with behave and docker-compose:

   - located in tests/features
   - might use docker-compose
   - run with behave

+ Coverage reports:

   - located in `coverage.unit.xml` and `coverage.integration.xml`

+ Documentation:

   - Builds using sphinx
   - Source located at `docs/source`
   - Output located at `docs/build`

Contribute
----------

- Issue Tracker: git@github.com:pwoolvett/chained_in.git/issues
- Source Code: git@github.com:pwoolvett/chained_in.git

Support
-------

If you are having issues, please let us know.
Contact us at: Chained In

License
-------

MIT
