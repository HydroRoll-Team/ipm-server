#!/usr/bin/env python

"""
Build the collections package index.  Usage:

  build_pkg_index.py <path-to-packages> <base-url> <output-file>
"""

from xml.etree import ElementTree
import sys
xml_header = """<?xml version="1.0"?>
<?xml-stylesheet href="index.xsl" type="text/xsl"?>
"""


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


def build_index(root, base_url):
    """
    Create a new data.xml index file, by combining the xml description
    files for various packages and collections.  ``root`` should be the
    path to a directory containing the package xml and zip files; and
    the collection xml files.  The ``root`` directory is expected to
    have the following subdirectories::

      root/
        packages/ .................. subdirectory for packages
        collections/ ............... xml files for collections

    For each package, there should be two files: ``package.zip``
    (where *package* is the package name)
    which contains the package itself as a compressed zip file; and
    ``package.xml``, which is an xml description of the package.  The
    zipfile ``package.zip`` should expand to a single subdirectory
    named ``package/``.  The base filename ``package`` must match
    the identifier given in the package's xml file.

    For each collection, there should be a single file ``collection.zip``
    describing the collection, where *collection* is the name of the collection.

    All identifiers (for both packages and collections) must be unique.
    """
    # Find all packages.
    packages = []
    for pkg_xml, zf, subdir in _find_packages(os.path.join(root, "packages")):
        zipstat = os.stat(zf.filename)
        url = f"{base_url}/{subdir}/{os.path.split(zf.filename)[1]}"
        unzipped_size = sum(zf_info.file_size for zf_info in zf.infolist())

        # Fill in several fields of the package xml with calculated values.
        pkg_xml.set("unzipped_size", "%s" % unzipped_size)
        pkg_xml.set("size", "%s" % zipstat.st_size)
        pkg_xml.set("checksum", "%s" % md5_hexdigest(zf.filename))
        pkg_xml.set("subdir", subdir)
        # pkg_xml.set('svn_revision', _svn_revision(zf.filename))
        if not pkg_xml.get("url"):
            pkg_xml.set("url", url)

        # Record the package.
        packages.append(pkg_xml)

    # Find all collections
    collections = list(_find_collections(os.path.join(root, "collections")))

    # Check that all UIDs are unique
    uids = set()
    for item in packages + collections:
        if item.get("id") in uids:
            raise ValueError("Duplicate UID: %s" % item.get("id"))
        uids.add(item.get("id"))

    # Put it all together
    top_elt = ElementTree.Element("ipm_package_data")
    top_elt.append(ElementTree.Element("packages"))
    top_elt[0].extend(sorted(packages, key=lambda package: package.get("id")))
    top_elt.append(ElementTree.Element("collections"))
    top_elt[1].extend(
        sorted(collections, key=lambda collection: collection.get("id")))

    _indent_xml(top_elt)
    return top_elt


if len(sys.argv) != 4:
    print("Usage: ")
    print("build_pkg_index.py <path-to-packages> <base-url> <output-file>")
    sys.exit(-1)

ROOT, BASE_URL, OUT = sys.argv[1:]

index = build_index(ROOT, BASE_URL)
s = ElementTree.tostring(index)
s = s.decode("utf8")
out = open(OUT, 'w')
out.write(xml_header)
out.write(s)
out.write('\n')
out.close()
