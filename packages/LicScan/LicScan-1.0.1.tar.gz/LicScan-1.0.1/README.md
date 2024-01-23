![PyPI - Downloads](https://img.shields.io/pypi/dm/licscan) ![PyPI - License](https://img.shields.io/badge/license-UPL_v1.0-green) [![Live Demo](https://img.shields.io/badge/live-demo-blue)](https://ospyp.github.io/licscan)

# LicScan

A python package to check the licenses of your dependencies. Automate your license compliance! Fast, free, and open-sourced!

## [NEW] Live Demo

Our NEW live demo is less accurate but runs on the web. [Try it out...](https://ospyp.github.io/licscan)

## Install

```
pip install licscan
```

## Usage

Use the default list of licenses:

```bash
licscan -f requirements.txt
```

Or a custom list:

```bash
licscan -f requirements.txt -a MIT ISC Apache
```

## License

UPL v1.0.

---

A initiative of [Open Source PYthon Packages](https://github.com/ospyp).

<a href="https://github.com/ospyp"><img width="100" src="https://raw.githubusercontent.com/ospyp/ospyp/main/logo.svg"></a>
