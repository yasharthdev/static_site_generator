from unittest import TestCase
from block_markdown import markdown_to_blocks, BlockType, block_to_block_type

class TestBlockMarkdown(TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        self.assertListEqual(
            markdown_to_blocks(md), [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_to_blocks_two(self):
        md = """
This is a **Python** programming introduction

This is another paragraph emphasizing _readability_ and using `print()` functions here
This is the same paragraph on a new line







- This is a list of features
- with dynamic typing
"""
        self.assertListEqual(
            markdown_to_blocks(md), [
                "This is a **Python** programming introduction",
                "This is another paragraph emphasizing _readability_ and using `print()` functions here\nThis is the same paragraph on a new line",
                "- This is a list of features\n- with dynamic typing",
            ]
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "#not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "```\nprint()```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "``` print()```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = ">Something in the rain\n>Something else"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- This is a list\n- of some items\n- know that it's unordered"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. apples\n2. bananas\n3. something else"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "This is supposedly a paragraph\n\nHas mutliple lines in it"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        