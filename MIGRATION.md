# Migrating to QURI SDK

This guide is for migrating open PRs in quri-algo to [QURI SDK](https://github.com/qunasys/quri-sdk).

quri-algo has been migrated and is now part of the quri-sdk repo. Its structure is pretty much intact, but a few important changes have been made that impact migration. In this guide, we will first go over the migration itself and then address some of these changes.

## Migrating your branch

First clone quri-sdk

```
git clone https://github.com/qunasys/quri-sdk.git
```

or if you already are developing quri-sdk make sure you are on the latest commit on the main branch

```
git checkout main
git pull
```

Then add quri-algo as a remote and pull from your branch on quri-algo using the subtree strategy

```
git remote add -f qa https://github.com/qunasys/quri-algo.git
git pull -s subtree qa your_qa_branch
```

Specify whether to merge using a rebase or not if needed and continue sorting out potential conflicting files

## Potential merge conflicts

If you have made changes to `mypy.ini`, `poetry.lock`, `pyproject.toml` or any of the files in the `.git` folder they are likely to result in merge conflicts. Some quick things to keep in mind

- The configuration files `mypy.ini`, `poetry.lock`, `pyproject.toml` may cause merge conflicts, but they will most likely not be anything out of the ordinary, it is just that some changes to these were made during the migration itself
- The workflow files in `.git` were all moved to the `.git` in the root directory of quri-sdk. Since you are attempting a pull with the `subtree` strategy, if you have made any changes to the files here, git will not know whether they should exist or not. If you want your changes to be kept you will most likely have to manually edit the files in the quri-sdk `.git` directory and `git rm -r quri-algo/.git`.
- 
