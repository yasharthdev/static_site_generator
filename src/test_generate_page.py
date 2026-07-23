from unittest import TestCase
from generate_page import extract_title

class TestGeneratePage(TestCase):
    def test_extract_title(self):
        md = """
# This is some heading

Some **bold** stuff

## This is a subheading
"""
        self.assertEqual("This is some heading", extract_title(md))


    def test_extract_title_multiple_h1(self):
        md = """
# The Main Title

# Another heading, but I just want the first title
"""
        self.assertEqual("The Main Title", extract_title(md))