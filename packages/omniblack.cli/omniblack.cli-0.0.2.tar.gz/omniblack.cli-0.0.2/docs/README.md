# Omniblack CLI

Omniblack CLI provides an easy way to create CLI applications.


## Example Usage

Python Code:

```python
from omniblack.cli import CLI
from .model import model

app = CLI(model)

@app.command
def hello(name='world'):
    """
    Say hello.

    Args:
        name: The name to say hello to.
    """

    print(f'Hello {name}!')
```

When {code}`app` is exposed as a console script:

```console
>>> hello
Hello world!

>>> hello user
Hello user!
```
