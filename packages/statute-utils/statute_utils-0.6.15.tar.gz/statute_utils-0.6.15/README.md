# statute-utils

![Github CI](https://github.com/justmars/statute-utils/actions/workflows/ci.yml/badge.svg)

Philippine statutory law pattern matching and unit retrieval; utilized in [LawSQL dataset](https://lawsql.com).

## Documentation

See [documentation](https://justmars.github.io/statute-utils).

## Fetch

See [notebook](notebooks/web.ipynb) on sample fetch process.

## Create interim db

Create an sqlite database which lists statutes found in a given directory, e.g. `../corpus-statutes`

```sh
source .venv/bin/activate
builder init-db --folder ../corpus/statutes
```

This is a wrapper around the `setup_local_statute_db()` function.

## Development

TODO: If statute-utils is imported into a third-party library, it needs to include the /templates folder which does not include any python files at present

must add statute_utils/templates, add a `MANIFEST.IN` to package this properly

## Todo

- [ ] Better unit segmentation.
- [x] Detect Family Code, see gr/227728/2022-09-28/main-193.md
- [ ] Detect Penal Code with `REV. PEN. CODE, Art. 308:`, gr/224316/2021-11-10/main-180.md
- [ ] Provision matching

## Changes

1. em / strong no longer with label
2. Need to add href on <a.label/>
3. `span.par-branch` converted to `a.par-branch`
4. <li#id> and <span#id> changed to <a[data-slug]/>
