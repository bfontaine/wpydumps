# WPyDumps

**WPyDumps** is a Python module to work with [dumps of Wikipedia][dumps].

It allows one to parse and extract relevant information from dump files without un-compressing them on-disk.

It works with (at least) these dumps:

- `pages-meta-history….xml-….7z` (“All pages with complete edit history”)
- `pages-meta-current.xml.bz2`

[dumps]: https://dumps.wikimedia.org

## Install

    pip install wpydumps

If you have issues with `libarchive`, see [its documentation](https://github.com/dsoprea/PyEasyArchive?tab=readme-ov-file#notes).

## Usage

The parser uses [SAX][] to read the files as a stream. It takes a reader or a filename and a page callback function. It
parses the file and call that function with each page.

Pages are represented as `wpydumps.model.Page` objects. They include the pages’ details as well as their
revisions (`wpydumps.model.Revision`). Each revision holds a reference to its contributor (`wpydumps.model.Contributor`).

```python3
import wpydumps as p


def simple_page_callback(page):
    print(page.title)


# parse from a local archive
p.parse_pages_from_archive_filename("myfile.7z", simple_page_callback)

# parse from an uncompressed file
with open("myfile") as f:
    p.parse_pages_from_reader(f, simple_page_callback)
```

Revisions always have a `text_length` and `diff_length` `int` attributes. You may drop the text content by
passing `keep_revisions_text=False` to the parser.

[SAX]: https://docs.python.org/3.6/library/xml.sax.html

### Examples

```python3
from wpydumps import parse_pages_from_archive_filename


def page_callback(page):
    pass  # do something with the page


# use the appropriate filename
parse_pages_from_archive_filename("frwiki-20190901-pages-meta-history1.xml-p3p1630.7z", page_callback)
```

#### Print all pages and their number of revisions

```python3
def page_callback(page):
    print(page.title, len(page.revisions))
```

#### Print all pages and their number of contributors

```python3
def page_callback(page):
    contributors = set()
    for rev in page.revisions:
        contributors.add(rev.contributor.username or rev.contributor.ip)

    print("%s: %d contributors" % (page.title, len(contributors)))
```
