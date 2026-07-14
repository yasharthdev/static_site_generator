from extract_links_and_images import extract_markdown_images, extract_markdown_links
from unittest import TestCase

class TestExtractor(TestCase):
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