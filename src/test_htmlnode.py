import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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
            "HTMLNode(tag: h1, value: Introduction, children: [], props: {'id': 'chapter-1', 'class': 'title'})",
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

    # tests for the LeafNode class
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

    # tests for the ParentNode class
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
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_with_great_great_grandchildren(self):
        great_great_gc = LeafNode("u", "great great grandchild")
        great_gc = ParentNode("i", [great_great_gc])
        gc = ParentNode("b", [great_gc])
        child = ParentNode("span", [gc])
        parent = ParentNode("div", [child])
        self.assertEqual(
            parent.to_html(), "<div><span><b><i><u>great great grandchild</u></i></b></span></div>"
        )

    def test_to_html_with_no_children(self):
        """check if error raised in case of no children"""
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_with_many_children(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "bold text"),
                LeafNode(None, "normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "normal text")
            ]
        )
        self.assertEqual(
            parent_node.to_html(), "<p><b>bold text</b>normal text<i>italic text</i>normal text</p>"
        )
        