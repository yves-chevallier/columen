# Column Spread LaTeX Package

This package provides the `columnspread` environment, which allows you to
distribute content across multiple columns while ensuring that items are not
split between columns.

## Install

```bash
l3build unpack
latexmk -pdf columnspread.dtx
```

Or manually:

```bash
tex columnspread.ins && latexmk -pdf columnspread.dtx
```
