import unittest
from src.blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks(self):
        markdown = "This is the first block.\n\nThis is the second block.\n\n\nThis is the third block."
        expected_blocks = [
            "This is the first block.",
            "This is the second block.",
            "This is the third block."
        ]
        result_blocks = markdown_to_blocks(markdown)
        self.assertEqual(result_blocks, expected_blocks)
    
    def test_single_block(self):
        markdown = "This is a single block without any double newlines."
        expected_blocks = [
            "This is a single block without any double newlines."
        ]
        result_blocks = markdown_to_blocks(markdown)
        self.assertEqual(result_blocks, expected_blocks)
    
    def test_empty_string(self):
        markdown = ""
        expected_blocks = []
        result_blocks = markdown_to_blocks(markdown)
        self.assertEqual(result_blocks, expected_blocks)
    
    def test_leading_trailing_newlines(self):
        markdown = "\n\nThis is a block with leading and trailing newlines.\n\n"
        expected_blocks = [
            "This is a block with leading and trailing newlines."
        ]
        result_blocks = markdown_to_blocks(markdown)
        self.assertEqual(result_blocks, expected_blocks)


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code(self):
        block = "```\nThis is code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> This is a quote\n> continued here"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = "This is a regular paragraph without any special formatting."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading_many_hashes(self):
        block = "####### This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading_no_space(self):
        block = "###This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_code_not_ending(self):
        block = "```\nThis is code"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_code_not_starting(self):
        block = "This is code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_quote_not_all_lines(self):
        block = "> This is a quote\nThis is not a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_unordered_list_not_all_lines(self):
        block = "- Item 1\nItem 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_unordered_list_no_space(self):
        block = "-Item 1\n-Item 2\n-Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_not_all_lines(self):
        block = "1. First item\nSecond item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_no_space(self):
        block = "1.First item\n2.Second item\n3.Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_no_ordering(self):
        block = "1. First item\n1. Second item\n1. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_starting_not_1(self):
        block = "2. First item\n3. Second item\n4. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
