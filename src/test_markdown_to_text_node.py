import unittest
from markdown_to_text_node import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from text_node import TextNode, TextType


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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_no_images(self):
        text = "This text has no images."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)
    
    def test_image_at_the_beginning(self):
        text = "![start_img](url_img_start) and some text"
        expected = [("start_img", "url_img_start")]
        self.assertEqual(extract_markdown_images(text), expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "Here is a link: [link text](https://example.com)"
        expected = [("link text", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_no_links(self):
        text = "This text has no links."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_link_at_the_beginning(self):
        text = "[start](url_start) and some text"
        expected = [("start", "url_start")]
        self.assertEqual(extract_markdown_links(text), expected)



class TestExtractMarkdownLinksWithImages(unittest.TestCase):
    def test_multiple_images_and_links(self):
        text = "Image1: ![img1](url1) Link1: [link1](url2) Image2: ![img2](url3) Link2: [link2](url4)"
        expected_images = [("img1", "url1"), ("img2", "url3")]
        expected_links = [("link1", "url2"), ("link2", "url4")]
        self.assertEqual(extract_markdown_images(text), expected_images)
        self.assertEqual(extract_markdown_links(text), expected_links)



class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        
        expected_result = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]

        self.assertEqual(len(new_nodes), len(expected_result))
        self.assertEqual(new_nodes, expected_result)
    
    def test_no_links(self):
        node = TextNode("This is text without links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected_result = [TextNode("This is text without links.", TextType.TEXT)]
        self.assertEqual(new_nodes, expected_result)
    
    def test_only_link(self):
        node = TextNode("[only link](url_only)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected_result = [TextNode("only link", TextType.LINK, "url_only")]
        self.assertEqual(new_nodes, expected_result)

    def test_link_at_beginning(self):
        node = TextNode("[start](url_start) and some text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected_result = [
            TextNode("start", TextType.LINK, "url_start"),
            TextNode(" and some text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)
    
    def test_link_at_end(self):
        node = TextNode("Some text and a link [end](url_end)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected_result = [
            TextNode("Some text and a link ", TextType.TEXT),
            TextNode("end", TextType.LINK, "url_end"),
        ]
        self.assertEqual(new_nodes, expected_result)
    
    def test_multiple_nodes(self):
        nodes = [
            TextNode("First node with a link [link1](url1)", TextType.TEXT),
            TextNode("Second node without links.", TextType.TEXT),
            TextNode("Third node with another link [link2](url2)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        expected_result = [
            TextNode("First node with a link ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("Second node without links.", TextType.TEXT),
            TextNode("Third node with another link ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
        ]
        self.assertEqual(new_nodes, expected_result)
    
    def test_multiple_nodes_with_multiple_links(self):
        nodes = [
            TextNode("Node1 [link1](url1) and [link2](url2)", TextType.TEXT),
            TextNode("Node2 with no links.", TextType.TEXT),
            TextNode("Node3 [link3](url3)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        expected_result = [
            TextNode("Node1 ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode("Node2 with no links.", TextType.TEXT),
            TextNode("Node3 ", TextType.TEXT),
            TextNode("link3", TextType.LINK, "url3"),
        ]
        self.assertEqual(new_nodes, expected_result)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        expected_result = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ]

        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            expected_result,
            new_nodes,
        )
    
    def test_no_images(self):
        node = TextNode("This is text without images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected_result = [TextNode("This is text without images.", TextType.TEXT)]
        self.assertEqual(new_nodes, expected_result)
    
    def test_only_image(self):
        node = TextNode("![only image](url_only)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected_result = [TextNode("only image", TextType.IMAGE, "url_only")]
        self.assertEqual(new_nodes, expected_result)

    def test_image_at_beginning(self):
        node = TextNode("![start_img](url_img_start) and some text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected_result = [
            TextNode("start_img", TextType.IMAGE, "url_img_start"),
            TextNode(" and some text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)
    
    def test_image_at_end(self):
        node = TextNode("Some text and an image ![end_img](url_img_end)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected_result = [
            TextNode("Some text and an image ", TextType.TEXT),
            TextNode("end_img", TextType.IMAGE, "url_img_end"),
        ]
        self.assertEqual(new_nodes, expected_result)
    
    def test_multiple_nodes(self):
        nodes = [
            TextNode("First node with an image ![img1](url1)", TextType.TEXT),
            TextNode("Second node without images.", TextType.TEXT),
            TextNode("Third node with another image ![img2](url2)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        expected_result = [
            TextNode("First node with an image ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode("Second node without images.", TextType.TEXT),
            TextNode("Third node with another image ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
        ]
        self.assertEqual(new_nodes, expected_result)
    
    def test_multiple_nodes_with_multiple_images(self):
        nodes = [
            TextNode("Node1 ![img1](url1) and ![img2](url2)", TextType.TEXT),
            TextNode("Node2 with no images.", TextType.TEXT),
            TextNode("Node3 ![img3](url3)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        expected_result = [
            TextNode("Node1 ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode("Node2 with no images.", TextType.TEXT),
            TextNode("Node3 ", TextType.TEXT),
            TextNode("img3", TextType.IMAGE, "url3"),
        ]
        self.assertEqual(new_nodes, expected_result)