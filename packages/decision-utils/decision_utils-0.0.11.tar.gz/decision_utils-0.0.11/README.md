# decision-utils

![Github CI](https://github.com/justmars/decision-utils/actions/workflows/ci.yml/badge.svg)

Preprocess frontmatter-formatted markdown with Philippine artifacts, statutes, citations.

## Installation

```sh
just start # install .venv
pip -V # check if within .venv (if not source .venv/bin/activate)
```

To make use of trained model _en_artifacts model_ in `decision-updater`, copy folder from `lexcorpora/packages/en_artifacts-0.0.0` then install it:

```sh
source .venv/bin/activate
pip install packages/en_artifacts-0.0.0 # installs spacy + model
```

> [!NOTE]
> Must install `en-artifacts` to use jupyter notebook cells that use `decision-updater`.

## pypi

Despite five packages, only `decision-utils` is usable as a third-party package, being a dependency of [citelaws-builder](https://github.com/justmars/citelaws-builder).

```sh
just dumpenv # pypi token
just publish # uses build / twine
```
