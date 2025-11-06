# Columen LaTeX Package

Columen provides the `columen` environment, which distributes list-like
content across multiple columns while ensuring that individual items are not
split between columns.

## Build Demo Document

```bash
l3build unpack
latexmk -pdf test.tex
```

## Install

```bash
l3build unpack
latexmk -pdf columen.dtx
```

Or manually:

```bash
tex columen.ins && latexmk -pdf columen.dtx
```
