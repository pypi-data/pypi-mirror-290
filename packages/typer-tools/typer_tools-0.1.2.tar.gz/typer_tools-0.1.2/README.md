# Typer Tools

> Simple tools for Typer CLI

```bash
pip install typer-tools
```

## Options Anywhere

Typer does not support making `cli -v export` and `cli export -v` work the same way. But we can handle:

```python
from typer_tools import option

Verbose = option(False, '-v', '--verbose') # drop-in replacement for typer.Option

@app.callback()
def main(verbose: bool = Verbose):
  ...

@app.command()
def export(verbose: bool = Verbose):
  ...
```

## Dependency Injection

Typer does not support dependency injection. But we can handle:

```python
from typer_tools import Dependency

def parse_client(
  host: str = typer.Option(..., '--host', help='HTTP host'), # or our own `option`, plain better
  port: int = typer.Option(80, '--port', help='HTTP port'),
  token: str = typer.Option(..., '--token', help='Access token')
) -> Client:
  ...

dep = Dependency(parse_client)

@typer.command()
@dep.inject
def main(some_option: str, client: Client = dep.Depends()):
  ...
```

