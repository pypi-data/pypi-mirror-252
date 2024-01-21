from xml.etree import ElementTree
from liku import __all__ as liku_exports
from liku.elements import HTMLElement, h


def html(entity: str):
    root = ElementTree.fromstring(entity)
    element = root.tag.replace("-", "_")

    html_elem: HTMLElement
    if element in liku_exports:
        html_elem = h(element, root.attrib, [])  # type: ignore
    else:
        args: list[str] = []
        for key, value in root.attrib:
            args.append(f"{key}=")
