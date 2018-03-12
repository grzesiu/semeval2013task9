import sys
import xml.etree.ElementTree

tree = xml.etree.ElementTree.parse(sys.argv[1])

for node in tree.iter():
    print(node.tag, node.attrib)
