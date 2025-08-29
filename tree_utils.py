import json
import xml.etree.ElementTree as ET
from tkinter import ttk

def insert_json(tree, parent, json_data):
    """Recursively insert JSON data into the Treeview."""
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            node_id = tree.insert(parent, 'end', text=str(key))
            insert_json(tree, node_id, value)
    elif isinstance(json_data, list):
        for index, item in enumerate(json_data):
            node_id = tree.insert(parent, 'end', text=f"[{index}]")
            insert_json(tree, node_id, item)
    else:
        tree.insert(parent, 'end', text=str(json_data))

def insert_xml(tree, parent, element):
    """Recursively insert XML element into the Treeview."""
    node_text = element.tag
    if element.attrib:
        node_text += f" {element.attrib}"
    node_id = tree.insert(parent, 'end', text=node_text)
    for child in element:
        insert_xml(tree, node_id, child)
    if element.text and element.text.strip():
        tree.insert(node_id, 'end', text=element.text.strip())

def expand_all(tree, node=''):
    """Recursively expand all nodes in the Treeview."""
    children = tree.get_children(node)
    for child in children:
        tree.item(child, open=True)
        expand_all(tree, child)

def collapse_all(tree, node=''):
    """Recursively collapse all nodes in the Treeview."""
    children = tree.get_children(node)
    for child in children:
        tree.item(child, open=False)
        collapse_all(tree, child)

def extract_tree(tree, node='', format='json'):
    """Extract the tree structure to JSON or XML format."""
    def extract_json(node_id):
        children = tree.get_children(node_id)
        if not children:
            return tree.item(node_id)['text']
        result = {}
        for child in children:
            key = tree.item(child)['text']
            result[key] = extract_json(child)
        return result
    
    # def extract_xml(node_id):
    #     text = tree.item(node_id)['text'].strip()
    #     tag = text.split()[0] if text else "node"  # Default to "node" if empty

    #     #tag = tree.item(node_id)['text'].split()[0]
    #     element = ET.Element(tag)
    #     children = tree.get_children(node_id)
    #     for child in children:
    #         child_element = extract_xml(child)
    #         element.append(child_element)
    #     return element

    # def extract_xml(node_id):
    #     text = tree.item(node_id)['text'].strip()
    #     tag = text.split()[0] if text else "node"
    #     element = ET.Element(tag)

    #     children = tree.get_children(node_id)
    #     if not children:
    #         element.text = text
    #     else:
    #         for child in children:
    #             child_element = extract_xml(child)
    #             element.append(child_element)

    #     return element

    def extract_xml(node_id):
        text = tree.item(node_id)['text'].strip()
        tag = text.split()[0] if text else "node"
        element = ET.Element(tag)

        children = tree.get_children(node_id)
        if children:
            for child in children:
                child_text = tree.item(child)['text'].strip()
                if not tree.get_children(child):
                    # Leaf node with text content
                    element.text = child_text
                else:
                    child_element = extract_xml(child)
                    element.append(child_element)
        else:
            element.text = text

        return element

    if format == 'json':
        return extract_json(node)
    elif format == 'xml':
        return extract_xml(node)
    else:
        raise ValueError("Unsupported format. Use 'json' or 'xml'.")

def export_treeview_to_xml(treeview_widget, filename="output.xml"):
    root_xml = ET.Element("TreeviewData")

    def add_item_to_xml(parent_xml_element, item_id):
        item_info = treeview_widget.item(item_id)
        item_text = item_info['text']
        item_values = item_info['values']

        # Create an XML element for the current Treeview item
        # You might customize the tag name and attributes based on your data
        item_element = ET.SubElement(parent_xml_element, "Item", text=item_text)

        # Add values as attributes or sub-elements
        for i, value in enumerate(item_values):
            item_element.set(f"col{i+1}", str(value))

        # Recursively add child items
        for child_id in treeview_widget.get_children(item_id):
            add_item_to_xml(item_element, child_id)

    # Start with top-level items
    for top_level_item_id in treeview_widget.get_children(''):
        add_item_to_xml(root_xml, top_level_item_id)

    # Create and write the XML tree to a file
    tree = ET.ElementTree(root_xml)
    tree.write(filename, encoding='utf-8', xml_declaration=True)
    print(f"Treeview data exported to {filename}")


