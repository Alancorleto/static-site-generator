import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res = []
    for old_node in old_nodes:
        text_split = old_node.text.split(delimiter)
        if len(text_split) % 2 == 0:
            # If the length is even, it means there's an unmatched delimiter
            raise ValueError("Unmatched delimiter in text")
        for i, text in enumerate(text_split):
            if i % 2 == 1:
                res.append(TextNode(text, text_type))
            else:
                res.append(TextNode(text, old_node.text_type))
    return res


def split_nodes_image(old_nodes):
    res = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)

        for alt_text, url in images:
            delimiter = f"![{alt_text}]({url})"
            text_split = old_node.text.split(delimiter)
            # Append text before the link
            if text_split[0]:
                res.append(TextNode(text_split[0], old_node.text_type))
            # Append the link node
            res.append(TextNode(alt_text, TextType.IMAGE, url))
            # Update old_node_text to the remaining text after the link
            old_node.text = text_split[-1]
        
        # Append any remaining text after the last link
        if old_node.text:
            res.append(TextNode(old_node.text, old_node.text_type))
    return res


def split_nodes_link(old_nodes):
    res = []
    text_split = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)

        for link_text, url in links:
            delimiter = f"[{link_text}]({url})"
            text_split = old_node.text.split(delimiter)
            # Append text before the link
            if text_split[0]:
                res.append(TextNode(text_split[0], old_node.text_type))
            # Append the link node
            res.append(TextNode(link_text, TextType.LINK, url))
            # Update old_node_text to the remaining text after the link
            old_node.text = text_split[-1]
        
        # Append any remaining text after the last link
        if old_node.text:
            res.append(TextNode(old_node.text, old_node.text_type))
    
    return res


def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

