# CommonMark Website

This is a Python package that provides the command line utility `cmw`, where
`cwm` is short for "CommonMark Website".

It converts `.md` CommonMark files from the `input` directory into `.html` HTML
files in the `output` directory.

## Motivation

I wanted to create a script for generating nice looking simple static websites.

## Installation

    pip install cmw

## Usage

1. Put your `.md` CommonMark files in the `input` directory.
2. Run `cmw`
3. Serve the resulting `.html` HTML files as static content.

## Dependencies

- [mistletoe](https://github.com/miyuchina/mistletoe), one of the Python
  CommonMark implementations listed on the CommonMark spec
  [wiki](https://github.com/commonmark/commonmark-spec/wiki/List-of-CommonMark-Implementations)
