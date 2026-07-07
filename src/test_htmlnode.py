import unittest
from htmlnode import HTMLNode, LeafNode

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

    def test_leaf_to_html_p(self):
       node = LeafNode("p", "A normal paragraph")
       self.assertEqual(node.to_html(), "<p>A normal paragraph</p>")
    
    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click this link", {
            "href": "https//:www.google.com",
            "target": "_blank"
        })
        self.assertEqual(
            node.to_html(), '<a href="https//:www.google.com" target="_blank">Click this link</a>'
        )

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Just some raw text")
        self.assertEqual(node.to_html(), "Just some raw text")
    
    def test_leaf_repr(self):
        node = LeafNode("p", "This is a paragraph", {"title": "something"})
        self.assertEqual(
            repr(node), "LeafNode(tag: p, value: This is a paragraph, props: {'title': 'something'})"
        )