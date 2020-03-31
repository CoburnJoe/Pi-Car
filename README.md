# Pi-Car
Raspberry Pi based smart car dashboard

Pre-Alpha codebase, to accompany an as-yet unpublished tutorial book.

# Developing/Configuring Environment
Make sure you have Python 3.x installed on your machine (use [pyenv](https://github.com/pyenv/pyenv)).

Install the dependencies with [pipenv](https://github.com/pypa/pipenv) (making sure to include dev and pre-release packages):

```bash
pipenv install --dev --pre
```

Configure your environment:

```bash
pipenv shell && export PYTHONPATH="$PWD"
```

Run the tests:

```bash
pytest
```

Or with logging:

```bash
pytest -s
```

Or tests with coverage:

```bash
pytest --cov=./
```

Format the code with [Black](https://github.com/psf/black):

```bash
black $PWD
```
# Running the App
Navigate into the `Pi-Car` directory:

```bash
cd Pi-Car
```

Configure your environment:

```bash
export FLASK_APP=Pi_Car.app
```

Then start Flask:

```bash
flask run
```