from src.blocks import markdown_to_blocks, block_to_block_type, BlockType
from src.text_node import TextNode, TextType
from src.markdown_to_text_node import markdown_to_text_nodes
from src.html_node import HTMLNode, LeafNode, ParentNode, text_node_to_html_node


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in blocks:
        match block_to_block_type(block):
            case BlockType.HEADING:
                html_nodes.append(convert_heading_to_html_node(block))
            case BlockType.CODE:
                html_nodes.append(convert_code_to_html_node(block))
            case BlockType.QUOTE:
                html_nodes.append(convert_quote_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                html_nodes.append(convert_unordered_list_to_html_node(block))
            case BlockType.ORDERED_LIST:
                html_nodes.append(convert_ordered_list_to_html_node(block))
            case BlockType.PARAGRAPH:
                html_nodes.append(convert_paragraph_to_html_node(block))
            case _:
                raise ValueError(f"Unknown block type for block: {block}")
    
    return ParentNode("div", html_nodes)


def convert_heading_to_html_node(block):
    block_split = block.split(" ", 1)
    heading_level = len(block_split[0])
    heading_text = block_split[1]
    
    return ParentNode(f"h{heading_level}", text_to_children(heading_text))


def convert_code_to_html_node(block):
    code_text = block.strip("```").lstrip("\n")
    text_node = TextNode(code_text, TextType.CODE)
    html_node = text_node_to_html_node(text_node)
    return ParentNode("pre", [html_node])


def convert_quote_to_html_node(block):
    quote_lines = block.split("\n")
    quote_lines = [line.lstrip("> ") for line in quote_lines]
    quote_text = "\n".join(quote_lines)
    return ParentNode("blockquote", text_to_children(quote_text))


def convert_unordered_list_to_html_node(block):
    list_lines = block.split("\n")
    list_items = [line.lstrip("- ") for line in list_lines]
    li_nodes = [ParentNode("li", text_to_children(item)) for item in list_items]
    return ParentNode("ul", li_nodes)


def convert_ordered_list_to_html_node(block):
    list_lines = block.split("\n")
    list_items = []
    for i, line in enumerate(list_lines):
        prefix = f"{i+1}. "
        list_items.append(line[len(prefix):])
    li_nodes = [ParentNode("li", text_to_children(item)) for item in list_items]
    return ParentNode("ol", li_nodes)


def convert_paragraph_to_html_node(block):
    block = block.replace("\n", " ")
    return ParentNode("p", text_to_children(block))


def text_to_children(text):
    text_nodes = markdown_to_text_nodes(text)
    html_children = [text_node_to_html_node(text_node) for text_node in text_nodes]
    return html_children
