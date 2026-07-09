import unittest
from textnode import TextNode, TextType, text_node_to_html_node

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
        node2 = TextNode("Google.com", TextType.ITALIC, "https://www.google.com")
        self.assertNotEqual(node1, node2)

    def test_eq_url(self):
        node1 = TextNode("Click to Google", TextType.ITALIC, "www.google.com")
        node2 = TextNode("Click to Google", TextType.ITALIC, "www.google.com")
        self.assertEqual(node1, node2)

    def test_not_eq_different_text_type(self):
        node1 = TextNode("This is a link", TextType.LINK, "https://boot.dev")
        node2 = TextNode("Another text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = TextNode("This is the final one", TextType.IMAGE, "https://some_image.png")
        self.assertEqual(
            "TextNode(This is the final one, image, https://some_image.png)",
            repr(node)
        )

    # tests for the text_to_html function
    def test_text(self):
        node = TextNode("some text here", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "some text here")
    
    def test_italic(self):
        node = TextNode("italic here", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic here")

    def test_link(self):
        node = TextNode("some link here", TextType.LINK, "https://some.random.link")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "some link here")
        self.assertEqual(html_node.props, {'href': 'https://some.random.link'})

    def test_image(self):
        node = TextNode("goats and mountains", TextType.IMAGE, "https://some.random.image")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {'src': 'https://some.random.image', 'alt': 'goats and mountains'})


if __name__ == "__main__":
    unittest.main()