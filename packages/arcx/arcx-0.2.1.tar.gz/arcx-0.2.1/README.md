# arcX - Archive, Rm & Clean toolboX

ArcX is a versatile toolbox designed to streamline data management by automating key tasks. Whether you're handling
experiment outputs or maintaining clean directories, ArcX simplifies the process with a range of powerful tools.

* **Archiving**: Seamlessly archive Oceanic experiment outputs using a flexible YAML configuration file. ArcX takes care
  of organizing and storing your data without manual intervention.
* **Safe File Removal**: Efficiently remove files that already have a local copy. ArcX ensures that only unnecessary
  files are deleted, safeguarding important data.
* **Comprehensive Directory Cleaning**: Clean multiple directories with a single command. ArcX offers various cleaning
  options and leverages a YAML configuration file to specify exactly what to delete and how to do it.

## Installation

### Via pip

```shell
pip install arcx
```

### Via conda/mamba

```shell
mamba install arcx
```

## Usage

```shell
Usage: arcx [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  rolling
  saferm
  update-md5
```

## Rolling

To keep a directory under rolling, use the command:

```shell
Usage: cli.py rolling [OPTIONS]

Options:
  -c, --config PATH  [required]
  --dry-run          Dry run mode.
  -d, --debug        Enable debug mode.
  --help             Show this message and exit.
```

### Rolling Configuration File

Here a template of a rolling configuration file:

```yaml
- !CleanPath
    path: $PATH_UNDER_ROLLING
    fmt: ????????   # YYYYMMDD
    safe:
        to_keep: X
        reference_paths:
            - <REF1>
            - <REF2>
    conditional:
        to_keep: Y
        expected_files:
            - file.exe
            - tmp.nc
    force:
        to_keep: Z
```

let's comment each section.

<details>
  <summary>
    <b>CleanPath object</b>
  </summary>

With this, we start to declare a list of !CleanPath objects with two mandatory attributes:

```yaml
- !CleanPath
    path: $PATH_UNDER_ROLLING
    fmt: ????????   # YYYYMMDD
```

* `path`: it's the path to keep under rolling
* `fmt`: it's a string bash that represent the format of file/dir to delete. It can contains jolly characters `?` or `*`

</details>

<details>
  <summary>
    <b>Safe</b>
  </summary>

```yaml
  safe:
      to_keep: X
      reference_paths:
          - <REF1>
          - <REF2>
```

* `safe`: means for safe rolling, which means **delete a file only if an identical local copy already exists**
* `to_keep`: how much dir/file to not include in the rolling
* `reference_paths`: a list of path where to find if a local copy already exists

To consider that the safe mode doesn't remove the dir under rolling.
</details>

<details>
  <summary>
    <b>Conditional</b>
  </summary>
#### Conditional

```yaml
  conditional:
      to_keep: Y
      expected_files:
          - file.exe
          - tmp.nc
```

* `conditional`: specify to remove a dir if some conditions are meet
* `to_keep`: how much dir/file to not include in the rolling
* `expected_files`: specify the exact list of files expected to find in rolling path to trigger the rm operations. The
  filename can contains jolly character `?` and `*`

</details>

<details>
  <summary>
    <b>Force</b>
  </summary>

```yaml
    force: # optional
        to_keep: Z
```

* `force`: Enable path rm without any check
* `to_keep`: how much dir/file to not include in the rolling

</details>

---

## Update md5 dir

A requirement to safe clean, is to compute in advance the md5 of all files in the rolling path using the command:

```shell
update-md5 [OPTIONS]

Options:
  -p, --path PATH  [required]
  -d, --debug      Enable debug mode.
  --help           Show this message and exit.
```

The command will create in the directory a file called `.dir_md5.txt` with the following structure:

```txt
md5hash filename1
md5hash filename2
```

---

## Safe Clean

Safe Rm command is the equivalent of safe rm rolling section: it removes files from **clean path** only if exists an
identical copy in **keep path**

```shell
Usage: cli.py saferm [OPTIONS]

Options:
  --keep PATH    [required]
  --clean PATH   [required]
  -f, --force    Delete files without confirm request
  -d, --dry-run  Disable file removal
  -d, --debug    Enable debug mode.
  --help         Show this message and exit.
```
