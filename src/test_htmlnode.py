import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        heading_node = HTMLNode(
            tag="h1",
            value="Introduction",
            children=[], 
            props={
                "id": "chapter-1",
                "class": "title"
            }
        )
        self.assertEqual(
            "HTMLNode(tag=h1, value=Introduction, children=[], props={'id': 'chapter-1', 'class': 'title'})",
            repr(heading_node)
        )
    
    def test_values(self):
        node = HTMLNode(
            "div",
            "This shite is pretty clever, I can't believe I forgot about it"
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(
            node.value,
            "This shite is pretty clever, I can't believe I forgot about it"
        )
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props_to_html(self):
        link_node = HTMLNode(
            tag="a",
            value="Click here",
            children=[],
            props={
                "href": "www.google.com",
                "target": "_blank"
            }
        )
        self.assertEqual(
            ' href="www.google.com" target="_blank"', link_node.props_to_html()
        )