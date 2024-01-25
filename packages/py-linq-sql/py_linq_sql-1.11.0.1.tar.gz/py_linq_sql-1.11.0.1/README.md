<!-- markdownlint-disable-file MD024 MD041 -->

![maintenance](https://img.shields.io/maintenance/yes/2023)
![open issue](https://img.shields.io/gitlab/issues/open-raw/exoplanet/py-linq-sql?gitlab_url=https%3A%2F%2Fgitlab.obspm.fr)

[![pipeline status](https://gitlab.obspm.fr/exoplanet/py-linq-sql/badges/main/pipeline.svg)](https://gitlab.obspm.fr/exoplanet/py-linq-sql/-/commits/main)
[![coverage report](https://gitlab.obspm.fr/exoplanet/py-linq-sql/badges/main/coverage.svg)](https://gitlab.obspm.fr/exoplanet/py-linq-sql/-/commits/main)

![Banner](https://py-linq-sql.readthedocs.io/en/latest/banner.png)

# Py-Linq-SQL

A Python module used for interacting with sql database using [LINQ](https://docs.microsoft.com/fr-fr/dotnet/api/system.linq.enumerable?view=net-6.0)
syntax. The project is under [EUPL License v1.2](LICENSE.md).

Py-linq-sql allows you to go from (SQLAlchemy using direct text query):

```python
conn.execute(
  text(
    """SELECT "data"->'obj'->'name' as name """
    """FROM "objects" """
    """WHERE "data"->'obj'->>'name' == "earth" """
    """AND CAST("data"->'obj'->'mass' > 0.5 AS Decimal) """
    """LIMIT 1 OFFSET 2"""
  )
)
```

to the safer and easier to read:

```python
sqle = (
  SQLEnumerable(conn, "objects")  # objects is the name of the table
  .select(lambda x: {"name": x.data.obj.name})  # data is a JSONB column
  .where(lambda x: x.data.obj.mass > 0.5)  # data is a JSONB column
  .skip(2)
  .take(1)  # this is the last part of the query, till there nothing is executed
  .execute()  # now we ask for the whole query to be executed on the DB server
)
```

Pro :

- all the query expression are expressed in pure python expression
- easy support of JSON database using a simple object notation
- very difficult to have an SQL injection (only the names of the tables are strings)
- standardized syntax/API of LINQ (used in java, C# and many .net languages)
- very fast: even very long and complex queries are executed in one single query on the
  server
- no need to define a class for every table in the DB as you would do in an ORM here you
  write query assuming the tables, columns and fields exist, if not then you get a clear
  error about it
- results are pylinq Enumerable that are themselves queryable in same way but locally
- all kinds of join (inner, outer and full, with or without intersections) are easy to
  use and combine with any kind of query

Cons :

- currently only support PostgresQL

Any feedback is welcome see [Contributing](CONTRIBUTING.md).

## Contacts

- Author: Ulysse CHOSSON (LESIA)
- Maintainer: Ulysse CHOSSON (LESIA)
- Email: <ulysse.chosson@obspm.fr>
- Contributors:
  - Pierre-Yves MARTIN (LESIA)

## Table of Content

- [Py-Linq-SQL](#py-linq-sql)
  - [Contacts](#contacts)
  - [Table of Content](#table-of-content)
  - [Install](#install)
  - [Implemented functions](#implemented-functions)
    - [LINQ functions](#linq-functions)
    - [Custom functions](#custom-functions)
  - [Not implemented functions](#not-implemented-functions)
    - [LINQ functions](#linq-functions-1)
    - [Py-Linq functions](#py-linq-functions)
  - [Contributing and info for developers](#contributing-and-info-for-developers)
  - [Full documentation](#full-documentation)

## Install

For all specific commands to this project, we use [just](https://github.com/casey/just).
**You need to install it.**

After you can install the dependencies:

```bash
$ just install
pwd
/home/uchosson/Documents/py-linq-sql
poetry install --no-dev --remove-untracked
Installing dependencies from lock file
Warning: The lock file is not up to date with the latest changes in pyproject.toml.
You may be getting outdated dependencies. Run update to update them.

No dependencies to install or update

Installing the current project: py-linq-sql (0.109.0)
```

And if you need to develop the project, install development dependencies:

```bash
$ just install-all
pwd
/home/uchosson/Documents/py-linq-sql
poetry install --remove-untracked
Installing dependencies from lock file
Warning: The lock file is not up to date with the latest changes in pyproject.toml.
You may be getting outdated dependencies. Run update to update them.

No dependencies to install or update

Installing the current project: py-linq-sql (0.109.0)
npm install

up to date, audited 8 packages in 793ms

1 package is looking for funding
  run `npm fund` for details

found 0 vulnerabilities
sudo npm install markdownlint-cli2 --global

changed 36 packages, and audited 37 packages in 2s

8 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
```

and the pre-commit dependencies:

```bash
$ just preinstall
pwd
/home/uchosson/Documents/py-linq-sql
pre-commit clean
Cleaned /home/uchosson/.cache/pre-commit.
pre-commit autoupdate
Updating https://github.com/pre-commit/pre-commit-hooks ...
[INFO] Initializing environment for https://github.com/pre-commit/pre-commit-hooks.
already up to date.
Updating https://github.com/pre-commit/pre-commit-hooks ... already up to date.
Updating https://github.com/pycqa/isort ...
[INFO] Initializing environment for https://github.com/pycqa/isort.
already up to date.
Updating https://github.com/ambv/black ...
[INFO] Initializing environment for https://github.com/ambv/black.
already up to date.
Updating https://github.com/codespell-project/codespell ...
[INFO] Initializing environment for https://github.com/codespell-project/codespell.
already up to date.
Updating https://github.com/sqlfluff/sqlfluff ...
[INFO] Initializing environment for https://github.com/sqlfluff/sqlfluff.
updating 1.1.0 -> 1.2.1.
Updating https://github.com/pycqa/flake8 ...
[INFO] Initializing environment for https://github.com/pycqa/flake8.
already up to date.
Updating https://github.com/DavidAnson/markdownlint-cli2 ...
[INFO] Initializing environment for https://github.com/DavidAnson/markdownlint-cli2.
already up to date.
pre-commit install --hook-type pre-merge-commit
pre-commit installed at .git/hooks/pre-merge-commit
pre-commit install --hook-type pre-push
pre-commit installed at .git/hooks/pre-push
pre-commit install --hook-type post-rewrite
pre-commit installed at .git/hooks/post-rewrite
pre-commit install-hooks
[INFO] Installing environment for https://github.com/pre-commit/pre-commit-hooks.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
[INFO] Installing environment for https://github.com/pycqa/isort.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
[INFO] Installing environment for https://github.com/ambv/black.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
[INFO] Installing environment for https://github.com/codespell-project/codespell.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
[INFO] Installing environment for https://github.com/sqlfluff/sqlfluff.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
[INFO] Installing environment for https://github.com/pycqa/flake8.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
[INFO] Installing environment for https://github.com/DavidAnson/markdownlint-cli2.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

## Implemented functions

### LINQ functions

[LINQ documentation](https://docs.microsoft.com/fr-fr/dotnet/api/system.linq.enumerable?view=net-6.0)

All function make before an `.execute()` are executed by the database server.

MDPA = MagicDotPathAggregate
<!-- markdownlint-disable MD013 -->
|Method Name           |Description                                                          |Output        |
|:---------------------|:--------------------------------------------------------------------|:-------------|
|all                   |Return True if all elements match the predicate.                     |SQLEnumerable |
|any                   |Return True if any elements match the predicate.                     |SQLEnumerable |
|avg                   |Aggregation function to get the average of the predicate.            |MDPA          |
|contains              |Return True if at least one element match the predicate.             |SQLEnumerable |
|concat                |Aggregation function to concat a predicate.                          |MDPA          |
|count                 |Return the number of line in a table.                                |SQLEnumerable |
|count                 |Aggregation function to count a predicate.                           |MDPA          |
|distinct              |Return all elements that are not duplicate.                          |SQLEnumerable |
|element_at            |Return the element at the specific index.                            |SQLEnumerable |
|element_at_or_default |Return the element at the specific index or None if index > len.     |SQLEnumerable |
|except                |Returns all elements except elements from another SQLEnumerable.     |SQLEnumerable |
|first                 |Return the first element match the predicate.                        |SQLEnumerable |
|first_or_default      |Return the first element match the predicate or None if none match.  |SQLEnumerable |
|group_by              |Return the selection group by a predicate.                           |SQLEnumerable |
|group_join            |Return the join between 2 selections group by a predicate.           |SQLEnumerable |
|intersect             |Return the intersection between 2 selections.                        |SQLEnumerable |
|join                  |Return the join between 2 selections.                                |SQLEnumerable |
|last                  |Return the last element match the predicate.                         |SQLEnumerable |
|last_or_default       |Return the last element match the predicate or None if none match.   |SQLEnumerable |
|max                   |Return the max element.                                              |SQLEnumerable |
|max                   |Aggregate function to get the max of predicate.                      |MDPA          |
|min                   |Return the min element.                                              |SQLEnumerable |
|min                   |Aggregate function to get the min of predicate.                      |MDPA          |
|order_by              |Return the selection order by key(s).                                |SQLEnumerable |
|order_by_descending   |Return the selection order by descending by key(s).                  |SQLEnumerable |
|select                |Return a selection of elements.                                      |SQLEnumerable |
|single                |Return the only element match the predicate.                         |SQLEnumerable |
|single_or_default     |Return the only element match the predicate or None if many matches. |SQLEnumerable |
|skip                  |Return the selection minus _X_ first elements.                       |SQLEnumerable |
|skip_last             |Return the selection minus _X_ last elements.                        |SQLEnumerable |
|sum                   |Aggregation function to get the sum of a predicate.                  |MDPA          |
|take                  |Return _X_ first element of the selection.                           |SQLEnumerable |
|take_last             |Return _X_ last element of the selection.                            |SQLEnumerable |
|union                 |Return the union between 2 selections.                               |SQLEnumerable |
|where                 |Return the selection with all elements match the predicate.          |SQLEnumerable |
<!-- markdownlint-enable MD013 -->

For more information see the [detailed documentation](https://py-linq-sql.readthedocs.io/en/latest/api/sqle/sqlenumerable/).

### Custom functions

<!-- markdownlint-disable MD013 -->
|Method Name   |Description                                         |Output                            |
|:-------------|:---------------------------------------------------|:---------------------------------|
|delete        |Delete data in a SQL table.                         |SQLEnumerable                     |
|execute       |Execute a request from an SQLEnumerable.            |Enumerable or int or bool or dict |
|insert        |Insert data in a SQL table.                         |SQLEnumerable                     |
|simple_insert |Insert data in a relationnal SQL table with kwargs. |SQLEnumerable                     |
|update        |Update data in a table.                             |SQLEnumerable                     |
<!-- markdownlint-enable MD013 -->

## Not implemented functions

### LINQ functions

|Method Name      |Description     |
|:----------------|:---------------|
|append           |Not implemented |
|default_if_empty |Not implemented |
|empty            |Not implemented |
|prepend          |Not implemented |
|range            |Not implemented |
|repeat           |Not implemented |
|reverse          |Not implemented |
|select_many      |Not implemented |
|skip_while       |Not implemented |
|take_while       |Not implemented |
|to_dictionary    |Not implemented |
|to_list          |Not implemented |
|zip              |Not implemented |

### Py-Linq functions

|Method Name|Description     |
|:----------|:---------------|
|add        |Not implemented |
|median     |Not implemented |

[Py-Linq link](https://viralogic.github.io/py-enumerable)

## Contributing and info for developers

- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [Our git workflow](https://py-linq-sql.readthedocs.io/en/latest/workflow/)

## Full documentation

- [Py-LINQ-SQL Documentation](https://py-linq-sql.readthedocs.io/en/latest/)
