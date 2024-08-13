# J-RSYNC

J-Rsync is a python wrapper on unix rsync which uses a json configuration file to identify what to sync.
The tool was designed to solve the problem of recurrently synchronising many directories or files

Using a single command from crontab, it is possible to keep synchronized many paths.

![Python](https://img.shields.io/badge/Python->3.10-blue.svg)
[![Anaconda](https://img.shields.io/badge/conda->22.11.1-green.svg)](https://anaconda.org/)
[![Pip](https://img.shields.io/badge/pip->19.0.3-brown.svg)](https://pypi.org/project/pip/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://docs.pydantic.dev/latest/contributing/#badges)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)

---

## Installation

### Via PIP

```shell
pip install jrsync
```

### Via MAMBA/CONDA

```shell
mamba install jrsync
```

---

## Usage

```shell
usage: jrsync [-h] [--src-address SRC_ADDRESS] [--dst-address DST_ADDRESS]
              [--force] [-o OPTIONS] [-d--dry-run] [-V]
              config date_to_sync

Jrsync CLI

positional arguments:
  config                Json file containing sync information
  date_to_sync          Date in the format YYYYMMDD

options:
  -h, --help            show this help message and exit
  --src-host SRC_HOST
                        Source host. Example: user@remote
  --dst-host DST_HOST
                        Dest host. Example: user@remote
  --force               Allow to run multiple instance in the same moment
  -o OPTIONS, --options OPTIONS
                        Rsync options. use -o|--options= to avoid conflicts
                        with python args
  -d--dry-run           Enable dry run mode
  -V, --version         Print version and exit

```

### Remote synchronization

As default, the tool assumes that the path are local, but both source and destination path can be located on a remote
server.
**Be carefully that only one path can be remote**

#### Sync from remote to local

To synchronize files from remote to local computer:

```shell
jrsync <config> <date> --src-host user@remote
```

#### Sync from local to remote

To synchronize files from local to remote:

```shell
jrsync <config> <date> --dst-host user@remote
```

### Rsync options

As default, rsync runs with the following options:

```shell
-aP
```

They can be changed using `-o|--options`:

```shell
jrsync <config> <date> --options="-avug"
```

---

## Configuration File

### Attributes

The configuration file is a json file which contains a list of Jsync objects with the following attributes:

* `source_dir`: The directory on the source host from which files will be synchronized.
* `dest_dir`: The directory on the destination host where files will be synchronized.
* `day` (optional): Specifies the day of the week when the synchronization should be executed, following crontab
  convention. For example:
  * "*": Every day.
  * "0": Sunday.
  * "1": Monday, and so on.
* `src_host` (optional): The source host from which files will be synced. If not provided, files will be synced from the
  local machine. It can be provided as an argument from CLI
* `dst_host` (optional): The destination host where files will be synced. If not provided, files will be synced to the
  local machine. It can be provided as an argument from CLI
* `file_to_sync` (optional): A list of specific files to be synchronized. If this field is omitted, all files in
  source_dir will be synchronized.
  Conditional Behavior: If src_host is None, only files that exist in the source_dir will be synchronized.

### Dynamic Placeholders:

* `{{DATE}}`: Replaces with the value of date to sync passed as argument from CLI.
* `{{DATE + X}}`: Replaces with the date X days after date_to_sync.
* `{{DATE - X}}`: Replaces with the date X days before date_to_sync.
* Global Variables: You can also use global variables in this field.

### Example

```shell
[
{
    "source_dir": "/data/{{DATE - 1}}",
    "dest_dir": "/backup/{{DATE}}",
    "day": "*",
    "file_to_sync": ["important_file.txt", "logs/{{DATE - 1}}.log"]
}
]

```

---

## Authors

- Antonio Mariani (antonio.mariani@cmcc.it)

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

---

## Contact

For any questions or suggestions, please open an issue on the project's GitHub repository.
