
import os
import sys
from glob import glob
from typing import List
from xml.etree import ElementTree


def _indent_xml(xml, prefix=""):
    """
    Helper for ``build_index()``: Given an XML ``ElementTree``, modify it
    (and its descendents) ``text`` and ``tail`` attributes to generate
    an indented tree, where each nested element is indented by 2
    spaces with respect to its parent.
    """
    if len(xml) > 0:
        xml.text = (xml.text or "").strip() + "\n" + prefix + "  "
        for child in xml:
            _indent_xml(child, prefix + "  ")
        for child in xml[:-1]:
            child.tail = (child.tail or "").strip() + "\n" + prefix + "  "
        xml[-1].tail = (xml[-1].tail or "").strip() + "\n" + prefix


if len(sys.argv) != 2:
    print("Usage: ")
    print("build_collections.py <path-to-packages>")
    sys.exit(-1)

ROOT = sys.argv[1]


def write(file_name: str, coll_name: str, items: List[str]) -> None:
    """Write `collections/{file_name}.xml` with `file_name` as the collection `id`,
    `coll_name` as the collection `name`, and `items` as a list of collection items.

    :param file_name: The id of the collection, equivalent to the file name,
        e.g. `all-collections`.
    :type file_name: str
    :param coll_name: The name of the collection, e.g. `"All collections"`
    :type coll_name: str
    :param items: A list of names for the collection items, e.g. `["dnd", "coc", ...]`
    :type items: List[str]
    """
    et = ElementTree.Element("collection", id=file_name, name=coll_name)
    et.extend(ElementTree.Element("item", ref=item) for item in sorted(items))
    _indent_xml(et)
    with open(os.path.join(ROOT, "collections", file_name + ".xml"), "w", encoding="utf8") as f:
        f.write(ElementTree.tostring(et).decode("utf8"))


def get_id(xml_path: str) -> str:
    """Given a full path, extract only the filename (i.e. the nltk_data id)

    :param xml_path: A full path, e.g. "./packages/collections/coc.xml"
    :type xml_path: str
    :return: The filename, without the extension, e.g. "coc"
    :rtype: str
    """
    return os.path.splitext(os.path.basename(xml_path))[0]


# Write `collection/all-collections.xml` based on all files under /packages/collections
collections_items = [get_id(xml_path)
                 for xml_path in glob(f"{ROOT}/packages/collections/*.xml")]
write("all-collections", "All the collections", collections_items)

# Write `collection/all-ipm.xml` and `collection/all.xml` based on all files under /packages
all_items = [get_id(xml_path)
             for xml_path in glob(f"{ROOT}/packages/**/*.xml")]
write("all-ipm", "All packages available on ipm-server gh-pages branch", all_items)
write("all", "All packages", all_items)
