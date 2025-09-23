import unittest
from markdowntotextnode import extract_markdown_images, extract_markdown_links


class TestMarkdownToTextNode(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        text = "Here is a link: [link text](https://example.com)"
        expected = [("link text", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_no_images(self):
        text = "This text has no images."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)
    
    def test_no_links(self):
        text = "This text has no links."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_multiple_images_and_links(self):
        text = "Image1: ![img1](url1) Link1: [link1](url2) Image2: ![img2](url3) Link2: [link2](url4)"
        expected_images = [("img1", "url1"), ("img2", "url3")]
        expected_links = [("link1", "url2"), ("link2", "url4")]
        self.assertEqual(extract_markdown_images(text), expected_images)
        self.assertEqual(extract_markdown_links(text), expected_links)
    
    def test_link_at_the_beginning(self):
        text = "[start](url_start) and some text"
        expected = [("start", "url_start")]
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_image_at_the_beginning(self):
        text = "![start_img](url_img_start) and some text"
        expected = [("start_img", "url_img_start")]
        self.assertEqual(extract_markdown_images(text), expected)