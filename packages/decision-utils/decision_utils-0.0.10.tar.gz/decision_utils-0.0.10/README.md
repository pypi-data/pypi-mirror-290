# decision-utils

![Github CI](https://github.com/justmars/decision-utils/actions/workflows/ci.yml/badge.svg)

> [!IMPORTANT]
> This is a dependecy of [citelaws-builder](https://github.com/justmars/citelaws-builder).

Preprocess frontmatter-formatted markdown with Philippine artifacts, statutes, citations.

This consists of five related packages:

1. `decision-fetcher`: extract raw html files from elibrary and create .md files
2. `decision-fetcher-fields`: defines fields prior to creation as markdown files
3. `decision-updater`: computationally expensive step modifying .md files
4. `decision-watcher`: with manual modifications to .md files, auto-format content
5. `decision-utils`: consumes modified .md files as pythonic objects

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

## Pypi

Despite five packages, only `decision-utils` is usable as a third-party package, being a dependency of [citelaws-builder](https://github.com/justmars/citelaws-builder).

```sh
just dumpenv # pypi token
just publish # uses build / twine
```

## Todo

> [!WARNING]
> Issues detected.

- [ ] Changed title position results in missing title: 69232
- [ ] No way to detect missing separate opinions yet:
  - [ ] 69232
  - [ ] 69257
  - [ ] 69256
  - [ ] 69115
- [ ] Debugging unparseable files

### Unparseable files

Detect errors via running `watcher` and editing a target file.

When trying to load a file with frontmatter, I get `yaml.scanner.ScannerError` indicating bad formatting found in the indicated lines. This usually means that the line is too long, e.g.

```yml
phrases: # bad since second line in the list can't be parsed
- Consolidated Building Maintenance, Inc. v. Asprec (Asprec), Philippine Pizza, Inc.
v. Cayetano (Cayetano)__vs__1
```

I have to edit manually:

```yml
phrases: # good
- Consolidated Building Maintenance, Inc. v. Asprec (Asprec), Philippine Pizza, Inc. v. Cayetano (Cayetano)__vs__1
```

## `decision-fetcher` + `decision-fetcher-fields`

`decision-fetcher` requires `decision-fetcher-fields` to extract data from sc e-library URL.

Converting the same to markdown files in a local directory.

First create an interim `decision_files.db`:

```sh
fetcher init-db
```

Populate this database with links via:

```sh
fetcher list-urls --start 1996 --end 2024
```

This searches the elibrary for decisions within the years indicated. Note that `--end` means it is excluded from the years list.

The collection of entries in the database serves as a directory.

This allows us to add markdown files to a local directory (skipping pre-existing files), e.g.: `/corpus-decisions`.

Create markdown files based on the database links via:

```sh
fetcher draft-files --start 2019
```

The files are considered **drafts** since these ought to be edited first.

### Edit opinion files

1. Go to the local directory where the files have been "drafted": e.g.: `/corpus-decisions`.
2. Using VSCode, search for markdown files prefixed with `**/a*.md` with regex string: `^label:`.
3. Alhtough some really do not have any others (being a per curiam opinion), most files need to be adjusted since the opinion authors have to be identified with their digits
4. Where it is warranted, create a separate `/opinion` folder on each decision

## `decision-watcher`

When modifying files in the /corpus-decisions directory (outside of this package), the markdown file cane be modified automatically with `decision_utils.update_content()`.

But in order for automation to work, the folder needs to be watched for manual changes.

```sh
watcher # uses default ../corpus-decisions
```

This component only needs to be run before a user edits the local markdown files directly.

## `decision-updater`

> [!IMPORTANT]
> Used when bulk modifying `/corpus-decisions` metadata.

This component of the package only needs to be run occasionally, specifically when any/all of the following libraries are updated:

1. `citation-utils`
2. `statute-utils`
3. `citation-title`
4. `lexcorpora` _en_artifacts model_

When these libraries are updated, the outputted metadata will vary.

Hence the need to re-run for consistency.

In addition, cleaning functions can be applied.

Delete `statute_files.db` (if it already exists) since this may have been previously updated via their original yaml files. The lack of a statutes database is remedied when program is run for the first time c/o _statute-utils_. The latter package is used to detect statute objects found within each opinion and add it to each opinion's metadata.

To run the updating step, open up a jupyter notebook:

```sh
# expects a range of years
updater --start 1901 --end 1902
```

> [!WARNING]
> Updating metadata takes a substantial amount of time, hence need to divide processing into stages, i.e. per year range. Furthermore, the entire `update_opinion()` method needs to be wrapped around a process function, i.e. `update_markdown_opinion_file()` since arbitrary text is involved and the complex regex patterns used by the above libraries might result in hanging processes, e.g. `am/97-9-282-rtc/1998-04-22/main-123.md` where it takes too long to determine citations (likely a recursive regex error), a timer of 5 seconds is used by `update_markdown_opinion_file`.

## `decision-utils`

See structured content based on file path:

```py
from decision_utils import Decision

file = next(Path().home().joinpath("corpus-decisions").glob("gr/**/2023*/main*"))
metadata = Decision.from_file(file)
meta.main_opinion.segments
meta.separate_opinions #
```

The `Decision` - consists of a single main opinion with optional separate opinions:

1. `Writer`- a justice who may pen an opinion (anonymous _per curiam_ opinions are marked as such)

2. `Voteline` - how the other justices voted in a decision re: each opinion

3. `Opinion` - authored by a writer, can consist of a _body_ (with or without an _annex_)

   1. `Body` - content of the opinion

      1. `Block` - a body division based on a natural or commented header in the body

         1. `Chunk` - a formula-based division of a block

            1. `Passage` - chunk divided into sentences _which end in footnotes_.

   2. `Annex` - if the body contains footnotes, the annex is the reference area of an opinion containing the value of footnotes; it can can be subdivided into the area of each footnote

      1. `Footnote`

4. `Artifact` - each opinion will contain relevant certain phrases/entities divided into overlapping `ArtifactCategory`:

   1. For "citation"-based artifacts, a `citation` may consist of `vs`, `docket`, and `ref` (aside from the date).

   2. For "statute"-based artifacts, a `statute` may consist of `unit`, `rule`, (aside from the date).

> [!NOTE]
> Based on block-chunk setups, it may be possible to use FTS only on `ruling` `issue` `preface` `fallo` chunks as searchable segments that can also have embeddings.

### Blocks

- [x] Heading includes footnote

      ## Regional Trial Court[^1]

- [ ] Heading may be prefixed by a Roman Numeral, Number, and/or Letter

      ## I. Facts

- [ ] Heading includes parenthesis

      ## Regional Trial Court (Sample Text)

### Chunks

1. Blocks can only create proper chunks if the block is formatted properly
2. For instance if an ` xxx ` is in between blockquotes and not preceded by a `>` indicator, this will result in multiple chunks rather than a single one.

    >

    xxx xxx xxx

    > As we outlined above, **a temporary total disability only becomes permanent when so declared by the company physician within the periods he is allowed to do so, or upon the expiration of the maximum 240-day medical treatment period without a declaration of either fitness

### Todo

- [ ]`^\*+[^\*]{1,60}(?!\*)\n` detect short strings that ought to be converted into headings
- [ ] The `formatter()` needs to exclude indented enumerations in removing pre-line spaces
- [ ] Create tests per component
