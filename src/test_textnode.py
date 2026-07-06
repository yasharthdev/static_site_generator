import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_eq_different_text(self):
        node1 = TextNode("This is something", TextType.BOLD)
        node2 = TextNode("This is another something, can't be equal", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_url(self):
        node1 = TextNode("Another text node", TextType.ITALIC, None)
        node2 = TextNode("Another text node", TextType.ITALIC, "www.google.com")
        self.assertNotEqual(node1, node2)

    def test_eq_url(self):
        node1 = TextNode("Another text node", TextType.ITALIC, "www.google.com")
        node2 = TextNode("Another text node", TextType.ITALIC, "www.google.com")
        self.assertEqual(node1, node2)

    def test_not_eq_different_text_type(self):
        node1 = TextNode("Another text node", TextType.LINK)
        node2 = TextNode("Another text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = TextNode("This is the final one", TextType.IMAGE, "google.com")
        self.assertEqual(
            "TextNode(This is the final one, image, google.com)",
            repr(node)
        )

if __name__ == "__main__":
    unittest.main()