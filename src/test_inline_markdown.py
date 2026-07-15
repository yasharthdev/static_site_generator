from inline_markdown import split_nodes_delimiter
from inline_markdown import extract_markdown_images, extract_markdown_links
from unittest import TestCase
from textnode import TextNode, TextType
from inline_markdown import split_nodes_image, split_nodes_link, text_to_textnodes

class TestInlineMarkdown(TestCase):
    # tests for the delimiterC
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

    # tests for split_nodes_image
    def test_split_nodes_no_images(self):
        node = TextNode("Just plain text here", TextType.TEXT)
        self.assertEqual(
            [(TextNode("Just plain text here", TextType.TEXT))], split_nodes_image([node])
        )

    def test_split_nodes_bold_text_no_image(self):
        node = TextNode("Some already bolded text", TextType.BOLD)
        self.assertEqual(
            [TextNode("Some already bolded text", TextType.BOLD)], split_nodes_image([node])
        )

    def test_split_nodes_single_image_no_surrounding_text(self):
        node = TextNode("![some image](https://someimage.png)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("some image", TextType.IMAGE, "https://someimage.png")],
            split_nodes_image([node])
        )

    def test_split_nodes_starts_with_image(self):
        node = TextNode(
            "![cute cat](https://igmur.com/cute-cat-image) looks cute right?", TextType.TEXT
        )
        self.assertListEqual(
            [TextNode("cute cat", TextType.IMAGE, "https://igmur.com/cute-cat-image"), TextNode(" looks cute right?", TextType.TEXT)],
            split_nodes_image([node])
        )

    def test_split_nodes_ends_with_image(self):
        node = TextNode(
            "Looks cute right? ![cute cat](https://igmur.com/cute-cat-image)", TextType.TEXT
        )
        self.assertListEqual(
            [TextNode("Looks cute right? ", TextType.TEXT), TextNode("cute cat", TextType.IMAGE, "https://igmur.com/cute-cat-image")],
            split_nodes_image([node])
        )

    def test_split_nodes_mutliple_images(self):
        node = TextNode(
            "here's one ![image1](https://image1.com) here's another ![image2](https://image2.com) and here's the last one ![image3](https://image3.com)",
            TextType.TEXT
        )   
        self.assertListEqual(
            [TextNode("here's one ", TextType.TEXT), TextNode("image1", TextType.IMAGE, "https://image1.com"), TextNode(" here's another ", TextType.TEXT), TextNode("image2", TextType.IMAGE, "https://image2.com"), TextNode(" and here's the last one ", TextType.TEXT), TextNode("image3", TextType.IMAGE, "https://image3.com")],
            split_nodes_image([node])
        )

    def test_split_nodes_multiple_mixed_image_nodes(self):
        nodes = [
            TextNode("An image ![image](igmur.com/image)", TextType.TEXT),
            TextNode("some bolded text", TextType.BOLD),
            TextNode("Some code", TextType.CODE),
            TextNode("two images ![image1](igmur.com/image1) and ![image2](igmur.com/image2)", TextType.TEXT)
        ]
        self.assertListEqual(
            [TextNode("An image ", TextType.TEXT), TextNode("image", TextType.IMAGE, "igmur.com/image"), TextNode("some bolded text", TextType.BOLD), TextNode("Some code", TextType.CODE), TextNode("two images ", TextType.TEXT), TextNode("image1", TextType.IMAGE, "igmur.com/image1"), TextNode(" and ", TextType.TEXT), TextNode("image2", TextType.IMAGE, "igmur.com/image2")],
            split_nodes_image(nodes)
        )

    def test_split_nodes_duplicate_images(self):
        node = TextNode("One image ![image](igmur.com/image) and the same one again ![image](igmur.com/image)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("One image ", TextType.TEXT), TextNode("image", TextType.IMAGE, "igmur.com/image"), TextNode(" and the same one again ", TextType.TEXT), TextNode("image", TextType.IMAGE, "igmur.com/image")],
            split_nodes_image([node])
        ) 

    # test for split_nodes_link
    def test_split_nodes_no_links(self):
        node = TextNode("Just plain text here", TextType.TEXT)
        self.assertListEqual(
            [(TextNode("Just plain text here", TextType.TEXT))], split_nodes_link([node])
        )    

    def test_split_nodes_bold_text_no_link(self):
        node = TextNode("Some already bolded text", TextType.BOLD)
        self.assertEqual(
            [TextNode("Some already bolded text", TextType.BOLD)], split_nodes_link([node])
        )

    def test_split_nodes_single_link_no_surrounding_text(self):
        node = TextNode("[some link](https://somelink.com)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("some link", TextType.LINK, "https://somelink.com")],
            split_nodes_link([node])
        )
    
    def test_split_nodes_starts_with_link(self):
        node = TextNode(
            "[wikipedia](wikipedia.com) check for more information", TextType.TEXT
        )
        self.assertListEqual(
            [TextNode("wikipedia", TextType.LINK, "wikipedia.com"), TextNode(" check for more information", TextType.TEXT)],
            split_nodes_link([node])
        )

    def test_split_nodes_ends_with_link(self):
        node = TextNode(
            "For more info [click here](https://some-random-link.com)", TextType.TEXT
        )
        self.assertListEqual(
            [TextNode("For more info ", TextType.TEXT), TextNode("click here", TextType.LINK, "https://some-random-link.com")],
            split_nodes_link([node])
        )

    def test_split_nodes_mutliple_links(self):
        node = TextNode(
            "this is [link1](https://link1.com) and this is [link2](https://link2.com)",
            TextType.TEXT
        )   
        self.assertListEqual(
            [TextNode("this is ", TextType.TEXT), TextNode("link1", TextType.LINK, "https://link1.com"), TextNode(" and this is ", TextType.TEXT), TextNode("link2", TextType.LINK, "https://link2.com")],
            split_nodes_link([node])
        )

    def test_split_nodes_mutiple_mixed_link_nodes(self):
        nodes = [
            TextNode("A link [link](somelink.com)", TextType.TEXT),
            TextNode("some bolded text", TextType.BOLD),
            TextNode("Some code", TextType.CODE),
            TextNode("this is [link1](https://link1.com) and this is [link2](https://link2.com)", TextType.TEXT)
        ]
        self.assertListEqual(
            [TextNode("A link ", TextType.TEXT), TextNode("link", TextType.LINK, "somelink.com"), TextNode("some bolded text", TextType.BOLD), TextNode("Some code", TextType.CODE), TextNode("this is ", TextType.TEXT), TextNode("link1", TextType.LINK, "https://link1.com"), TextNode(" and this is ", TextType.TEXT), TextNode("link2", TextType.LINK, "https://link2.com")],
            split_nodes_link(nodes)
        )

    def test_split_nodes_duplicate_links(self):
        node = TextNode("Here's a link [link](somelink.com) and here's the same one again [link](somelink.com)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("Here's a link ", TextType.TEXT), TextNode("link", TextType.LINK, "somelink.com"), TextNode(" and here's the same one again ", TextType.TEXT), TextNode("link", TextType.LINK, "somelink.com")],
            split_nodes_link([node])
        )

    # tests for text to TextNodes
    def test_text_to_node_one(self):
        text = "Sometimes you just need **strong emphasis** and _subtle styling_ to make your point, like you'll find in this [Markdown Guide](https://www.markdownguide.org)."
        self.assertListEqual(
            [TextNode("Sometimes you just need ", TextType.TEXT), TextNode("strong emphasis", TextType.BOLD), TextNode(" and ", TextType.TEXT), TextNode("subtle styling", TextType.ITALIC), TextNode(" to make your point, like you'll find in this ", TextType.TEXT), TextNode("Markdown Guide", TextType.LINK, "https://www.markdownguide.org"), TextNode(".", TextType.TEXT)],
            text_to_textnodes(text)
        )

    def test_text_to_node_two(self):
        text = "![Warning Icon](https://example.com/warning.png) The system encountered a **critical** error! Please run `sudo reboot` in your terminal immediately."
        self.assertListEqual(
            [TextNode("Warning Icon", TextType.IMAGE, "https://example.com/warning.png"), TextNode(" The system encountered a ", TextType.TEXT), TextNode("critical", TextType.BOLD), TextNode(" error! Please run ", TextType.TEXT), TextNode("sudo reboot", TextType.CODE), TextNode(" in your terminal immediately.", TextType.TEXT)],
            text_to_textnodes(text)
        )

    def test_text_to_text_node_four(self):
        text = "To parse this _correctly_, your function should use a `Regex` pattern that checks for **matching brackets**."
        self.assertListEqual(
            [TextNode("To parse this ", TextType.TEXT), TextNode("correctly", TextType.ITALIC), TextNode(", your function should use a ", TextType.TEXT), TextNode("Regex", TextType.CODE), TextNode(" pattern that checks for ", TextType.TEXT), TextNode("matching brackets", TextType.BOLD), TextNode(".", TextType.TEXT)],
            text_to_textnodes(text)
        )