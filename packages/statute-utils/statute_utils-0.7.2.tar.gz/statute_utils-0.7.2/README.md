# statute-utils

![Github CI](https://github.com/justmars/statute-utils/actions/workflows/ci.yml/badge.svg)

Philippine statutory law pattern matching, unit retrieval, database creation and template creation.

Utilized in [LawSQL dataset](https://lawsql.com).

## Documentation

See [documentation](https://justmars.github.io/statute-utils).

## Fetch

See [notebook](notebooks/web.ipynb) on sample fetch process.

## Development

> [!NOTE]
> If `statute-utils` is imported into a third-party library, it needs to include the `/templates` folder. This does not include any `*.py` files and is thus included in the `MANIFEST.IN`.

## Todo

- [ ] Better unit segmentation.
- [x] Detect Family Code, see gr/227728/2022-09-28/main-193.md
- [ ] Detect Penal Code with `REV. PEN. CODE, Art. 308:`, gr/224316/2021-11-10/main-180.md
- [ ] Provision matching
