from textnode import TextNode

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
