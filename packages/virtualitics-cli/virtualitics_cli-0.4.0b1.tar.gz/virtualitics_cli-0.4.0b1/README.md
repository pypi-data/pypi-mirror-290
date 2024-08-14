# `vaip`

**Usage**:

```console
$ vaip [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--verbose / --no-verbose`: [default: no-verbose]
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `build`: Builds a VAIP App Python wheel file.
* `config`: Used to create a configuration file.
* `deploy`: Deploys the VAIP App to a VAIP Instance.
* `init`: Initializes a VAIP app structure.
* `publish`: Publishes a VAIP App to other users.
* `rollback`: Roll back a deployment.
* `use-context`: Used to set the context.

## `vaip build`

Builds a VAIP App Python wheel file

**Usage**:

```console
$ vaip build [OPTIONS]
```

**Options**:

* `-y, --yes`: Build a wheel using pyproject.toml in current directory?  [required]
* `--help`: Show this message and exit.

## `vaip config`

Used to create a configuration file in ~/.virtualitics/config.conf (DEFAULT_CONTEXT_PATH)
Requires a friendly name of a VAIP instance, host of a VAIP instance, and an API token.

**Usage**:

```console
$ vaip config [OPTIONS]
```

**Options**:

* `-N, --name TEXT`: User-specified friendly name for a given VAIP instance, i.e. predict-dev  [required]
* `-H, --host TEXT`: Backend hostname for a given VAIP instance, i.e. https://predict-api-prd.virtualitics.com  [required]
* `-T, --token TEXT`: API token used to verify the user’s access to the given VAIP instance  [required]
* `-U, --username TEXT`: Username associated with API token  [required]
* `--help`: Show this message and exit.

## `vaip deploy`

Deploys the VAIP App to a VAIP Instance

**Usage**:

```console
$ vaip deploy [OPTIONS]
```

**Options**:

* `-fr, --force-reinstall`: Force reinstall of the module.
* `-f, --file TEXT`: Absolute path to the wheel file if not in current project /dist
* `--help`: Show this message and exit.

## `vaip init`

Initializes a VAIP app structure, and a pyproject.toml file that looks like this:
[project]
name = "vaip-apps"
version = "0.1.1"
description = "vaip example apps"
authors = [{name = "Virtualitics Engineering", email = "engineering@virtualitics.com"}]
license = {text = "MIT"}
requires-python = ">= 3.11"

[build-system]
requires = ["setuptools >= 61.0"]
build-backend = "setuptools.build_meta"

**Usage**:

```console
$ vaip init [OPTIONS]
```

**Options**:

* `-n, --project-name TEXT`: Name for the VAIP App (No spaces or special chars besides '_')  [required]
* `-v, --version TEXT`: Version for the VAIP App (0.1.0)  [required]
* `-d, --description TEXT`: Description for the VAIP App  [required]
* `-a, --authors TEXT`: Authors for the VAIP App (email)  [required]
* `-l, --licenses TEXT`: Licenses for the VAIP App  [required]
* `--help`: Show this message and exit.

## `vaip publish`

Publishes a VAIP App to other users in your group

**Usage**:

```console
$ vaip publish [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `vaip rollback`

Roll back the deployment of the most recently deployed VAIP App

**Usage**:

```console
$ vaip rollback [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `vaip use-context`

Used to set the context referenced in the config file

**Usage**:

```console
$ vaip use-context [OPTIONS] NAME
```

**Arguments**:

* `NAME`: The name of a previously configured context referenced in the configuration file  [required]

**Options**:

* `--help`: Show this message and exit.
