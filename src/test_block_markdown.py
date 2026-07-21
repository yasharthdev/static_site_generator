from unittest import TestCase
from block_markdown import markdown_to_blocks, BlockType, block_to_block_type
from block_markdown import markdown_to_html_node

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

        block = "```\nprint()\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "```\nprint()```"
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)
        block = "``` print()```"
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = ">Something in the rain\n>Something else"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        block = "- This is a list\n- of some items\n- know that it's unordered"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)

        block = "1. apples\n2. bananas\n3. something else"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "1. apples\n3. bananas\n7. something else"
        self.assertNotEqual(block_to_block_type(block), BlockType.OLIST)

        block = "This is supposedly a paragraph\n\nHas mutliple lines in it"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        

    # markdown to html_nodes tests
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        )

        md2 = """
```
print('Something')
def func():
    return 'Hello'
print(func())
**bolded** text
```
"""
        html = markdown_to_html_node(md2).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>print('Something')\ndef func():\n    return 'Hello'\nprint(func())\n**bolded** text\n</code></pre></div>"
        )

    def test_ulist(self):
        md = """
- something
- some element here
- some **bolded** thingy
- _italics_ for good measure
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>something</li><li>some element here</li><li>some <b>bolded</b> thingy</li><li><i>italics</i> for good measure</li></ul></div>"
        )

    def test_olist(self):
        md = """
1. Rajhans
2. Hotel **California**
3. what is this?
4. It's _love_
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Rajhans</li><li>Hotel <b>California</b></li><li>what is this?</li><li>It's <i>love</i></li></ol></div>"
        )

    def test_quote(self):
        md = """
> To be or not to be
>that is the question
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>To be or not to be that is the question</blockquote></div>"
        )

        md_not_quote = ">\nNot a quote"
        html = markdown_to_html_node(md_not_quote).to_html()
        self.assertEqual(
            html, "<div><p>> Not a quote</p></div>"
        )

    def test_heading(self):
        md = """
# This is a heading

## This one is another

### And this is yet another heading
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><h2>This one is another</h2><h3>And this is yet another heading</h3></div>"
        )
        
        md_not_heading = "#This is not a heading"
        html = markdown_to_html_node(md_not_heading).to_html()
        self.assertEqual(
            html, "<div><p>#This is not a heading</p></div>"
        )

    def test_mixed_stuff(self):
        md = """
# Main Heading

This is a **paragraph** with _italic_ text and a `code` snippet.

## A Subheading

> A wise quote spanning
> two lines here

- first item with **bold**
- second item with _italic_
- third plain item

1. step one
2. step two with `code`
3. step three

```
def greet(name):
    return f"Hello, {name}"
```
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h1>Main Heading</h1><p>This is a <b>paragraph</b> with <i>italic</i> text and a <code>code</code> snippet.</p><h2>A Subheading</h2><blockquote>A wise quote spanning two lines here</blockquote><ul><li>first item with <b>bold</b></li><li>second item with <i>italic</i></li><li>third plain item</li></ul><ol><li>step one</li><li>step two with <code>code</code></li><li>step three</li></ol><pre><code>def greet(name):\n    return f\"Hello, {name}\"\n</code></pre></div>"
        )