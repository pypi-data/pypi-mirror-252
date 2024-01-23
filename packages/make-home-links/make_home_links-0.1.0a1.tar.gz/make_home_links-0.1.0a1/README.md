# make-home-links readme

Simplify your shell setup by making symlinks to your home folder.

It takes a TOML file and creates symlinks from your checkout.

## Prerequisites

* `pipx` or just `pip3`

## Installation

One of:

* `pipx install make-home-links`
* `pip install --user make-home-links`

Upgrading:

* `pipx upgrade make-home-links`
* `pip install --user -U make-home-links`

After installation, `make-home-links` command should become available:

```shell
make-home-links --help
make-home-links --version
```

## Development

The project uses [`hatch`](https://hatch.pypa.io/) behind the scenes.

### How to use

```shell
# reformat the code
make fmt

# run the cli
hatch run cli

# run the cli version
hatch run cli --version

# run the cli help
hatch run help
hatch run cli --help

# run mypy
hatch run types:check

# run tests
hatch run test
hatch run test -k usual_pytest_flags -m my_marker

# go to the dev shell
hatch shell

# build the distribution
hatch build
```

### Increase version
```shell
hatch version <new_version>
```

### Publishing

#### Test publishing

Create `.env.test` with contents (when doing first ever release, you will not be able to constrain the token to project -- create one for entire account and then switch to project-based token):
```shell
export HATCH_INDEX_USER=__token__
# token from "API tokens" of https://test.pypi.org/manage/account/
export HATCH_INDEX_AUTH=pypi-...
```

then publish to the testing PyPI:

```shell
hatch version <new_version>
source .env.test
hatch publish -r test -y
```

#### Publishing to prod

Create `.env.prod` with contents (when doing first ever release, you will not be able to constrain the token to project -- create one for entire account and then switch to project-based token):
```shell
export HATCH_INDEX_USER=__token__
# token from "API tokens" of https://pypi.org/manage/account/
export HATCH_INDEX_AUTH=pypi-...
```

then publish to the testing PyPI:

```shell
# maybe also: hatch version <new_version>
source .env.prod
hatch publish -r main -y
```

See also [`hatch publish`](https://hatch.pypa.io/1.9/publish/) documentation.
