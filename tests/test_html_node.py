import unittest

from src.html_node import LeafNode, ParentNode, text_node_to_html_node
from src.text_node import TextNode, TextType


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click here", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">Click here</a>')
    

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")
    

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()



class TestHTMLNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        child_node3 = LeafNode("span", "child3")
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child1</span><span>child2</span><span>child3</span></div>",
        )
    
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child", {"class": "text-bold"})
        parent_node = ParentNode("div", [child_node], {"id": "main"})
        self.assertEqual(
            parent_node.to_html(),
            '<div id="main"><span class="text-bold">child</span></div>',
        )
    
    def test_to_html_complex(self):
        grandchild_node = LeafNode("i", "grandchild", {"style": "color: red;"})
        child_node1 = LeafNode("b", "Text in bold")
        child_node2 = ParentNode("span", [grandchild_node], {"class": "text-italic"})
        child_node3 = LeafNode("img", "Image", {"src": "image.png", "alt": "An image"})
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3], {"id": "main"})
        self.assertEqual(
            parent_node.to_html(),
            '<div id="main"><b>Text in bold</b><span class="text-italic"><i style="color: red;">grandchild</i></span><img src="image.png" alt="An image">Image</img></div>',
            
        )



class TestTextToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_node_to_html_bold(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")
    
    def test_text_node_to_html_italic(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")
    
    def test_text_node_to_html_code(self):
        text_node = TextNode("Code snippet", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<code>Code snippet</code>")
    
    def test_text_node_to_html_link(self):
        text_node = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<a href="https://www.boot.dev">Click here</a>')
    
    def test_text_node_to_html_link_no_url(self):
        text_node = TextNode("Click here", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)
    
    def test_text_node_to_html_image(self):
        text_node = TextNode("An image", TextType.IMAGE, "https://www.boot.dev/image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<img src="https://www.boot.dev/image.png" alt="An image"></img>')
