# statute-utils

![Github CI](https://github.com/justmars/statute-utils/actions/workflows/ci.yml/badge.svg)

Philippine statutory law:

1. pattern matching
2. unit retrieval
3. database creation
4. template creation

## Documentation

See [documentation](https://justmars.github.io/statute-utils).

## Fetch

See [notebook](notebooks/web.ipynb) on sample fetch process.

## Development

> [!IMPORTANT]
> When modifying a database structure, consider three inter-related parts:
>
> 1. The pythonic object, e.g. `NamedTuple`
> 2. The representation of such in the prospective database
> 3. The documentation of the pythonic object found in `/docs`

Included folders:

> [!NOTE]
> If `statute-utils` is imported into a third-party library, it needs to include the `/templates` folder and `/sql` folder. These doe not include any `*.py` files and are thus referenced in `MANIFEST.IN`.

## Todo

- [ ] Better unit segmentation.
- [x] Detect Family Code, see gr/227728/2022-09-28/main-193.md
- [ ] Detect Penal Code with `REV. PEN. CODE, Art. 308:`, gr/224316/2021-11-10/main-180.md
- [ ] Provision matching
