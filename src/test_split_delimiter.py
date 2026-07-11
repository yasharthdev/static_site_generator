from split_delimiter import split_nodes_delimiter
from unittest import TestCase
from textnode import TextNode, TextType

class TestSplitDelimiter(TestCase):
    def test_split_single_text_with_code_to_code(self):
        node = TextNode("This is a text with a `code` block", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [TextNode("This is a text with a ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(" block", TextType.TEXT)]
        )

    def test_split_multiple_bold_to_code(self):
        node1 = TextNode("Some bold text here", TextType.BOLD)
        node2 = TextNode("Some more already bolded text", TextType.BOLD)
        self.assertEqual(
            split_nodes_delimiter([node1, node2], "`", TextType.CODE),
            [
                TextNode("Some bold text here", TextType.BOLD), TextNode("Some more already bolded text", TextType.BOLD)
            ]
        )

    def test_split_multiple_bold_and_text_with_code_to_code(self):
        nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode(" and this has `code` and more `code` in it", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes, "`", TextType.CODE),
            [TextNode("This is ", TextType.TEXT), TextNode("already bold", TextType.BOLD), TextNode(" and this has ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(" and more ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(" in it", TextType.TEXT)]
        )

    def test_split_multiple_italic_and_text_with_bold_to_bold(self):
        nodes = [
            TextNode("This is", TextType.TEXT),
            TextNode("some already italic", TextType.ITALIC),
            TextNode("and **lots and lots** of **large** bold text", TextType.TEXT),
            TextNode("and some more code for fun", TextType.CODE)
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes, "**", TextType.BOLD),
            [TextNode("This is", TextType.TEXT), TextNode("some already italic", TextType.ITALIC), TextNode("and ", TextType.TEXT), TextNode("lots and lots", TextType.BOLD), TextNode(" of ", TextType.TEXT), TextNode("large", TextType.BOLD), TextNode(" bold text", TextType.TEXT), TextNode("and some more code for fun", TextType.CODE)]
        )
