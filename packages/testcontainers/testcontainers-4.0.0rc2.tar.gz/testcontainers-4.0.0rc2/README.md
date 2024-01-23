# Testcontainers Python

`testcontainers-python` facilitates the use of Docker containers for functional and integration testing. 

for more information, see [the docs][readthedocs].

[readthedocs]: https://testcontainers-python.readthedocs.io/en/latest/

## Getting Started

```python
>>> from testcontainers.postgres import PostgresContainer
>>> import sqlalchemy

>>> with PostgresContainer("postgres:9.5") as postgres:
...     engine = sqlalchemy.create_engine(postgres.get_connection_url())
...     result = engine.execute("select version()")
...     version, = result.fetchone()
>>> version
'PostgreSQL 9.5...'
```

The snippet above will spin up a postgres database in a container. The `get_connection_url()` convenience method returns a `sqlalchemy` compatible url we use to connect to the database and retrieve the database version.
