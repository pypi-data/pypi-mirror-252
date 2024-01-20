# Repos

[![PyPI version](https://badge.fury.io/py/repos.svg)](https://badge.fury.io/py/repos)
[![Unstable package](https://img.shields.io/badge/_Unstable_package_-_This_code_is_a_work_in_progress_-red)](https://semver.org)


Manage your git repos.


## Install

    pip install repos


## Usage

Inside a directory with several git repos run:

    $ repos
    Repos in /Users/hello/repos

    STATUS              NAME                            BRANCH
    ────────────────    ────────────────────────────    ──────────
    •   •  1↑  •  •     this-is-a-ahead-repo              master
    •  1↓   •  •  •     this-is-a-behind-repo             master
    •   •   •  •  •     this-is-a-clean-repo              master
                        this-is-a-directory/
    1±      ⚑  •  •     this-is-a-dirty-repo              master
    •   ⚑         •     this-repo-has-no-remotes          master
    •   •   •  •  3     this-repo-has-three-branches      branch-3
    •   •   •  2  •     this-repo-has-two-remotes         master

            1 directories
            1 without a remote ⚑
            1 without upstream ⚑
            1 changed
            1 behind
            1 ahead
            4 clean

To check all available commands:

```
$ repos help
NAME
    repos —  Manages your git repos

USAGE
    repos                       # Lists all repos in text format
    repos export --json         # Exports all repos as json
    repos export --yaml         # Exports all repos as yaml
    repos show REPO             # Shows the repo details
    repos save                  # Commits local changes
    repos push                  # Pushes up to the upstream
    repos pull                  # Pulls from the upstream
    repos sync                  # Pull from the upstream and pushes up
    repos help                  # Shows this help
    repos version               # Prints the current version
```


## Todos

- [ ] Show by default only repos with issues.

- [ ] Show all with the `-a | --all` flag.

- [ ] Add `clone <url>` command to clone a git repo.

- [ ] Add `export [file]` command to dump all repos, branches
      and remotes into a file (by default `repos.yaml`).

- [ ] Add `import [file]` command to clone repos, branches
      and remotes from a file (by default `repos.yaml`).

- [x] Add `config [repo1,repo2] [key] [value]` subcommand to
      store settings in the `.git/repo.yaml` file.

- [ ] Add `save [repo1,repo2]` subcommand to commit all
      changes.

- [ ] Add `pull [repo1,repo2]` subcommand to pull all the
      latest commits from the upstream.

- [ ] Add `sync [repo1,repo2]` subcommand to commits all
      changes, pull the latest commits, and push local commits
      to the upstream.

- [ ] Code the `enabled` config to turn off all other configs.

- [ ] Customise the colours via env vars.
