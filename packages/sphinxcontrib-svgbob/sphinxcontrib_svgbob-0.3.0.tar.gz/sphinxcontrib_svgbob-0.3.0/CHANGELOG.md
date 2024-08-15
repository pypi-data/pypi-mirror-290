# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## [Unreleased]
[Unreleased]: https://github.com/althonos/sphinxcontrib-svgbob/compare/v0.3.0...HEAD


## [v0.3.0] - 2024-08-14
[v0.3.0]: https://github.com/althonos/sphinxcontrib-svgbob/compare/v0.2.1...v0.3.0

### Added
- Support for Python 3.12 ([#4](https://github.com/sphinx-contrib/svgbob/issues/4), by [@maffoo](https://github.com/maffoo)).

### Changed
- Bumped `svgbob` dependency to `v0.7.2`.

### Removed
- `enhance_circuitries` and `merge_line_with_shapes` directives.


## [v0.2.1] - 2022-11-10
[v0.2.1]: https://github.com/althonos/sphinxcontrib-svgbob/compare/v0.2.0...v0.2.1

### Fixed
- Allow using Unicode box characters instead of ASCII ([#2](https://github.com/sphinx-contrib/svgbob/issues/2)).

### Added 
- Support for Python 3.11.


## [v0.2.0] - 2022-09-30
[v0.2.0]: https://github.com/althonos/sphinxcontrib-svgbob/compare/v0.1.1...v0.2.0

### Changed
- Bumped `pyo3` dependency to `v0.17.1`.
- Bumped `svgbob` dependency to `v0.6.7`.
- Use GitHub Actions instead of AppVeyor to build and test wheels for Windows.

### Added
- Support for Python 3.10 ([#1](https://github.com/sphinx-contrib/svgbob/issues/1)).

### Removed
- Support for Python 3.6.


## [v0.1.1] - 2021-04-14
[v0.1.1]: https://github.com/althonos/sphinxcontrib-svgbob/compare/v0.1.0...v0.1.1

### Fixed
- Wrong project name in `setup.cfg`.
- Invalid branch name in URL of AppVeyor status badge in `README.md`.


## [v0.1.0] - 2021-04-14
[v0.1.0]: https://github.com/althonos/sphinxcontrib-svgbob/compare/a46aa6e...v0.1.0

Initial release.
