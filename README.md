# WPyDumps

**WpyDumps** is a Python module to work with [dumps of Wikipedia][dumps].

It allows one to parse and extract relevant information from dump files without
uncompressing them on-disk.

Only the “All pages with complete edit history” dump is supported.

[dumps]: https://dumps.wikimedia.org

## Usage
The parser uses [SAX][] to read the files as a stream. It takes a reader or a
filename and a page callback function. It parses the file and call that
function with each page.

Pages are represented as `wpydumps.model.Page` objects. They include the pages’
details as well as their revisions (`wpydumps.model.Revision`). Each revision
holds a reference to its contributor (`wpydumps.model.Contributor`).

```python3
import wpydumps.parser as p

def simple_page_callback(page):
    print(page.title)

# parse from a local archive
p.parse_pages_from_archive_filename("myfile.7z", simple_page_callback)

# parse from an uncompressed file
with open("myfile") as f:
    p.parse_pages_from_reader(f, simple_page_callback)
```

The text of each revision is dropped by default. You can disable this behavior
by passing `keep_revisions_text=True` to the parser function.

[SAX]: https://docs.python.org/3.6/library/xml.sax.html

### Examples
#### Print all pages and their number of revisions
```python3
from wpydumps.parser import parse_pages_from_archive_filename

def next_page(page):
    print(page.title, len(page.revisions))

# use the appropriate filename
parse_pages_from_archive_filename(
    "frwiki-20190901-pages-meta-history1.xml-p3p1630.7z",
    next_page)
```
