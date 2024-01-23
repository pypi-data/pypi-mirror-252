# GhTrend

<img src="./docs/GhTrend.gif" width="360" />


Request and parse Github trending page.

**Usage**:

```console
$ get-trend [OPTIONS] [DATE_RANGE] [OUT_FILE]
```

**Arguments**:

* `[DATE_RANGE]`: Choose from: daily, weekly, monthly
* `[OUT_FILE]`: Enter the filepath csv to be stored at

**Options**:

* `--quiet / --no-quiet`: [default: no-quiet]
* `--version / --no-version`
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Dependency:**

- requests
- BeautifulSoup4
- typer

