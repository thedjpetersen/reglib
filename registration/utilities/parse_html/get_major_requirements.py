from lxml import etree

def get_major_requirements(original_xml):
    tree = etree.fromstring(original_xml)
    audit = tree.getchildren()[0]
    return audit
