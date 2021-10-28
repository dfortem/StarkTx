<h1 align='center' style='border-bottom: none'>
  <p>StarkTx - StarkNet transactions decoder </p>
</h1>

<p align="center">
<a target="_blank">
    <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg" alt="Python">
</a>
<a target="_blank">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black">
</a>
</p>

## Live version

Live version of StarkTx is available here [http://starktx.info/](http://starktx.info/), with source code released
here [StarkWare](https://github.com/TokenFlowInsights/StarkWare)

## Backend Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.


## Backend local development

* Start the stack with Docker Compose:

```bash
docker-compose up -d --build
```

## Backend local development, additional details

### General workflow

By default, the dependencies are managed with [Poetry](https://python-poetry.org/), go there and install it.

From `./stark_tx/app/` you can install all the dependencies with:

```console
$ poetry install
```

Then you can start a shell session with the new environment with:

```console
$ poetry shell
```

Next, open your editor at ./stark_tx/app/ (instead of the project root: ./), so that you see an ./app/ directory with
your code inside. That way, your editor will be able to find all the imports, etc. Make sure your editor uses the
environment you just created with Poetry.
