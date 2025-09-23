from splitnodesdelimiter import split_nodes_delimiter
from textnode import TextNode, TextType
import unittest


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        old_nodes = [
            TextNode("This is a *bold* text", TextType.TEXT),
        ]

        delimiter = "*"
        text_type = TextType.BOLD

        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        result_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        self.assertEqual(len(result_nodes), len(expected_nodes))
        for result_node, expected_node in zip(result_nodes, expected_nodes):
            self.assertEqual(result_node.text, expected_node.text)
            self.assertEqual(result_node.text_type, expected_node.text_type)
        

    def test_multiple_delimiters(self):
        old_nodes = [
            TextNode("This is *bold* and *another bold* text", TextType.TEXT),
        ]

        delimiter = "*"
        text_type = TextType.BOLD

        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        result_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        self.assertEqual(len(result_nodes), len(expected_nodes))
        for result_node, expected_node in zip(result_nodes, expected_nodes):
            self.assertEqual(result_node.text, expected_node.text)
            self.assertEqual(result_node.text_type, expected_node.text_type)
        
    
    def test_different_delimiters(self):
        old_nodes = [
            TextNode("This is _italic_ text and *bold* text.", TextType.TEXT),
        ]

        delimiter1 = "_"
        delimiter2 = "*"
        
        text_type1 = TextType.ITALIC
        text_type2 = TextType.BOLD

        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]

        result_nodes = split_nodes_delimiter(old_nodes, delimiter1, text_type1)
        result_nodes = split_nodes_delimiter(result_nodes, delimiter2, text_type2)

        self.assertEqual(len(result_nodes), len(expected_nodes))
        for result_node, expected_node in zip(result_nodes, expected_nodes):
            self.assertEqual(result_node.text, expected_node.text)
            self.assertEqual(result_node.text_type, expected_node.text_type)
        

    def test_multiple_nodes(self):
        old_nodes = [
            TextNode("This is *bold* text.", TextType.TEXT),
            TextNode("Here is _italic_ text.", TextType.TEXT),
        ]

        delimiter1 = "*"
        delimiter2 = "_"
        
        text_type1 = TextType.BOLD
        text_type2 = TextType.ITALIC

        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
            TextNode("Here is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]

        result_nodes = split_nodes_delimiter(old_nodes, delimiter1, text_type1)
        result_nodes = split_nodes_delimiter(result_nodes, delimiter2, text_type2)

        self.assertEqual(len(result_nodes), len(expected_nodes))
        for result_node, expected_node in zip(result_nodes, expected_nodes):
            self.assertEqual(result_node.text, expected_node.text)
            self.assertEqual(result_node.text_type, expected_node.text_type)


