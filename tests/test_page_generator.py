from src.page_generator import extract_title
import unittest


class TestExtractTitle(unittest.TestCase):
    def test_valid_title(self):
        markdown = "# My Title\nSome content here."
        self.assertEqual(extract_title(markdown), "My Title")

    def test_no_title(self):
        markdown = "Some content here."
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "Markdown content does not start with a title.")

    def test_empty_content(self):
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "Markdown content is empty.")

    def test_title_with_extra_spaces(self):
        markdown = "#    My Title   \nSome content here."
        self.assertEqual(extract_title(markdown), "My Title")

    def test_multiple_lines_before_title(self):
        markdown = "\n\n# My Title\nSome content here."
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "Markdown content does not start with a title.")
    
    def test_h2(self):
        markdown = "## My Subtitle\nSome content here."
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "Markdown content does not start with a title.")
