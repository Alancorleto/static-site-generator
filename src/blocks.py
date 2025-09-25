from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip().strip('\n') for block in blocks]
    blocks = [block for block in blocks if block != ""]
    return blocks


def block_to_block_type(block):
    if block_is_heading(block):
        return BlockType.HEADING
    elif block_is_code(block):
        return BlockType.CODE
    elif block_is_quote(block):
        return BlockType.QUOTE
    elif block_is_unordered_list(block):    
        return BlockType.UNORDERED_LIST
    elif block_is_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def block_is_heading(block):
    block_split = block.split(" ")
    if len(block_split) == 0:
        return False
    if len(block_split[0]) > 6:
        return False
    for character in block_split[0]:
        if character != "#":
            return False
    return True


def block_is_code(block):
    return block.startswith("```") and block.endswith("```")


def block_is_quote(block):
    block_split = block.split("\n")
    return all(line.startswith(">") for line in block_split)


def block_is_unordered_list(block):
    block_split = block.split("\n")
    return all(line.strip().startswith("- ") for line in block_split)


def block_is_ordered_list(block):
    block_split = block.split("\n")
    for i in range(len(block_split)):
        line = block_split[i]
        if not line.startswith(f"{i+1}. "):
            return False
    return True
