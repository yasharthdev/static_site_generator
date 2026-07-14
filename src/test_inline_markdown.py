from inline_markdown import split_nodes_delimiter
from inline_markdown import extract_markdown_images, extract_markdown_links
from unittest import TestCase
from textnode import TextNode, TextType

class TestInlineMarkdown(TestCase):
    # tests for the delimiter
    def test_delim_split_single_text_with_code_to_code(self):
        node = TextNode("This is a text with a `code` block", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [TextNode("This is a text with a ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(" block", TextType.TEXT)]
        )

    def test_delim_split_multiple_bold_to_code(self):
        node1 = TextNode("Some bold text here", TextType.BOLD)
        node2 = TextNode("Some more already bolded text", TextType.BOLD)
        self.assertEqual(
            split_nodes_delimiter([node1, node2], "`", TextType.CODE),
            [
                TextNode("Some bold text here", TextType.BOLD), TextNode("Some more already bolded text", TextType.BOLD)
            ]
        )

    def test_delim_split_multiple_bold_and_text_with_code_to_code(self):
        nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode(" and this has `code` and more `code` in it", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes, "`", TextType.CODE),
            [TextNode("This is ", TextType.TEXT), TextNode("already bold", TextType.BOLD), TextNode(" and this has ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(" and more ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(" in it", TextType.TEXT)]
        )

    def test_delim_split_multiple_italic_and_text_with_bold_to_bold(self):
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

    # tests for images
    def test_normal_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertEqual(
            [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')],
            matches
        )

    def test_empty_image(self):
        matches = extract_markdown_images( "A completely empty image ![]()." )
        self.assertEqual([("", "")], matches)

    def test_broken_image(self):
        matches = extract_markdown_images("A broken image ![missing the closing bracket(https://boot.dev/img.png).")
        self.assertEqual([], matches)

    def test_images_missing_closing_parenthesis(self):
        matches = extract_markdown_images("An image with no closing parenthesis ![broken image](https://boot.dev/img.png")
        self.assertEqual([], matches)

    def test_images_without_spaces(self):
        matches = extract_markdown_images(
            "Images touching each other ![one](https://one.png)![two](https://two.png)."
        )
        self.assertEqual(
            matches, [('one', 'https://one.png'), ('two', 'https://two.png')]
        )

    def test_fake_image_whitespace_trap(self):
        matches = extract_markdown_images(
            "Is this an image? ! [trick question](https://boot.dev/img.png)."
        )
        self.assertEqual(matches, [])

    # tests for links
    def test_normal_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        )
        self.assertEqual(
            [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')], matches
        )
    
    def test_empty_link(self):
        matches = extract_markdown_links("A completely empty link []().")
        self.assertEqual([("", "")], matches)

    def test_broken_link(self):
        matches = extract_markdown_links("A broken link [missing the closing bracket(https://boot.dev).")
        self.assertEqual([], matches)

    def test_links_missing_closing_parenthesis(self):
        matches = extract_markdown_links(
            "A link with no closing parenthesis [broken link](https://boot.dev"
        )
        self.assertEqual([], matches)

    def test_multiple_links_without_spaces(self):
        matches = extract_markdown_links(
            "Links touching each other [one](https://one.com)[two](https://two.com)."
        )
        self.assertEqual(
            [("one", "https://one.com"), ("two", "https://two.com")], matches
        )

    def test_link_with_extra_parenthesis_inside_URL(self):
        matches = extract_markdown_links(
            "A link with weird URL formatting [wiki](https://en.wikipedia.org/wiki/File_(disambiguation))."
        )
        self.assertEqual(matches, [])
