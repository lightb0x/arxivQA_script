#!/usr/bin/env python3
# removes the following:
# * link
# * image
# * reference | bibliography
# * ar5iv tail
# * appendix
from panflute import (
    run_filter,
    Str,
    Link,
    Image,
    Space,
    Span,
    Table,
    Plain,
    Header,
    BulletList,
    OrderedList,
    Inline,
    Block,
    Element,
)
import re

REF = False
TAIL = False


def flatten(elem):
    str_arr = []
    for e in elem.content:
        if isinstance(e, Str):
            str_arr.append(e.text)
        elif isinstance(e, Span):
            str_arr.append(flatten(e))
        elif isinstance(e, Space):
            str_arr.append(" ")
        elif hasattr(e, "content"):
            str_arr.append(flatten(e))
        else:
            break
    return "".join(str_arr)


def empty_like(elem):
    if isinstance(elem, Inline):
        return Str("")
    elif isinstance(elem, Block):
        return Plain()
    elif isinstance(elem, Element):
        return elem
    else:
        raise NotImplementedError(elem)


def trim_elements(elem, doc):
    global REF, TAIL

    if isinstance(elem, (Inline)) and TAIL:
        return empty_like(elem)
    elif type(elem) in [Link, Image]:
        if "\u25c4" == flatten(elem):
            TAIL = True
            return empty_like(elem)
        return Str(flatten(elem))
    elif type(elem) in [Header]:
        if re.search(
            r"^references?$|^bibliography$", flatten(elem).lower().strip()
        ):
            REF = True
            return empty_like(elem)
        if re.search(r"^appendix", flatten(elem).lower().strip()):
            TAIL = True
            return empty_like(elem)
        return elem
    elif type(elem) in [BulletList, OrderedList] and REF:
        REF = False
        return empty_like(elem)
    elif type(elem) in [Table]:
        return empty_like(elem)


def main(doc=None):
    return run_filter(trim_elements, doc=doc)


if __name__ == "__main__":
    main()
