import unittest
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
    extract_title,
)


class TestExtractTile(unittest.TestCase):

    def test_heading1(self):
        md = """
# Title

Not a title #
"""
        title = extract_title(md)
        self.assertEqual(title, "Title")

    def test_heading2(self):
        md = """
## Heading 2
"""
        with self.assertRaises(Exception):
            extract_title(md)


class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_paragrahs_qoutes(self):
        md = """
Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
            '<div><p>Here\'s the deal, <b>I like Tolkien</b>.</p><blockquote>"I am in fact a Hobbit in all but size."-- J.R.R. Tolkien</blockquote></div>'
        )


    def test_quotes(self):
        md = """
> 'Interesting and deep quote'
>
> -- buh
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>'Interesting and deep quote'-- buh</blockquote></div>"
        )


    def test_olists(self):
        md = """
1. This is the **first** list item
2. This is the second list item
3. This is the _third_ list item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is the <b>first</b> list item</li><li>This is the second list item</li><li>This is the <i>third</i> list item</li></ol></div>",
        )

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
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_block(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlock(unittest.TestCase):

    def test_paragraph(self):

        md_text = "This is **bolded** paragraph"

        block_type = block_to_block_type(md_text)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_heading(self):

        md_text = "# Level 1 Heading"

        block_type = block_to_block_type(md_text)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_quote(self):

        md_text = ("> 'Interesting and deep quote'"
                   "> "
                   "> -- buh")
        block_type = block_to_block_type(md_text)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_code_block(self):
        md_text = """```\ncode\n```"""
        block_type = block_to_block_type(md_text)
        self.assertEqual(block_type, BlockType.CODE)

def test_ordered_list(self):
    md_text = "1. ordered item one\n2. ordered item two\n3. ordered item three"

    block_type = block_to_block_type(md_text)
    self.assertEqual(block_type, BlockType.ORDERED_LIST)

def test_unordered_list(self):
    md_text = "- unordered list item one\n- unordered list item two\n- unordred list item three"
    block_type = block_to_block_type(md_text)
    self.assertEqual(block_type, BlockType.UNORDERED_LIST)
